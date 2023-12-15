from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioTemperaturaDespachoSisa
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
import json

# Create your views here.

@login_required
def temperatura_despacho_ptsisa(request):
    return render(request, 'temperatura_despacho_ptsisa/r_temperatura_despacho_ptsisa.html')

@login_required
def vista_temperatura_despacho_ptsisa(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        dato = data.get('dato', None)
        if dato:
            nombre_tecnologo = request.user.nombre_completo
            fecha_registro = timezone.now()
            cadena = dato.get('cadena')
            item = dato.get('item')
            producto = dato.get('producto')
            congelado_refrigerado = dato.get('congelado_refrigerado')
            temperatura_producto = dato.get('temperatura_producto')
            revision_etiquetado = dato.get('revision_etiquetado')
            lote = dato.get('lote')
            fecha_vencimiento = timezone.make_aware(datetime.strptime(dato.get('fecha_vencimiento'), '%Y-%m-%d'), timezone=timezone.utc)
            accion_correctiva = dato.get('accion_correctiva')
            verificacion_accion_correctiva = dato.get('verificacion_accion_correctiva')        


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

            return JsonResponse({'existe': True})
        else:
            return JsonResponse({'existe': False})

@login_required
def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)