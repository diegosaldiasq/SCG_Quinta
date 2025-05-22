from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import DatosFormularioCrearCuenta
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
import json
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def main(request):
    logout(request)
    return render(request, 'login/main.html')

def vista_main(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        nombre_completo = body_data.get('nombreCompleto')
        perfil_recibido = body_data.get('perfilUsuario')
        rut_recibido = body_data.get('rut')
        password = body_data.get('pasword')

        usuario = authenticate(request, username=nombre_completo, password=password)
        dato = None
        if usuario is not None:
            dato = True
            login(request, usuario)
        else:
            dato = False
        return JsonResponse({'existe': dato})

def ingresa_rut(request):
    return render(request, 'login/Ingresa_rut.html')

def crear_cuenta(request):
    return render(request, 'login/crear_cuenta.html')

def vista_crear_cuenta(request):
    if request.method == 'POST':
        if request.method != 'POST':
            return JsonResponse({'error': 'Método no permitido'}, status=405)

        # Si mandas form-urlencoded:
        nombre_completo = request.POST.get('nombre_completo')
        perfil_usuario = request.POST.get('perfil_usuario')
        rut = request.POST.get('rut')
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')

        # 1) Validar contraseñas
        if password != new_password:
            return JsonResponse({'error': 'Las contraseñas no coinciden'}, status=400)

        # 2) Validar existencia de RUT
        if DatosFormularioCrearCuenta.objects.filter(rut=rut).exists():
            return JsonResponse({'error': 'El RUT ya está registrado'}, status=400)

        # 3) Validar existencia de username (o email, según tu campo)
        #    Suponiendo que el campo usuario sea el nombre_completo o username separado:
        if DatosFormularioCrearCuenta.objects.filter(username=nombre_completo).exists():
            return JsonResponse({'error': 'El nombre de usuario ya existe'}, status=400)

        # 4) Si todo OK, guardamos
        datos = DatosFormularioCrearCuenta(
            nombre_completo=nombre_completo,
            perfil_usuario=perfil_usuario,
            rut=rut,
            new_password=new_password
        )
        datos.set_password(password)
        datos.save()

        return JsonResponse({'mensaje': 'Datos guardados exitosamente'}, status=200)
        
def cuenta_creada(request):
    return render(request, 'login/cuenta_creada.html')

def vista_ingresa_rut(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        rut_recibido = body_data.get('dato')

        data = DatosFormularioCrearCuenta.objects.filter(rut=rut_recibido).exists()
        if data == True:
            request.session['rut'] = rut_recibido
        return JsonResponse({'existe': data})

def pasword(request):
    return render(request, 'login/pasword.html')

def vista_pasword(request):
    rut_temporal_recibido = request.session.get('rut', default=None)
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        nueva_contraseña = body_data.get('dato')
        usuario = DatosFormularioCrearCuenta.objects.get(rut=rut_temporal_recibido)
        usuario.set_password(nueva_contraseña)
        usuario.new_password = nueva_contraseña
        usuario.save()
        
        data = DatosFormularioCrearCuenta.objects.filter(password=nueva_contraseña).exists()
        return JsonResponse({'existe': data})

def pasword_creado(request):
    return render(request, 'login/pasword_creado.html')