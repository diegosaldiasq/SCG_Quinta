from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioMonitoreoDelAgua
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def monitoreo_del_agua(request):
    return render(request, 'monitoreo_del_agua/r_monitoreo_del_agua.html')

@login_required
def vista_monitoreo_del_agua(request):
    if request.method == 'POST':
        nombre_tecnologo = request.POST.get('nombre_tecnologo')
        fecha_registro = timezone.make_aware(datetime.strptime(request.POST.get('fecha_registro'), '%Y-%m-%dT%H:%M'), timezone=timezone.utc)
        turno_mda = request.POST.get('turno_mda')
        planta_mda = request.POST.get('planta_mda')
        numero_llave = request.POST.get('numero_llave')
        punto_muestreo = request.POST.get('punto_muestreo')
        sabor_insipido = request.POST.get('sabor_insipido')
        olor_inodora = request.POST.get('olor_inodora')
        color_incoloro = request.POST.get('color_incoloro')
        ph_mda = request.POST.get('ph_mda')
        cloro_libre = request.POST.get('cloro_libre')
        accion_correctiva = request.POST.get('accion_correctiva')
        resultado_ac = request.POST.get('resultado_ac')


        datos = DatosFormularioMonitoreoDelAgua(
            nombre_tecnologo=nombre_tecnologo, 
            fecha_registro=fecha_registro,
            turno_mda=turno_mda,
            planta_mda=planta_mda,
            numero_llave=numero_llave,
            punto_muestreo=punto_muestreo,
            sabor_insipido=sabor_insipido,
            olor_inodora=olor_inodora,
            color_incoloro=color_incoloro,
            ph_mda=ph_mda,
            cloro_libre=cloro_libre,
            accion_correctiva=accion_correctiva,
            resultado_ac=resultado_ac
            )
        datos.save()

        return JsonResponse({'mensaje': 'Datos guardados exitosamente'})

@login_required
def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)

