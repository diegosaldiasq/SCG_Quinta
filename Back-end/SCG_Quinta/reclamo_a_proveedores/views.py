from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioReclamoProveedores

# Create your views here.

def reclamo_a_proveedores(request):
    if request.method == 'POST' and request.is_ajax():
        nombre_tecnologo = request.POST.get('nombre_tecnologo')
        fecha_registro = request.POST.get('fecha_registro')
        nombre_proveedor = request.POST.get('nombre_proveedor')
        fecha_reclamo = request.POST.get('fecha_reclamo')
        nombre_del_producto = request.POST.get('nombre_del_producto')
        fecha_elaboracion = request.POSt.get('fecha_elaboracion')
        lote = request.POST.get('lote')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')
        no_conformidad = request.POST.get('no_conformidad')
        clasificacion = request.POST.get('clasificacion')
        cantidad_involucrada = request.POST.get('cantidad_involucrada')
        unidad_de_medida = request.POST.get('unidad_de_medida')
        archivo_foto = request.POST.get('archivo_foto')
        

        datos = DatosFormularioReclamoProveedores(
            nombre_tecnologo=nombre_tecnologo,
            fecha_registro=fecha_registro,
            nombre_proveedor=nombre_proveedor,
            fecha_reclamo=fecha_reclamo,
            nombre_del_producto=nombre_del_producto,
            fecha_elaboracion=fecha_elaboracion,
            lote=lote,
            fecha_vencimiento=fecha_vencimiento,
            no_conformidad=no_conformidad,
            clasificacion=clasificacion,
            cantidad_involucrada=cantidad_involucrada,
            unidad_de_medida=unidad_de_medida,
            archivo_foto=archivo_foto
            )
        datos.save()

        return JsonResponse({'mensaje': 'Datos guardados exitosamente'})
