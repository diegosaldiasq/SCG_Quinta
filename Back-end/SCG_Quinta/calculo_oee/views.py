from django.shortcuts import render, redirect
from .forms import TurnoOEEForm
from .models import TurnoOEE, Detencion, Reproceso
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .forms import ProduccionRealForm

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

            return redirect('turno_exito')

    else:
        form = TurnoOEEForm()

    return render(request, 'crear_turno.html', {'form': form})

def resumen_turno(request, turno_id):
    turno = get_object_or_404(TurnoOEE, id=turno_id)

    tiempo_paro = sum(d.duracion for d in turno.detenciones.all())
    productos_malos = sum(r.cantidad for r in turno.reprocesos.all())

    tiempo_operativo = turno.tiempo_planeado - tiempo_paro
    tasa_nominal = 2  # <-- ajusta esto según tu línea (ej: 2 unidades/min)
    produccion_teorica = tiempo_operativo * tasa_nominal

    # ⚠️ En esta demo no tenemos producción_real registrada aún.
    # Supongamos que el operador la ingresa manualmente después.
    produccion_real = produccion_teorica  # puedes ajustarlo en modelo o plantilla
    productos_buenos = produccion_real - productos_malos

    disponibilidad = tiempo_operativo / turno.tiempo_planeado if turno.tiempo_planeado else 0
    rendimiento = produccion_real / produccion_teorica if produccion_teorica else 0
    calidad = productos_buenos / produccion_real if produccion_real else 0
    oee = disponibilidad * rendimiento * calidad * 100  # en %

    contexto = {
        'turno': turno,
        'disponibilidad': round(disponibilidad * 100, 2),
        'rendimiento': round(rendimiento * 100, 2),
        'calidad': round(calidad * 100, 2),
        'oee': round(oee, 2),
        'tiempo_paro': tiempo_paro,
        'productos_malos': productos_malos,
        'produccion_teorica': produccion_teorica,
        'produccion_real': produccion_real,
        'productos_buenos': productos_buenos,
    }
    return render(request, 'resumen_turno.html', contexto)

def cerrar_turno(request, turno_id):
    turno = get_object_or_404(TurnoOEE, id=turno_id)

    if request.method == 'POST':
        form = ProduccionRealForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            return redirect('resumen_turno', turno_id=turno.id)
    else:
        form = ProduccionRealForm(instance=turno)

    return render(request, 'cerrar_turno.html', {'form': form, 'turno': turno})
