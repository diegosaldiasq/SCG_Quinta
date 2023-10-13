from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioTemperaturaDespachoSisa
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def temperatura_despacho_ptsisa(request):
    return render(request, 'temperatura_despacho_ptsisa/r_temperatura_despacho_ptsisa.html')

@login_required
def vista_temperatura_despacho_ptsisa(request):
    if request.method == 'POST':
        nombre_tecnologo = request.POST.get('nombre_tecnologo')
        fecha_registro = timezone.make_aware(datetime.strptime(request.POST.get('fecha_registro'), '%Y-%m-%dT%H:%M'), timezone=timezone.utc)
        cadena = request.POST.get('cadena')
        item = request.POST.get('item')
        producto = request.POST.get('producto')
        congelado_refrigerado = request.POST.get('congelado_refrigerado')
        temperatura_producto = request.POST.get('temperatura_producto')
        revision_etiquetado = request.POST.get('revision_etiquetado')
        lote = request.POST.get('lote')
        fecha_vencimiento = timezone.make_aware(datetime.strptime(request.POST.get('fecha_vencimiento'), '%Y-%m-%d'), timezone=timezone.utc)
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

@login_required
def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)