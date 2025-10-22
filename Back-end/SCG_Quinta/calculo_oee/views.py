from django.shortcuts import render, redirect
from .forms import TurnoOEEForm
from .models import TurnoOEE, Producto, Detencion, Reproceso, ResumenTurnoOee
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .forms import ProduccionRealForm
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect
from .constants import TASA_NOMINAL_POR_PRODUCTO, TASA_NOMINAL_DEFECTO
from django.forms.models import model_to_dict
from openpyxl import Workbook
from datetime import datetime
import pytz
from urllib.parse import unquote
from django.db.models import Exists, OuterRef
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET
from django.db.models import Value, FloatField
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.functions import ExtractWeek, ExtractYear
from django.db.models import Sum


# Create your views here.

@csrf_exempt
@login_required
def crear_turno(request):
    if request.method == 'POST':
        form = TurnoOEEForm(request.POST)
        if form.is_valid():
            lote = form.save()

            # Guardar productos
            cliente = request.POST.getlist('cliente_producto[]')
            productos = request.POST.getlist('producto[]')
            codigos = request.POST.getlist('codigo[]')
            planeadas = request.POST.getlist('produccion_planeada[]')
            reales = request.POST.getlist('produccion_real[]')  # si ya se ingresan
            comentarios_pro = request.POST.getlist('comentarios_producto[]')  # <-- nuevo campo

            for cli, prod, cod, plan, real, com in zip(cliente, productos, codigos, planeadas, reales, comentarios_pro):
                Producto.objects.create(
                    lote=lote,
                    cliente=cli,
                    producto=prod,
                    codigo=cod,
                    produccion_planeada=int(plan) if plan else None,
                    produccion_real=int(real) if real else None,
                    comentarios=com.strip() if com else None  # <-- nuevo campo 
                )
            # 3) Con base en los productos guardados, actualizar el mismo TurnoOEE
            lote.cliente = cliente[0]
            lote.producto = productos[0]
            lote.codigo = codigos[0] or None

            # Sumar producción de todos los productos
            lote.produccion_planeada = sum(
                int(p) for p in planeadas if p.isdigit()
            )
            lote.produccion_real = sum(
                int(r) for r in reales if r.isdigit()
            )
            lote.save()
            
            # Guardar detenciones
            motivos   = request.POST.getlist('motivo_det[]')
            inicios   = request.POST.getlist('hora_inicio_det[]')
            finales   = request.POST.getlist('hora_fin_det[]')
            comentarios_det = request.POST.getlist('comentarios_det[]')  # <-- nuevo campo

            from datetime import datetime, timedelta
            fmt = "%H:%M"
            for mot, hi, hf, com in zip(motivos, inicios, finales, comentarios_det):
                # parseamos las horas
                t1 = datetime.strptime(hi, fmt)
                t2 = datetime.strptime(hf, fmt)
                if t2 < t1:
                    t2 += timedelta(days=1)
                dur = int((t2 - t1).total_seconds() // 60)

                Detencion.objects.create(
                    lote=lote,
                    motivo=mot,
                    hora_inicio=t1.time(),   # <-- aquí
                    hora_fin=   t2.time(),   # <-- y aquí
                    duracion=   dur,
                    comentarios= com # <-- nuevo campo
                )

            # Guardar reprocesos
            motivos_rep = request.POST.getlist('motivo_rep[]')
            cantidades_rep = request.POST.getlist('cantidad_rep[]')
            comentarios_rep = request.POST.getlist('comentarios_rep[]')  # <-- si quieres agregar comentarios a reprocesos
            for motivo, cantidad, comentario in zip(motivos_rep, cantidades_rep, comentarios_rep):
                Reproceso.objects.create(lote=lote, motivo=motivo, comentarios=comentario, cantidad=int(cantidad))

            return redirect('lista_turnos')  # Redirige al listado

    else:
        form = TurnoOEEForm()

    return render(request, 'calculo_oee/crear_turno.html', {'form': form})


@login_required
def resumen_turno(request, lote_id):
    lote = get_object_or_404(TurnoOEE, id=lote_id)

    # Evitar duplicados en ResumenTurnoOee
    if not ResumenTurnoOee.objects.filter(lote=lote).exists():
        fecha = lote.fecha
        turno = lote.turno
        supervisor = lote.supervisor

        # Productos asociados (pueden ser múltiples)
        productos_qs = lote.productos.all()
        if productos_qs.exists():
            # Suma planeada y real desde productos
            produccion_planificada = sum(p.produccion_planeada or 0 for p in productos_qs)
            produccion_real = sum(p.produccion_real or 0 for p in productos_qs)
            # Concatenar nombres y códigos únicos
            productos_concat = ", ".join(
                dict.fromkeys(p.producto for p in productos_qs if p.producto)
            )
            codigos_concat = ", ".join(
                dict.fromkeys(p.codigo for p in productos_qs if p.codigo)
            )
            cliente_concat = ", ".join(
                dict.fromkeys(p.cliente for p in productos_qs if p.cliente)
            )
            # Tasa nominal promedio (promedio simple)
            tasas = []
            for p in productos_qs:
                clave = (p.producto, p.codigo)
                tasas.append(TASA_NOMINAL_POR_PRODUCTO.get(clave, TASA_NOMINAL_DEFECTO))
            tasa_nominal = sum(tasas) / len(tasas) if tasas else TASA_NOMINAL_DEFECTO
        else:
            # Caída a lógica previa de un solo producto en el turno
            produccion_planificada = lote.produccion_planeada or 0
            produccion_real = lote.produccion_real or 0
            productos_concat = lote.producto
            codigos_concat = lote.codigo or ""
            cliente_concat = lote.cliente
            clave = (lote.producto, lote.codigo)
            tasa_nominal = TASA_NOMINAL_POR_PRODUCTO.get(clave, TASA_NOMINAL_DEFECTO)

        tiempo_paro = sum(d.duracion for d in lote.detenciones.all())
        productos_malos = sum(r.cantidad for r in lote.reprocesos.all())

        tiempo_operativo = lote.tiempo_planeado - tiempo_paro
        num_personas = lote.numero_personas or 0
        produccion_teorica = tasa_nominal * num_personas

        productos_buenos = produccion_real - productos_malos if produccion_real else 0

        disponibilidad = tiempo_operativo / lote.tiempo_planeado if lote.tiempo_planeado else 0
        rendimiento = produccion_real / produccion_teorica if produccion_teorica else 0
        calidad = productos_buenos / produccion_real if produccion_real else 0
        oee = disponibilidad * rendimiento * calidad * 100  # en %

        ResumenTurnoOee.objects.create(
            fecha=fecha,
            turno=turno,
            supervisor=supervisor,
            lote=lote,
            cliente=cliente_concat,
            codigo=codigos_concat,
            producto=productos_concat,
            linea=lote.linea,
            tiempo_paro=tiempo_paro,
            tiempo_planeado=lote.tiempo_planeado,
            produccion_teorica=round(produccion_teorica),
            produccion_planificada=produccion_planificada,
            produccion_real=produccion_real,
            productos_malos=productos_malos,
            productos_buenos=productos_buenos,
            numero_personas=lote.numero_personas,
            unidades_por_persona=round(produccion_real / lote.numero_personas, 2) if lote.numero_personas else 0,
            unidades_pp_hora=round(produccion_real / (lote.tiempo_planeado / 60) / lote.numero_personas, 2) if lote.numero_personas and lote.tiempo_planeado else 0,
            eficiencia=round(rendimiento * 100, 2),
            disponibilidad=round(disponibilidad * 100, 2),
            calidad=round(calidad * 100, 2),
            oee=round(oee, 2)
        )

    resumen = ResumenTurnoOee.objects.get(lote=lote)

    raw_next = request.GET.get('next', '')
    if raw_next:
        next_url = unquote(raw_next)
    else:
        next_url = reverse('lista_turnos')

    return render(request, 'calculo_oee/resumen_turno.html', {
        'resumen': resumen,
        'next_url': next_url,
    })

@csrf_exempt
@login_required
def cerrar_turno(request, lote_id):
    lote = get_object_or_404(TurnoOEE, id=lote_id)

    if request.method == 'POST':
        form = ProduccionRealForm(request.POST, instance=lote)
        if form.is_valid():
            form.save()
            return redirect('resumen_turno', lote_id=lote.id)
    else:
        form = ProduccionRealForm(instance=lote)

    return render(request, 'calculo_oee/cerrar_turno.html', {'form': form, 'lote': lote})

@login_required
def lista_turnos(request):
    qs = TurnoOEE.objects.all().order_by('-fecha')

    # Anotación: ¿existe resumen para este lote?
    resumen_subq = ResumenTurnoOee.objects.filter(lote=OuterRef('pk'))
    qs = qs.annotate(tiene_resumen=Exists(resumen_subq))

    # --- 1. Aplicar filtros GET si vienen ---
    fecha    = request.GET.get('fecha', '')
    linea    = request.GET.get('linea', '')
    cliente  = request.GET.get('cliente', '')
    producto = request.GET.get('producto', '')
    turno   = request.GET.get('turno', '')
    produccion_real = request.GET.get('produccion_real', '')

    if fecha:
        qs = qs.filter(fecha__date=fecha)
    if linea:
        qs = qs.filter(linea=linea)
    if cliente:
        qs = qs.filter(cliente=cliente)
    if producto:
        qs = qs.filter(producto=producto)
    if turno:
        qs = qs.filter(turno=turno)
    if produccion_real == 'null':
        qs = qs.filter(produccion_real__isnull=True)

     # --- 2. Filtro por estado (nuevo) ---
    estado = request.GET.get('estado', '')
    if estado == 'calcular_oee':
        # Tiene produccion_real, pero no tiene resumen aún
        qs = qs.filter(produccion_real__isnull=False, tiene_resumen=False)
    elif estado == 'cerrar_turno':
        # Aún no tiene produccion_real
        qs = qs.filter(produccion_real__isnull=True)
    elif estado == 'ver_resumen':
        # Ya existe resumen
        qs = qs.filter(tiene_resumen=True)

    # --- 3. Obtener valores únicos para los desplegables ---
    lineas    = TurnoOEE.objects.values_list('linea', flat=True).distinct()
    clientes  = TurnoOEE.objects.values_list('cliente', flat=True).distinct()
    productos = TurnoOEE.objects.values_list('producto', flat=True).distinct()
    turnos   = TurnoOEE.objects.values_list('turno', flat=True).distinct()

    # --- 4. Paginación ---
    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Construimos un querystring sin el parámetro page:
    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    querystring = query_params.urlencode()

    return render(request, 'calculo_oee/lista_turnos.html', {
        'turnos': page_obj,
        'lineas': lineas,
        'clientes': clientes,
        'productos': productos,
        'filtro_fecha': fecha,
        'filtro_linea': linea,
        'filtro_cliente': cliente,
        'filtro_producto': producto,
        'turnos_disponibles': turnos,
        'filtro_produccion_real': produccion_real,
        'filtro_estado': estado, 
        'querystring': querystring,   # <-- nuevo
    })
    
@login_required
def detalle_turno(request, lote_id):
    lote = get_object_or_404(TurnoOEE, id=lote_id)
    productos = lote.productos.all()
    detenciones = lote.detenciones.all()
    reprocesos = lote.reprocesos.all()

    next_param = request.GET.get('next', '')
    return render(request, 'calculo_oee/detalle_turno.html', {
        'lote': lote,
        'productos': productos,
        'detenciones': detenciones,
        'reprocesos': reprocesos,
        'next_url': next_param or reverse('lista_turnos'),
    })

@csrf_exempt
@login_required
def marcar_verificado(request, lote_id):
    next_param = request.GET.get('next') or request.POST.get('next', '')
    next_param = unquote(next_param) if next_param else ''

    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            resumen = get_object_or_404(ResumenTurnoOee, lote_id=lote_id)
            resumen.verificado = True
            # Evita error si el usuario no tiene 'nombre_completo'
            resumen.verificado_por = getattr(request.user, 'nombre_completo', request.user.get_username())
            resumen.fecha_de_verificacion = timezone.now()
            resumen.save()

            # ✅ Si hay next, vuelve directo al listado filtrado
            if next_param:
                return redirect(next_param)

            # Si no hay next, vuelve al resumen del turno
            return redirect(reverse('resumen_turno', args=[lote_id]))

    # GET u otro método: vuelve al resumen preservando next si existe
    base = reverse('resumen_turno', args=[lote_id])
    return redirect(f"{base}?next={next_param}") if next_param else redirect(base)
    
@login_required
def redireccionar_intermedio(request):
    url_inicio = reverse('intermedio')
    return HttpResponseRedirect(url_inicio)

@login_required
def redireccionar_intermedio_4(request):
    url_inicio = reverse('intermedio_4')
    return HttpResponseRedirect(url_inicio)

# Descargar registros de ResumenTurnoOee
@csrf_exempt
@login_required
def descargar_resumenturnooee(request):
    fecha_inicio_str = request.session.get('fechainicio')
    fecha_fin_str = request.session.get('fechafin')
    registros = None
    if fecha_inicio_str == None or fecha_fin_str == None:
        registros = ResumenTurnoOee.objects.all()
    else:
        fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio_str, '%Y-%m-%d'))
        fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin_str, '%Y-%m-%d'))
        registros = ResumenTurnoOee.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
    if not registros:
        return render(request, 'inicio/no_hay_datos.html')

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="resumen_turno_oee.xlsx"'

    wb = Workbook()
    ws = wb.active

    fields = [f.name for f in ResumenTurnoOee._meta.fields]
    ws.append(fields)

    def convertir_fecha(fecha):
        return fecha.astimezone(pytz.timezone('America/Santiago')).replace(tzinfo=None) if fecha else None

    for obj in registros:
        data = model_to_dict(obj, fields=fields)
        # si tienes DateTimeField y quieres formatear:
        if 'fecha' in data:
            data['fecha'] = convertir_fecha(data['fecha'])
        if 'fecha_de_verificacion' in data:
            data['fecha_de_verificacion'] = convertir_fecha(data['fecha_de_verificacion'])
        fila = []
        for field in fields:
            val = data[field]
            if hasattr(val, 'isoformat'):  # p.ej. datetime / date
                val = val.isoformat(sep=' ')
            fila.append(val)
        ws.append(fila)

    wb.save(response)
    if fecha_inicio_str != None or fecha_fin_str != None:
        del request.session['fechainicio']
        del request.session['fechafin']
    return response

