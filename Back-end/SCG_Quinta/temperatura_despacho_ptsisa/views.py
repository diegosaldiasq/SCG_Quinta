from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioTemperaturaDespachoSisa

# Create your views here.


def temperatura_despacho_ptsisa(request):
    if request.method == 'POST' and request.is_ajax():
        nombre_tecnologo = request.POST.get('nombre_tecnologo')
        fecha_registro = request.POST.get('fecha_registro')
        cadena = request.POST.get('cadena')
        item = request.POST.get('item')
        producto = request.POST.get('producto')
        congelado_refrigerado = request.POST.get('congelado_refrigerado')
        temperatura_producto = request.POST.get('temperatura_producto')
        revision_etiquetado = request.POST.get('revision_etiquetado')
        lote = request.POST.get('lote')
        fecha_vencimiento = render.POST.get('fecha_vencimiento')
        accion_correctiva = request.POST.get('accion_correctiva')
        verificacion_accion_correctiva = request.POST.get('verificacion_accion_correctiva')        


        datos = DatosFormularioTemperaturaDespachoSisa(
            nombre_tecnologo=nombre_tecnologo, 
            fecha_registro=fecha_registro,
            cadena=cadena,
            item=item,
            producto=producto,
            congelado_refrigerado=congelado_refrigerado,
            temperatura_producto=temperatura_producto,
            revision_etiquetado=revision_etiquetado,
            lote=lote,
            fecha_vencimiento=fecha_vencimiento,
            accion_correctiva=accion_correctiva,
            verificacion_accion_correctiva=verificacion_accion_correctiva
            )
        datos.save()

        return JsonResponse({'mensaje': 'Datos guardados exitosamente'})