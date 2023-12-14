from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioPcc2DetectorMetales
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import json

# Create your views here.

@login_required
def pcc2_detector_metales(request):
    return render(request, 'pcc2_detector_metales/r_pcc2_detector_metales.html')

@login_required
def vista_pcc2_detector_metales(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        dato = data.get('dato', None)
        if dato:
            nombre_tecnologo = request.user.nombre_completo
            fecha_registro = timezone.now()
            lote = dato.get('lote')
            turno = dato.get('turno')
            tipo_metal = dato.get('tipo_metal')
            medicion = dato.get('medicion')
            producto = dato.get('producto')
            observaciones = dato.get('observaciones')
            accion_correctiva = dato.get('accion_correctiva')

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

            return JsonResponse({'existe': True})
        else:
            return JsonResponse({'existe': False})

@login_required
def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)