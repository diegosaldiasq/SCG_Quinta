from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioRecepcionMpMe
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def recepcion_mpme(request):
    return render(request, 'recepcion_mpme/r_recepcion_mpme.html')

@login_required
def vista_recepcion_mpme(request):
    if request.method == 'POST':
        nombre_tecnologo = request.user.nombre_completo
        lote_dia = request.POST.get('lote_dia')
        fecha_registro = timezone.make_aware(datetime.strptime(request.POST.get('fecha_registro'), '%Y-%m-%dT%H:%M'), timezone=timezone.utc)
        nombre_proveedor = request.POST.get('nombre_proveedor')
        nombre_producto = request.POST.get('nombre_producto')
        fecha_elaboracion = timezone.make_aware(datetime.strptime(request.POST.get('fecha_elaboracion'), '%Y-%m-%d'), timezone=timezone.utc)
        fecha_vencimiento = timezone.make_aware(datetime.strptime(request.POST.get('fecha_vencimiento'), '%Y-%m-%d'), timezone=timezone.utc)
        lote_producto = request.POST.get('lote_producto')
        numero_factura = request.POST.get('numero_factura')
        higiene = request.POST.get('higiene')
        rs = request.POST.get('rs')
        temperatura_transporte = request.POST.get('temperatura_transporte')
        apariencia = request.POST.get('apariencia')
        textura = request.POST.get('textura')
        ausencia_material_extraño = request.POST.get('ausencia_material_extraño')
        temperatura_producto = request.POST.get('temperatura_producto')
        condicion_envase = request.POST.get('condicion_envase')
        color = request.POST.get('color')
        olor = request.POST.get('olor')
        sabor = request.POST.get('sabor')
        grados_brix = request.POST.get('grados_brix')


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

        return JsonResponse({'mensaje': 'Datos guardados exitosamente'})

@login_required
def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)