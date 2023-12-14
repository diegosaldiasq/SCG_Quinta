from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioControlMaterialExtraño
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
import json

# Create your views here.

@login_required
def control_material_extraño(request):
    return render(request, 'control_material_extraño/r_control_material_extraño.html')

@login_required
def vista_control_material_extraño(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        dato = data.get('dato', None)
        if dato:
            nombre_tecnologo = request.user.nombre_completo
            fecha_registro = timezone.now()
            turno = dato.get('turno')
            area_material = dato.get('area_material')
            tipo_material = dato.get('tipo_material')
            accion_correctiva = dato.get('accion_correctiva')
            verificacion_accion_correctiva = dato.get('verificacion_accion_correctiva')
            observaciones = dato.get('observaciones')


            datos = DatosFormularioControlMaterialExtraño(
                nombre_tecnologo=nombre_tecnologo, 
                fecha_registro=fecha_registro,
                turno=turno,
                area_material=area_material,
                tipo_material=tipo_material,
                accion_correctiva=accion_correctiva,
                verificacion_accion_correctiva=verificacion_accion_correctiva,
                observaciones=observaciones
                )
            datos.save()

            return JsonResponse({'existe': True})
        else:
            return JsonResponse({'existe': False})

@login_required
def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)