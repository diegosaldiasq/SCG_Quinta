from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import DatosFormularioCrearCuenta
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
import json, traceback, logging
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def main(request):
    logout(request)
    return render(request, 'login/main.html')

User = get_user_model()

@csrf_exempt
def vista_main(request):
    if request.method != 'POST':
        return JsonResponse({'existe': False}, status=405)

    try:
        body_data = json.loads(request.body.decode('utf-8'))
        nombre_completo = body_data.get('nombreCompleto', '').strip()
        perfil_usuario = body_data.get('perfilUsuario', '').strip()
        rut = body_data.get('rut', '').strip()
        password = body_data.get('pasword', '')
    except json.JSONDecodeError:
        return JsonResponse({'existe': False}, status=400)

    # Autenticar usando el backend de Django
    user = authenticate(request, username=nombre_completo, perfil_usuario=perfil_usuario, rut=rut, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'existe': True})
    else:
        return JsonResponse({'existe': False}, status=401)

def ingresa_rut(request):
    return render(request, 'login/Ingresa_rut.html')

def crear_cuenta(request):
    return render(request, 'login/crear_cuenta.html')

@csrf_exempt
def vista_crear_cuenta(request):
    if request.method == 'POST':
        nombre_completo = request.POST.get('nombre_completo')
        perfil_usuario = request.POST.get('perfil_usuario')
        rut = request.POST.get('rut')
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')

        if password != new_password:
            messages.error(request, "Las contraseñas no coinciden")

        if DatosFormularioCrearCuenta.objects.filter(rut=rut).exists():
            messages.error(request, "El RUT ya está registrado")
            return redirect('crear_cuenta')

        datos = DatosFormularioCrearCuenta(
            nombre_completo=nombre_completo, 
            perfil_usuario=perfil_usuario,
            rut=rut,
            new_password=new_password,
            fecha_creacion=timezone.now()
            )
        datos.set_password(password)
        datos.save()

        return HttpResponse("Datos guardados exitosamente")
        
def cuenta_creada(request):
    return render(request, 'login/cuenta_creada.html')

@csrf_exempt
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

@csrf_exempt
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
        
        #data = DatosFormularioCrearCuenta.objects.filter(password=nueva_contraseña).exists()
        return JsonResponse({'existe': True})
    else:
        return JsonResponse({'existe': False}, status=405)  

def pasword_creado(request):
    return render(request, 'login/pasword_creado.html')