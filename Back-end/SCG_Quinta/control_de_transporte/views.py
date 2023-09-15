from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioControlDeTransporte
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def control_de_transporte(request):
    return render(request, 'control_de_transporte/r_control_de_transporte.html')


def vista_control_de_transporte(request):
    if request.method == 'POST' and request.is_ajax():
        nombre_tecnologo = request.POST.get('nombre_tecnologo')
        fecha_registro = request.POST.get('fecha_registro')
        fecha_recepcion = request.POST.get('fecha_recepcion')
        producto_recepcion = request.POST.get('producto_recepcion')
        temperatura_transporte = request.POST.get('temperatura_transporte')
        temperatura_producto = request.POST.get('temperatura_producto')
        lote = request.POST.get('lote')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')
        accion_correctiva = request.POST.get('accion_correctiva')
        verificacion_accion_correctiva = request.POST.get('verificacion_accion_correctiva')

        datos = DatosFormularioControlDeTransporte(
            nombre_tecnologo=nombre_tecnologo,
            fecha_registro=fecha_registro,
            fecha_recepcion=fecha_recepcion,
            producto_recepcion=producto_recepcion,
            temperatura_transporte=temperatura_transporte,
            temperatura_producto=temperatura_producto,
            lote=lote,
            fecha_vencimiento=fecha_vencimiento,
            accion_correctiva=accion_correctiva,
            verificacion_accion_correctiva=verificacion_accion_correctiva
            )
        datos.save()

        return JsonResponse({'mensaje': 'Datos guardados exitosamente'})

def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)