from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioControlParametrosGorreri
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@login_required
def control_parametros_gorreri(request):
    return render(request, 'control_parametros_gorreri/r_control_parametros_gorreri.html')

@csrf_exempt
@login_required 
def vista_control_parametros_gorreri(request):
     if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        dato = data.get('dato', None)
        if dato:
            nombre_tecnologo = request.user.nombre_completo
            fecha_registro = timezone.now()
            cliente = dato.get('cliente')
            codigo_producto = dato.get('codigo_producto')
            producto = dato.get('producto')
            numero_tm = dato.get('numero_tm')
            velocidad_bomba = dato.get('velocidad_bomba')
            velocidad_turbo = dato.get('velocidad_turbo')
            contrapresion = dato.get('contrapresion')
            inyeccion_de_aire = dato.get('inyeccion_de_aire')
            densidad = dato.get('densidad')
            t_final = dato.get('t_final')
            lote = dato.get('lote')
            turno = dato.get('turno')

            datos = DatosFormularioControlParametrosGorreri(
                nombre_tecnologo=nombre_tecnologo,
                fecha_registro=fecha_registro,
                cliente=cliente,
                codigo_producto=codigo_producto,
                producto=producto,
                numero_tm=numero_tm,
                velocidad_bomba=velocidad_bomba,
                velocidad_turbo=velocidad_turbo,
                contrapresion=contrapresion,
                inyeccion_de_aire=inyeccion_de_aire,
                densidad=densidad,
                t_final=t_final,
                lote=lote,
                turno=turno
                )
            datos.save()

            return JsonResponse({'existe': True})
        else:
            return JsonResponse({'existe': False})

@login_required
def redireccionar_selecciones_2(request):
    url_selecciones = reverse('vista_selecciones_2')
    return HttpResponseRedirect(url_selecciones)