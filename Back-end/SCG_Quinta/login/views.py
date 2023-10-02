from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.


def main(request):
    return render(request, 'login/main.html')

def ingresa_rut(request):
    return render(request, 'login/ingresa_rut.html')
