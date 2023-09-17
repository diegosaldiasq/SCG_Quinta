from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioControlMaterialExtraño
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def control_material_extraño(request):
    return render(request, 'control_material_extraño/r_control_material_extraño.html')

def vista_control_material_extraño(request):
    if request.method == 'POST' and request.is_ajax():
        nombre_tecnologo = request.POST.get('nombre_tecnologo')
        fecha_registro = request.POST.get('fecha_registro')
        turno = request.POST.get('turno')
        area_material = request.POST.get('area_material')
        tipo_material = request.POST.get('tipo_material')
        accion_correctiva = request.POST.get('accion_correctiva')
        verificacion_accion_correctiva = request.POST.get('verificacion_accion_correctiva')
        observaciones = request.POST.get('observaciones')


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

        return JsonResponse({'mensaje': 'Datos guardados exitosamente'})

def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)