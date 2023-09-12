from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def vista_selecciones(request):
    return render(request, 'selecciones/selecciones.html')

def redireccionar_historial_termometro(request):
    url_historial_termometro = reverse('historial_termometro')
    return HttpResponseRedirect(url_historial_termometro)

