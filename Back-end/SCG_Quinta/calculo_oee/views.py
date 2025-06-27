from django.shortcuts import render, redirect
from .forms import TurnoOEEForm
from .models import TurnoOEE, Detencion, Reproceso
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .forms import ProduccionRealForm
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator


# Create your views here.

@login_required
#@csrf_exempt
def crear_turno(request):
    if request.method == 'POST':
        form = TurnoOEEForm(request.POST)
        if form.is_valid():
            turno = form.save()

            # Guardar detenciones
            motivos_det = request.POST.getlist('motivo_det[]')
            duraciones_det = request.POST.getlist('duracion_det[]')
            for motivo, duracion in zip(motivos_det, duraciones_det):
                Detencion.objects.create(turno=turno, motivo=motivo, duracion=int(duracion))

            # Guardar reprocesos
            motivos_rep = request.POST.getlist('motivo_rep[]')
            cantidades_rep = request.POST.getlist('cantidad_rep[]')
            for motivo, cantidad in zip(motivos_rep, cantidades_rep):
                Reproceso.objects.create(turno=turno, motivo=motivo, cantidad=int(cantidad))

            return render(request, 'calculo_oee/cerrar_turno.html') # Redirige a una vista de éxito

    else:
        form = TurnoOEEForm()

    return render(request, 'calculo_oee/crear_turno.html', {'form': form})

@login_required
def resumen_turno(request, turno_id):
    turno = get_object_or_404(TurnoOEE, id=turno_id)

    fecha = turno.fecha
    cliente = turno.cliente
    codigo = turno.codigo
    producto = turno.producto
    linea = turno.linea

    # Detenciones asociadas (usamos el related_name 'detenciones')
    tiempo_paro = sum(d.duracion for d in turno.detenciones.all())

    # Reprocesos asociados (usamos el related_name 'reprocesos')
    productos_malos = sum(r.cantidad for r in turno.reprocesos.all())

    tiempo_operativo = turno.tiempo_planeado - tiempo_paro

    # Tasa de producción nominal (puedes personalizar esto o almacenarlo en el modelo si es variable)
    tasa_nominal = turno.produccion_planeada / turno.tiempo_planeado if turno.tiempo_planeado else 0
    produccion_teorica = tiempo_operativo * tasa_nominal

    # Producción real desde el modelo
    produccion_real = turno.produccion_real or 0
    productos_buenos = produccion_real - productos_malos

    # Cálculos OEE
    disponibilidad = tiempo_operativo / turno.tiempo_planeado if turno.tiempo_planeado else 0
    rendimiento = produccion_real / produccion_teorica if produccion_teorica else 0
    calidad = productos_buenos / produccion_real if produccion_real else 0
    oee = disponibilidad * rendimiento * calidad * 100  # en %

    contexto = {
        'fecha': fecha,
        'cliente': cliente,
        'codigo': codigo,
        'producto': producto,
        'linea': linea,
        'turno': turno,
        'disponibilidad': round(disponibilidad * 100, 2),
        'rendimiento': round(rendimiento * 100, 2),
        'calidad': round(calidad * 100, 2),
        'oee': round(oee, 2),
        'tiempo_paro': tiempo_paro,
        'productos_malos': productos_malos,
        'produccion_teorica': round(produccion_teorica),
        'produccion_real': produccion_real,
        'productos_buenos': productos_buenos,
    }

    return render(request, 'calculo_oee/resumen_turno.html', contexto)

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
    if fecha:
        turnos_queryset = turnos_queryset.filter(fecha=parse_date(fecha))
    if linea:
        turnos_queryset = turnos_queryset.filter(linea__icontains=linea)

    # paginación
    paginator = Paginator(turnos_queryset, 10)  # 10 por página
    page_number = request.GET.get('page')
    turnos = paginator.get_page(page_number)

    return render(request, 'lista_turnos.html', {
        'turnos': turnos,
        'filtro_fecha': fecha,
        'filtro_linea': linea
    })
