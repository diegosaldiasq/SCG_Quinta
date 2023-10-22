from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioPcc2DetectorMetales
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def pcc2_detector_metales(request):
    return render(request, 'pcc2_detector_metales/r_pcc2_detector_metales.html')

@login_required
def vista_pcc2_detector_metales(request):
    if request.method == 'POST':
        nombre_tecnologo = request.user.nombre_completo
        fecha_registro = timezone.make_aware(datetime.strptime(request.POST.get('fecha_registro'), '%Y-%m-%dT%H:%M'), timezone=timezone.utc)
        lote = request.POST.get('lote')
        turno = request.POST.get('turno')
        tipo_metal = request.POST.get('tipo_metal')
        medicion = request.POST.get('medicion')
        producto = request.POST.get('producto')
        observaciones = request.POST.get('observaciones')
        accion_correctiva = request.POST.get('accion_correctiva')

        datos = DatosFormularioPcc2DetectorMetales(
            nombre_tecnologo=nombre_tecnologo, 
            fecha_registro=fecha_registro,
            lote=lote,
            turno=turno,
            tipo_metal=tipo_metal,
            medicion=medicion,
            producto=producto,
            observaciones=observaciones,
            accion_correctiva=accion_correctiva
            )
        datos.save()

        return JsonResponse({'mensaje': 'Datos guardados exitosamente'})

@login_required
def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)