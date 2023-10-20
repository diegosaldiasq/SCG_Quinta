from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    #return HttpResponse("Hello World!!")
    return render(request, 'inicio/index.html')

@login_required
def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)

@login_required
def redireccionar_main(request):
    url_main = reverse('main')
    return HttpResponseRedirect(url_main)
