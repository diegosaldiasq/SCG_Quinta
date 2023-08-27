from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioPcc2DetectorMetales

# Create your views here.

def pcc2_detector_metales(request):
    if request.method == 'POST' and request.is_ajax():
        nombre_tecnologo = request.POST.get('nombre_tecnologo')
        fecha_registro = request.POST.get('fecha_registro')
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