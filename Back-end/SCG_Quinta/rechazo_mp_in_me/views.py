from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioRechazoMpInMe
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
import json

# Create your views here.

@login_required
def rechazo_mp_in_me(request):
    return render(request, 'rechazo_mp_in_me/r_informe_rechazo_mp_in_me.html')

@login_required
def vista_rechazo_mp_in_me(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        dato = data.get('dato', None)
        if dato:
            nombre_tecnologo = request.user.nombre_completo
            fecha_registro = timezone.now()
            nombre_proveedor = dato.get('nombre_proveedor')
            numero_factura = dato.get('numero_factura')
            nombre_transportista = dato.get('nombre_transportista')
            nombre_producto = dato.get('nombre_producto')
            fecha_elaboracion = timezone.make_aware(datetime.strptime(dato.get('fecha_elaboracion'), '%Y-%m-%d'), timezone=timezone.utc)
            lote = dato.get('lote')
            fecha_vencimiento = timezone.make_aware(datetime.strptime(dato.get('fecha_vencimiento'), '%Y-%m-%d'), timezone=timezone.utc)
            motivo_rechazo = dato.get('motivo_rechazo')
            cantidad_producto_involucrado = dato.get('cantidad_producto_involucrado')
            unidad_de_medida = dato.get('unidad_de_medida')
            clasificacion = dato.get('clasificacion')


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

            return JsonResponse({'existe': True})
        else:
            return JsonResponse({'existe': False})

@login_required
def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)