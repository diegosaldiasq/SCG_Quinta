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
    """
    Vista que recibe un POST con JSON:
    {
      "nombreCompleto": "...",
      "perfilUsuario": "...",
      "rut": "...",
      "pasword": "..."
    }
    Verifica que exista un objeto DatosFormularioCrearCuenta con ese RUT,
    chequea la contraseña con el método check_password y, si coincide,
    crea/obtiene un User (tu modelo custom) y hace login(request, user).
    Devuelve {'existe': True/False}.
    """
    if request.method != 'POST':
        return JsonResponse({'existe': False}, status=405)

    # 1) Leer y parsear JSON
    try:
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
    except json.JSONDecodeError:
        # JSON mal formado
        return JsonResponse({'existe': False}, status=400)

    # 2) Extraer campos
    nombre_completo = body_data.get('nombreCompleto', '').strip()
    perfil_usuario  = body_data.get('perfilUsuario', '').strip()
    rut             = body_data.get('rut', '').strip()
    password        = body_data.get('pasword', '')

    # 3) Buscar en tu modelo de datos (antes de crear el User de Django)
    try:
        cuenta = DatosFormularioCrearCuenta.objects.get(rut=rut)
    except DatosFormularioCrearCuenta.DoesNotExist:
        # No existe ninguna cuenta con ese RUT
        return JsonResponse({'existe': False})

    # 4) Verificar contraseña
    if cuenta.check_password(password):
        # Si la contraseña coincide, creamos/obtenemos un usuario usando el User swapped
        try:
            user_django, creado = User.objects.get_or_create(
                username=rut,
                defaults={
                    'nombre_completo': cuenta.nombre_completo
                    # Si tu modelo custom (DatosFormularioCrearCuenta) tiene campos adicionales
                    # que sean required, podrías pasarlos aquí en defaults.
                }
            )
        except Exception as exc:
            # Por ejemplo, si tu modelo User swapped requiere otros campos obligatorios,
            # aquí se podría producir un error. Maneja según convenga.
            return JsonResponse({'existe': False, 'error': 'No se pudo crear/obtener usuario'}, status=500)

        # Forzar el backend para login (si no usas authenticate())
        user_django.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user_django)
        return JsonResponse({'existe': True})
    else:
        return JsonResponse({'existe': False})

def ingresa_rut(request):
    return render(request, 'login/Ingresa_rut.html')

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