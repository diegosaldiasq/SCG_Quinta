from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioMonitoreoDePlagas
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def monitoreo_de_plagas(request):
    return render(request, 'monitoreo_de_plagas/r_monitoreo_de_plagas.html')

@login_required
def vista_monitoreo_de_plagas(request):
    if request.method == 'POST':
        nombre_tecnologo = request.user.nombre_completo
        fecha_registro = timezone.make_aware(datetime.strptime(request.POST.get('fecha_registro'), '%Y-%m-%dT%H:%M'), timezone=timezone.utc)
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

@login_required
def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)
