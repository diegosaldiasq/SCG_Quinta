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

# Create your views here.

@csrf_exempt
@login_required
def crear_turno(request):
    if request.method == 'POST':
        form = TurnoOEEForm(request.POST)
        if form.is_valid():
            lote = form.save()

            # Guardar productos
            cliente = lote.POST.get('cliente[]', '')
            productos = request.POST.getlist('producto[]')
            codigos = request.POST.getlist('codigo[]')
            planeadas = request.POST.getlist('produccion_planeada[]')
            reales = request.POST.getlist('produccion_real[]')  # si ya se ingresan
            comentarios = request.POST.getlist('comentarios[]')  # <-- nuevo campo

            for cli, prod, cod, plan, real, com in zip(cliente, productos, codigos, planeadas, reales, comentarios):
                Producto.objects.create(
                    lote=lote,
                    cliente=cli,
                    producto=prod,
                    codigo=cod,
                    produccion_planeada=int(plan) if plan else None,
                    produccion_real=int(real) if real else None,
                    comentarios=com.strip() if com else None  # <-- nuevo campo 
                )

            # Guardar detenciones
            motivos   = request.POST.getlist('motivo_det[]')
            inicios   = request.POST.getlist('hora_inicio_det[]')
            finales   = request.POST.getlist('hora_fin_det[]')
            comentarios = request.POST.getlist('comentarios_det[]')  # <-- nuevo campo

            from datetime import datetime, timedelta
            fmt = "%H:%M"
            for mot, hi, hf, com in zip(motivos, inicios, finales, comentarios):
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
            for motivo, cantidad in zip(motivos_rep, cantidades_rep):
                Reproceso.objects.create(lote=lote, motivo=motivo, cantidad=int(cantidad))

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

        tiempo_paro = sum(d.duracion for d in lote.detenciones.all())
        productos_malos = sum(r.cantidad for r in lote.reprocesos.all())

        tiempo_operativo = lote.tiempo_planeado - tiempo_paro
        clave = (lote.producto, lote.codigo)
        tasa_nominal = TASA_NOMINAL_POR_PRODUCTO.get(clave, TASA_NOMINAL_DEFECTO) # valores en constants.py
        num_personas = lote.numero_personas or 0
        produccion_teorica = tasa_nominal * num_personas

        produccion_real = lote.produccion_real or 0
        productos_buenos = produccion_real - productos_malos

        disponibilidad = tiempo_operativo / lote.tiempo_planeado if lote.tiempo_planeado else 0
        rendimiento = produccion_real / produccion_teorica if produccion_teorica else 0
        calidad = productos_buenos / produccion_real if produccion_real else 0
        oee = disponibilidad * rendimiento * calidad * 100  # en %

        ResumenTurnoOee.objects.create(
            fecha=fecha,
            turno=turno,
            supervisor=supervisor,
            lote=lote,
            cliente=lote.cliente,
            codigo=lote.codigo,
            producto=lote.producto,
            linea=lote.linea,
            tiempo_paro=tiempo_paro,
            tiempo_planeado=lote.tiempo_planeado,
            produccion_teorica=round(produccion_teorica),
            produccion_planificada=lote.produccion_planeada,
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
        # decode para que vuelva como estaba
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

    # --- 2. Obtener valores únicos para los desplegables ---
    lineas    = TurnoOEE.objects.values_list('linea', flat=True).distinct()
    clientes  = TurnoOEE.objects.values_list('cliente', flat=True).distinct()
    productos = TurnoOEE.objects.values_list('producto', flat=True).distinct()
    turnos   = TurnoOEE.objects.values_list('turno', flat=True).distinct()

    # --- 3. Paginación ---
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
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            resumen = get_object_or_404(ResumenTurnoOee, lote_id=lote_id)
            resumen.verificado = True
            resumen.verificado_por = request.user.nombre_completo
            resumen.fecha_de_verificacion = timezone.now()
            resumen.save()
    base = reverse('resumen_turno', args=[lote_id])
    if next_param:
        return redirect(f"{base}?next={next_param}")
    return redirect(base)
    
@login_required
def redireccionar_intermedio(request):
    url_inicio = reverse('intermedio')
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