@require_GET
def resumen_turno_oee_opciones(request):
    try:
        qs = ResumenTurnoOee.objects.all()
        semanas = (qs.annotate(sem=ExtractWeek('fecha'))
                     .values_list('sem', flat=True)
                     .distinct())
        anios = (qs.annotate(y=ExtractYear('fecha'))
                   .values_list('y', flat=True)
                   .distinct())
        lineas = (qs.values_list('linea', flat=True)
                    .distinct()
                    .order_by('linea'))
        turnos = (qs.values_list('turno', flat=True)
                    .distinct()
                    .order_by('turno'))

        # Ordena semanas y años
        semanas = sorted([s for s in semanas if s is not None])
        anios = sorted([a for a in anios if a is not None])

        return JsonResponse({
            "semanas": semanas,   # [1..53]
            "anios": anios,       # [2024, 2025, ...]
            "lineas": list(lineas),
            "turnos": list(turnos)
        }, safe=False, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        return HttpResponseBadRequest(f"error_opciones: {e}")

@require_GET
def resumen_turno_oee_api(request):
    """
    Devuelve puntos OEE con: fecha, turno, linea, disponibilidad, eficiencia, oee, target, lote_id
    Soporta filtros múltiples: semana, anio, linea, turno, desde, hasta
    """
    try:
        semanas = request.GET.getlist('semana')
        anios   = request.GET.getlist('anio')
        lineas  = request.GET.getlist('linea')
        turnos  = request.GET.getlist('turno')
        desde   = request.GET.get('desde')
        hasta   = request.GET.get('hasta')

        qs = (ResumenTurnoOee.objects
              .annotate(target=Value(70.0, output_field=FloatField()))  # ajusta tu target si es otro
              .values('id', 'fecha', 'turno', 'linea',
                      'disponibilidad', 'eficiencia', 'oee',
                      'target', 'lote_id'))

        if semanas:
            qs = qs.annotate(sem=ExtractWeek('fecha')) \
                   .filter(sem__in=[int(s) for s in semanas if s.isdigit()])
        if anios:
            qs = qs.annotate(an=ExtractYear('fecha')) \
                   .filter(an__in=[int(a) for a in anios if a.isdigit()])
        if lineas:
            qs = qs.filter(linea__in=lineas)
        if turnos:
            qs = qs.filter(turno__in=turnos)
        if desde and hasta:
            qs = qs.filter(fecha__range=[desde, hasta])
        elif desde:
            qs = qs.filter(fecha__gte=desde)
        elif hasta:
            qs = qs.filter(fecha__lte=hasta)

        datos = sorted(qs, key=lambda d: (d['fecha'], str(d['turno'])))
        return JsonResponse(list(datos), safe=False, json_dumps_params={'ensure_ascii': False})

    except Exception as e:
        return HttpResponseBadRequest(f"error_api_resumen: {e}")
    
@login_required
def graficos_oee(request):
    return render(request, 'calculo_oee/graficos_oee.html')

@require_GET
def detenciones_turno_api(request):
    """
    Devuelve: fecha, turno, linea, motivo, porcentaje (0..100), lote_id
    % calculado sobre tiempo_planeado del ResumenTurnoOee.
    Agrega un motivo extra: 'Tiempo Productivo' (resto).
    """
    try:
        semanas = request.GET.getlist('semana')
        anios   = request.GET.getlist('anio')
        lineas  = request.GET.getlist('linea')
        turnos  = request.GET.getlist('turno')
        desde   = request.GET.get('desde')
        hasta   = request.GET.get('hasta')

        # Detención -> TurnoOEE (lote) -> ResumenTurnoOee
        qs = (Detencion.objects
              .select_related('lote')
              .filter(lote__resumenes_turno__isnull=False)
              .values(
                  'lote_id',                                  # 👈 NECESARIO
                  'lote__resumenes_turno__id',                # id del resumen
                  'lote__resumenes_turno__fecha',
                  'lote__resumenes_turno__turno',
                  'lote__resumenes_turno__linea',
                  'motivo'
              )
              .annotate(duracion_total=Sum('duracion'))
              .order_by('lote__resumenes_turno__fecha',
                        'lote__resumenes_turno__turno',
                        'motivo'))

        # Filtros
        if semanas:
            qs = qs.annotate(sem=ExtractWeek('lote__resumenes_turno__fecha')) \
                   .filter(sem__in=[int(s) for s in semanas if s.isdigit()])
        if anios:
            qs = qs.annotate(an=ExtractYear('lote__resumenes_turno__fecha')) \
                   .filter(an__in=[int(a) for a in anios if a.isdigit()])
        if lineas:
            qs = qs.filter(lote__resumenes_turno__linea__in=lineas)
        if turnos:
            qs = qs.filter(lote__resumenes_turno__turno__in=turnos)
        if desde and hasta:
            qs = qs.filter(lote__resumenes_turno__fecha__range=[desde, hasta])
        elif desde:
            qs = qs.filter(lote__resumenes_turno__fecha__gte=desde)
        elif hasta:
            qs = qs.filter(lote__resumenes_turno__fecha__lte=hasta)

        # Resúmenes con tiempo_planeado + lote_id para todos
        resumenes = (ResumenTurnoOee.objects
                     .values('id', 'fecha', 'turno', 'linea', 'tiempo_planeado', 'lote_id'))
        resumen_map = {r['id']: r for r in resumenes}

        # Totales de detenciones por resumen
        tot_det_por_resumen = {}
        for r in qs:
            rid = r['lote__resumenes_turno__id']
            tot_det_por_resumen[rid] = tot_det_por_resumen.get(rid, 0) + (r['duracion_total'] or 0)

        salida = []

        # Por motivo (duracion_motivo / tiempo_planeado)
        for r in qs:
            rid = r['lote__resumenes_turno__id']
            res = resumen_map.get(rid)
            if not res:
                continue
            tp = res['tiempo_planeado'] or 1
            porcentaje = round(100 * (r['duracion_total'] or 0) / tp, 2)
            salida.append({
                'fecha': res['fecha'],
                'turno': res['turno'],
                'linea': res['linea'],
                'motivo': r['motivo'],
                'porcentaje': porcentaje,
                'lote_id': r['lote_id'],  # 👈 ahora sí siempre va
            })

        # Tiempo Productivo (resto)
        for rid, det in tot_det_por_resumen.items():
            res = resumen_map.get(rid)
            if not res:
                continue
            tp = res['tiempo_planeado'] or 1
            restante = max(tp - det, 0)
            porcentaje_restante = round(100 * restante / tp, 2)
            salida.append({
                'fecha': res['fecha'],
                'turno': res['turno'],
                'linea': res['linea'],
                'motivo': 'Tiempo Productivo',
                'porcentaje': porcentaje_restante,
                'lote_id': res['lote_id'],  # 👈 también aquí
            })

        return JsonResponse(salida, safe=False, json_dumps_params={'ensure_ascii': False})

    except Exception as e:
        return HttpResponseBadRequest(f"error_api_detenciones: {e}")
    
@login_required
def graficos_detencion(request):
    return render(request, 'calculo_oee/graficos_detencion.html')