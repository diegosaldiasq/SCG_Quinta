from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def vista_selecciones(request):
    return render(request, 'selecciones/selecciones.html')

def redireccionar_historial_termometro(request):
    url_historial_termometro = reverse('historial_termometro')
    return HttpResponseRedirect(url_historial_termometro)

def redireccionar_inicio(request):
    url_inicio = reverse('index')
    return HttpResponseRedirect(url_inicio)

def redireccionar_monitoreo_del_agua(request):
    url_monitoreo_del_agua = reverse('monitoreo_del_agua')
    return HttpResponseRedirect(url_monitoreo_del_agua)

def redireccionar_monitoreo_de_plagas(request):
    url_monitoreo_de_plagas = reverse('monitoreo_de_plagas')
    return HttpResponseRedirect(url_monitoreo_de_plagas)

