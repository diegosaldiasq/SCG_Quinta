from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioHistorialTermometro
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
import json

# Create your views here.

@login_required
def historial_termometro(request):
    return render(request, 'historial_termometro/r_historial_termometro.html')

@login_required
def vista_historial_termometro(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        dato = data.get('dato', None)
        if dato:
            nombre_tecnologo = request.user.nombre_completo
            fecha_registro = timezone.now()
            codigo_termometro = dato.get('codigo_termometro')
            valor_1 = dato.get('valor_1')
            valor_2 = dato.get('valor_2')
            valor_3 = dato.get('valor_3')
            valor_4 = dato.get('valor_4')
            valor_5 = dato.get('valor_5')
            promedio_prueba = dato.get('promedio_prueba')
            valor_6 = dato.get('valor_6')
            valor_7 = dato.get('valor_7')
            valor_8 = dato.get('valor_8')
            valor_9 = dato.get('valor_9')
            valor_10 = dato.get('valor_10')
            promedio_patron = dato.get('promedio_patron')   
            factor_anual = dato.get('factor_anual')
            promedio_termometros = dato.get('promedio_termometros')
            nivel_aceptacion = dato.get('nivel_aceptacion')
            cumplimiento = dato.get('cumplimiento')     
            accion_correctiva = dato.get('accion_correctiva')
            verificacion_accion_correctiva = dato.get('verificacion_accion_correctiva')


            datos = DatosFormularioHistorialTermometro(
                nombre_tecnologo=nombre_tecnologo, 
                fecha_registro=fecha_registro,
                codigo_termometro=codigo_termometro,
                valor_1=valor_1,
                valor_2=valor_2,
                valor_3=valor_3,
                valor_4=valor_4,
                valor_5=valor_5,
                promedio_prueba=promedio_prueba,
                valor_6=valor_6,
                valor_7=valor_7,
                valor_8=valor_8,
                valor_9=valor_9,
                valor_10=valor_10,
                promedio_patron=promedio_patron,
                factor_anual=factor_anual,
                promedio_termometros=promedio_termometros,
                nivel_aceptacion=nivel_aceptacion,
                cumplimiento=cumplimiento,
                accion_correctiva=accion_correctiva,
                verificacion_accion_correctiva=verificacion_accion_correctiva
                )
            datos.save()

            return JsonResponse({'existe': True})
        else:
            return JsonResponse({'existe': False})

@login_required  
def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)



