from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
    #return HttpResponse("Hello World!!")
    return render(request, 'inicio/index.html')

def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)

def redireccionar_main(request):
    url_main = reverse('main')
    return HttpResponseRedirect(url_main)
