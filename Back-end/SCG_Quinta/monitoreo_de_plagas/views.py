from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioMonitoreoDePlagas
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def monitoreo_de_plagas(request):
    return render(request, 'monitoreo_de_plagas/r_monitoreo_de_plagas.html')

def vista_monitoreo_de_plagas(request):
    if request.method == 'POST' and request.is_ajax():
        nombre_tecnologo = request.POST.get('nombre_tecnologo')
        fecha_registro = request.POST.get('fecha_registro')
        numero_estacion = request.POST.get('numero_estacion')
        tipo_plaga = request.POST.get('tipo_plaga')
        tipo_trampa = request.POST.get('tipo_trampa')
        ubicacion = request.POST.get('ubicacion')
        monitoreo = request.POST.get('monitoreo')
        accion_correctiva = request.POST.get('accion_correctiva')


        datos = DatosFormularioMonitoreoDePlagas(
            nombre_tecnologo=nombre_tecnologo, 
            fecha_registro=fecha_registro,
            numero_estacion=numero_estacion,
            tipo_plaga=tipo_plaga,
            tipo_trampa=tipo_trampa,
            ubicacion=ubicacion,
            monitoreo=monitoreo,
            accion_correctiva=accion_correctiva
            )
        datos.save()

        return JsonResponse({'mensaje': 'Datos guardados exitosamente'})