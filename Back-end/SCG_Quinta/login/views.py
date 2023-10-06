from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import DatosFormularioCrearCuenta
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.


def main(request):
    return render(request, 'login/main.html')

def ingresa_rut(request):
    return render(request, 'login/ingresa_rut.html')

def crear_cuenta(request):
    return render(request, 'login/crear_cuenta.html')

def vista_crear_cuenta(request):
    if request.method == 'POST':
        nombre_completo = request.POST.get('nombre_completo')
        perfil_usuario = request.POST.get('perfil_usuario')
        rut = request.POST.get('rut')
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')

        if password != new_password:
            messages.error(request, "Las contraseñas no coinciden")

        datos = DatosFormularioCrearCuenta(
            nombre_completo=nombre_completo, 
            perfil_usuario=perfil_usuario,
            rut=rut,
            password=password,
            new_password=new_password
            )
        datos.save()

        #return render(request, 'login/cuenta_creada.html')
        #return HttpResponse("Datos guardados exitosamente")
        #return redirect('cuenta_creada')
        return HttpResponseRedirect(reverse('cuenta_creada'))
    
    
def cuenta_creada(request):
    return render(request, 'login/cuenta_creada.html')