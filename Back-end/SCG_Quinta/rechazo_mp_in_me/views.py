from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioRechazoMpInMe

# Create your views here.

def rechazo_mp_in_me(request):
    if request.method == 'POST' and request.is_ajax():
        nombre_tecnologo = request.POST.get('nombre_tecnologo')
        fecha_registro = request.POST.get('fecha_registro')
        nombre_proveedor = request.POST.get('nombre_proveedor')
        numero_factura = request.POST.get('numero_factura')
        nombre_transportista = request.POST.get('nombre_transportista')
        nombre_producto = request.POST.get('nombre_producto')
        fecha_elaboracion = request.POSt.get('fecha_elaboracion')
        lote = request.POST.get('lote')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')
        motivo_rechazo = request.POST.get('motivo_rechazo')
        cantidad_producto_involucrado = request.POST.get('cantidad_producto_involucrado')
        unidad_de_medida = request.POST.get('unidad_de_medida')
        clasificacion = request.POST.get('clasificacion')


        datos = DatosFormularioRechazoMpInMe(
            nombre_tecnologo=nombre_tecnologo,
            fecha_registro=fecha_registro,
            nombre_proveedor=nombre_proveedor,
            numero_factura=numero_factura,
            nombre_transportista=nombre_transportista,
            nombre_producto=nombre_producto,
            fecha_elaboracion=fecha_elaboracion,
            lote=lote,
            fecha_vencimiento=fecha_vencimiento,
            motivo_rechazo=motivo_rechazo,
            cantidad_producto_involucrado=cantidad_producto_involucrado,
            unidad_de_medida=unidad_de_medida,
            clasificacion=clasificacion
            )
        datos.save()

        return JsonResponse({'mensaje': 'Datos guardados exitosamente'})
