from django.shortcuts import render, redirect
from .forms import TurnoOEEForm
from .models import TurnoOEE, Detencion, Reproceso, ResumenTurnoOee
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

# Create your views here.

@csrf_exempt
@login_required
def crear_turno(request):
    if request.method == 'POST':
        form = TurnoOEEForm(request.POST)
        if form.is_valid():
            turno = form.save()

            # Guardar detenciones
            motivos   = request.POST.getlist('motivo_det[]')
            inicios   = request.POST.getlist('hora_inicio_det[]')
            finales   = request.POST.getlist('hora_fin_det[]')

            from datetime import datetime, timedelta
            for mot, hi, hf in zip(motivos, inicios, finales):
                fmt = "%H:%M"
                t1 = datetime.strptime(hi, fmt)
                t2 = datetime.strptime(hf, fmt)
                # si pasa de medianoche
                if t2 < t1:
                    t2 += timedelta(days=1)
                dur = int((t2 - t1).total_seconds() // 60)
                Detencion.objects.create(
                    turno=turno,
                    motivo=mot,
                    duracion=dur
                )

            # Guardar reprocesos
            motivos_rep = request.POST.getlist('motivo_rep[]')
            cantidades_rep = request.POST.getlist('cantidad_rep[]')
            for motivo, cantidad in zip(motivos_rep, cantidades_rep):
                Reproceso.objects.create(turno=turno, motivo=motivo, cantidad=int(cantidad))

            return redirect('lista_turnos')  # Redirige al listado

    else:
        form = TurnoOEEForm()

    return render(request, 'calculo_oee/crear_turno.html', {'form': form})


@login_required
def resumen_turno(request, turno_id):
    turno = get_object_or_404(TurnoOEE, id=turno_id)

    # Evitar duplicados en ResumenTurnoOee
    if not ResumenTurnoOee.objects.filter(turno=turno).exists():
        fecha = turno.fecha

        tiempo_paro = sum(d.duracion for d in turno.detenciones.all())
        productos_malos = sum(r.cantidad for r in turno.reprocesos.all())

        tiempo_operativo = turno.tiempo_planeado - tiempo_paro
        tasa_nominal = turno.produccion_planeada / turno.tiempo_planeado if turno.tiempo_planeado else 0
        produccion_teorica = tiempo_operativo * tasa_nominal

        produccion_real = turno.produccion_real or 0
        productos_buenos = produccion_real - productos_malos

        disponibilidad = tiempo_operativo / turno.tiempo_planeado if turno.tiempo_planeado else 0
        rendimiento = produccion_real / produccion_teorica if produccion_teorica else 0
        calidad = productos_buenos / produccion_real if produccion_real else 0
        oee = disponibilidad * rendimiento * calidad * 100  # en %

        ResumenTurnoOee.objects.create(
            fecha=fecha,
            turno=turno,
            cliente=turno.cliente,
            codigo=turno.codigo,
            producto=turno.producto,
            linea=turno.linea,
            tiempo_paro=tiempo_paro,
            tiempo_planeado=turno.tiempo_planeado,
            produccion_teorica=round(produccion_teorica),
            produccion_real=produccion_real,
            productos_malos=productos_malos,
            productos_buenos=productos_buenos,
            eficiencia=round(rendimiento * 100, 2),
            disponibilidad=round(disponibilidad * 100, 2),
            calidad=round(calidad * 100, 2),
            oee=round(oee, 2)
        )

    resumen = ResumenTurnoOee.objects.get(turno=turno)

    return render(request, 'calculo_oee/resumen_turno.html', {'resumen': resumen})

@csrf_exempt
@login_required
def cerrar_turno(request, turno_id):
    turno = get_object_or_404(TurnoOEE, id=turno_id)

    if request.method == 'POST':
        form = ProduccionRealForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            return redirect('resumen_turno', turno_id=turno.id)
    else:
        form = ProduccionRealForm(instance=turno)

    return render(request, 'calculo_oee/cerrar_turno.html', {'form': form, 'turno': turno})

@login_required
def lista_turnos(request):
    turnos = TurnoOEE.objects.all().order_by('-fecha', '-hora_inicio')

    # filtros
    fecha = request.GET.get('fecha')
    linea = request.GET.get('linea')
    cliente = request.GET.get('cliente')
    producto = request.GET.get('producto')

    if fecha:
        turnos = turnos.filter(fecha__date=parse_date(fecha))
    if linea:
        turnos = turnos.filter(linea__icontains=linea)
    if cliente:
        turnos = turnos.filter(cliente__icontains=cliente)
    if producto:
        turnos = turnos.filter(producto__icontains=producto)

    # paginación
    paginator = Paginator(turnos, 10)
    page_number = request.GET.get('page')
    turnos_pag = paginator.get_page(page_number)

    return render(request, 'calculo_oee/lista_turnos.html', {
        'turnos': turnos_pag,
        'filtro_fecha': fecha,
        'filtro_linea': linea,
        'filtro_cliente': cliente,
        'filtro_producto': producto,
    })

@login_required
def detalle_turno(request, turno_id):
    turno = get_object_or_404(TurnoOEE, id=turno_id)
    detenciones = turno.detenciones.all()
    reprocesos = turno.reprocesos.all()
    return render(request, 'calculo_oee/detalle_turno.html', {
        'turno': turno,
        'detenciones': detenciones,
        'reprocesos': reprocesos
    })

@csrf_exempt
@login_required
def marcar_verificado(request, turno_id):
    if request.method == 'POST':
        resumen = get_object_or_404(ResumenTurnoOee, turno_id=turno_id)
        resumen.verificado = True
        resumen.verificado_por = request.user.username
        resumen.fecha_de_verificacion = timezone.now()
        resumen.save()
        return redirect('resumen_turno', turno_id=turno_id)
    
@login_required
def redireccionar_intermedio(request):
    url_inicio = reverse('intermedio')
    return HttpResponseRedirect(url_inicio)
