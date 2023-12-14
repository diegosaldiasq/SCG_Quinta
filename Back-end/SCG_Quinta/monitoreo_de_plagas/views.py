from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioMonitoreoDePlagas
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import json

# Create your views here.

@login_required
def monitoreo_de_plagas(request):
    return render(request, 'monitoreo_de_plagas/r_monitoreo_de_plagas.html')

@login_required
def vista_monitoreo_de_plagas(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        dato = data.get('dato', None)
        if dato:
            nombre_tecnologo = request.user.nombre_completo
            fecha_registro = timezone.now()
            numero_estacion = dato.get('numero_estacion')
            tipo_plaga = dato.get('tipo_plaga')
            tipo_trampa = dato.get('tipo_trampa')
            ubicacion = dato.get('ubicacion')
            monitoreo = dato.get('monitoreo')
            accion_correctiva = dato.get('accion_correctiva')


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

            return JsonResponse({'existe': True})
        else:
            return JsonResponse({'existe': False})

@login_required
def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)
