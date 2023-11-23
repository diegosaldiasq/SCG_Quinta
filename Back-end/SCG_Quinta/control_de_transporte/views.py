from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioControlDeTransporte
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def control_de_transporte(request):
    return render(request, 'control_de_transporte/r_control_de_transporte.html')

@login_required
def vista_control_de_transporte(request):
    if request.method == 'POST':
        nombre_tecnologo = request.user.nombre_completo
        fecha_registro = timezone.now()
        fecha_recepcion = timezone.make_aware(datetime.strptime(request.POST.get('fecha_recepcion'), '%Y-%m-%d'), timezone=timezone.utc)
        producto_recepcion = request.POST.get('producto_recepcion')
        temperatura_transporte = request.POST.get('temperatura_transporte')
        temperatura_producto = request.POST.get('temperatura_producto')
        lote = request.POST.get('lote')
        fecha_vencimiento = timezone.make_aware(datetime.strptime(request.POST.get('fecha_vencimiento'), '%Y-%m-%d'), timezone=timezone.utc)
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

@login_required
def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)