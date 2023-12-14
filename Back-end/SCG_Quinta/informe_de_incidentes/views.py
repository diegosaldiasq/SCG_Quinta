from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioInformeDeIncidentes
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
import json

# Create your views here.

@login_required
def informe_de_incidentes(request):
    return render(request, 'informe_de_incidentes/r_informe_de_incidentes.html')

@login_required
def vista_informe_de_incidentes(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        dato = data.get('dato', None)
        if dato:
            nombre_tecnologo = request.user.nombre_completo
            fecha_registro = timezone.now()
            fuente_material = dato.get('fuente_material')
            cantidad_contaminada = dato.get('cantidad_contaminada')
            unidad_de_medida = dato.get('unidad_de_medida')
            lote_producto_contaminado = dato.get('lote_producto_contaminado')
            observaciones = dato.get('observaciones')
            analisis_causa = dato.get('analisis_causa')
            accion_correctiva = dato.get('accion_correctiva')

            datos = DatosFormularioInformeDeIncidentes(
                nombre_tecnologo=nombre_tecnologo, 
                fecha_registro=fecha_registro,
                fuente_material=fuente_material,
                cantidad_contaminada=cantidad_contaminada,
                unidad_de_medida=unidad_de_medida,
                lote_producto_contaminado=lote_producto_contaminado,
                observaciones=observaciones,
                analisis_causa=analisis_causa,
                accion_correctiva=accion_correctiva
                )
            datos.save()

            return JsonResponse({'existe': True})
        else:
            return JsonResponse({'existe': False})

@login_required
def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)