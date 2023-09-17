from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioInformeDeIncidentes
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def informe_de_incidentes(request):
    return render(request, 'informe_de_incidentes/r_informe_de_incidentes.html')

def vista_informe_de_incidentes(request):
    if request.method == 'POST' and request.is_ajax():
        nombre_tecnologo = request.POST.get('nombre_tecnologo')
        fecha_registro = request.POST.get('fecha_registro')
        fuente_material = request.POST.get('fuente_material')
        cantidad_contaminada = request.POST.get('cantidad_contaminada')
        unidad_de_medida = request.POST.get('unidad_de_medida')
        lote_producto_contaminado = request.POST.get('lote_producto_contaminado')
        observaciones = request.POST.get('observaciones')
        analisis_causa = request.POST.get('analisis_causa')
        accion_correctiva = request.POST.get('accion_correctiva')


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

        return JsonResponse({'mensaje': 'Datos guardados exitosamente'})

def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)