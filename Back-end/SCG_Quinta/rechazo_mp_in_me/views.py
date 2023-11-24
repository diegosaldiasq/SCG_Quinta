from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioRechazoMpInMe
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def rechazo_mp_in_me(request):
    return render(request, 'rechazo_mp_in_me/r_informe_rechazo_mp_in_me.html')

@login_required
def vista_rechazo_mp_in_me(request):
    if request.method == 'POST':
        nombre_tecnologo = request.user.nombre_completo
        fecha_registro = timezone.now()
        nombre_proveedor = request.POST.get('nombre_proveedor')
        numero_factura = request.POST.get('numero_factura')
        nombre_transportista = request.POST.get('nombre_transportista')
        nombre_producto = request.POST.get('nombre_producto')
        fecha_elaboracion = timezone.make_aware(datetime.strptime(request.POST.get('fecha_elaboracion'), '%Y-%m-%d'), timezone=timezone.utc)
        lote = request.POST.get('lote')
        fecha_vencimiento = timezone.make_aware(datetime.strptime(request.POST.get('fecha_vencimiento'), '%Y-%m-%d'), timezone=timezone.utc)
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

@login_required
def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)