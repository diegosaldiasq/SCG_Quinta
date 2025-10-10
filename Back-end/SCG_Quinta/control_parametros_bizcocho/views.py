from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioControlParametrosBizcocho
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@login_required
def control_parametros_bizcocho(request):
    return render(request, 'control_parametros_bizcocho/r_control_parametros_bizcocho.html')    

@csrf_exempt
@login_required 
def vista_control_parametros_bizcocho(request): 
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            dato = data.get('dato', None)
            if dato:
                try:
                    nombre_tecnologo = request.user.nombre_completo
                    fecha_registro = timezone.now()
                    proveedor = dato.get('proveedor')
                    producto = dato.get('producto')
                    cantidad_agua = float(dato.get('cantidad_agua'))
                    cantidad_huevo = float(dato.get('cantidad_huevo'))
                    velocidad_bomba = int(dato.get('velocidad_bomba'))
                    velocidad_turbo = int(dato.get('velocidad_turbo'))
                    contrapresion = float(dato.get('contrapresion'))
                    contrapresion_trasera = float(dato.get('contrapresion_trasera'))
                    inyeccion_de_aire = int(dato.get('inyeccion_de_aire'))
                    densidad = float(dato.get('densidad'))
                    t_final = float(dato.get('t_final'))
                    lote = dato.get('lote')
                    turno = dato.get('turno')
    
                    datos = DatosFormularioControlParametrosBizcocho(
                        nombre_tecnologo=nombre_tecnologo,
                        fecha_registro=fecha_registro,
                        proveedor=proveedor,
                        producto=producto,
                        cantidad_agua=cantidad_agua,
                        cantidad_huevo=cantidad_huevo,
                        velocidad_bomba=velocidad_bomba,
                        velocidad_turbo=velocidad_turbo,
                        contrapresion=contrapresion,
                        contrapresion_trasera=contrapresion_trasera,
                        inyeccion_de_aire=inyeccion_de_aire,
                        densidad=densidad,
                        t_final=t_final,
                        lote=lote,
                        turno=turno
                        )
                    datos.save()
    
                    return JsonResponse({'existe': True})   
                except Exception as e:
                    return JsonResponse({'existe': False, 'error': str(e)}) 

            else:
                return JsonResponse({'existe': False, 'error': 'No se recibieron datos.'})
        else:
            return JsonResponse({'existe': False, 'error': 'Método no permitido.'})     
        
@login_required
def redireccionar_selecciones_3(request):
    return HttpResponseRedirect(reverse('selecciones'))     

