from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioRecepcionMpMe
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
import json

# Create your views here.

@login_required
def recepcion_mpme(request):
    return render(request, 'recepcion_mpme/r_recepcion_mpme.html')

@login_required
def vista_recepcion_mpme(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        dato = data.get('dato', None)
        if dato:
            nombre_tecnologo = request.user.nombre_completo
            lote_dia = dato.get('lote_dia')
            fecha_registro = timezone.now()
            nombre_proveedor = dato.get('nombre_proveedor')
            nombre_producto = dato.get('nombre_producto')
            fecha_elaboracion = timezone.make_aware(datetime.strptime(dato.get('fecha_elaboracion'), '%Y-%m-%d'), timezone=timezone.utc)
            fecha_vencimiento = timezone.make_aware(datetime.strptime(dato.get('fecha_vencimiento'), '%Y-%m-%d'), timezone=timezone.utc)
            lote_producto = dato.get('lote_producto')
            numero_factura = dato.get('numero_factura')
            higiene = dato.get('higiene')
            rs = dato.get('rs')
            temperatura_transporte = dato.get('temperatura_transporte')
            apariencia = dato.get('apariencia')
            textura = dato.get('textura')
            ausencia_material_extraño = dato.get('ausencia_material_extraño')
            temperatura_producto = dato.get('temperatura_producto')
            condicion_envase = dato.get('condicion_envase')
            color = dato.get('color')
            olor = dato.get('olor')
            sabor = dato.get('sabor')
            grados_brix = dato.get('grados_brix')

            datos = DatosFormularioRecepcionMpMe(
                nombre_tecnologo=nombre_tecnologo,
                lote_dia=lote_dia, 
                fecha_registro=fecha_registro,
                nombre_proveedor=nombre_proveedor,
                nombre_producto=nombre_producto,
                fecha_elaboracion=fecha_elaboracion,
                fecha_vencimiento=fecha_vencimiento,
                lote_producto=lote_producto,
                numero_factura=numero_factura,
                higiene=higiene,
                rs=rs,
                temperatura_transporte=temperatura_transporte,
                apariencia=apariencia,
                textura=textura,
                ausencia_material_extraño=ausencia_material_extraño,
                temperatura_producto=temperatura_producto,
                condicion_envase=condicion_envase,
                color=color,
                olor=olor,
                sabor=sabor,
                grados_brix=grados_brix
                )
            datos.save()

            return JsonResponse({'existe': True})
        else:
            return JsonResponse({'existe': False})


@login_required
def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)