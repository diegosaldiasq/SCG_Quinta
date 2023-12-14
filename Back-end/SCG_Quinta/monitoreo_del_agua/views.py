from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioMonitoreoDelAgua
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import json


# Create your views here.

@login_required
def monitoreo_del_agua(request):
    return render(request, 'monitoreo_del_agua/r_monitoreo_del_agua.html')

@login_required
def vista_monitoreo_del_agua(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        dato = data.get('dato', None)
        if dato:
            nombre_tecnologo = request.user.nombre_completo
            fecha_registro = timezone.now()
            turno_mda = dato.get('turno_mda')
            planta_mda = dato.get('planta_mda')
            numero_llave = dato.get('numero_llave')
            punto_muestreo = dato.get('punto_muestreo')
            sabor_insipido = dato.get('sabor_insipido')
            olor_inodora = dato.get('olor_inodora')
            color_incoloro = dato.get('color_incoloro')
            ph_mda = dato.get('ph_mda')
            cloro_libre = dato.get('cloro_libre')
            accion_correctiva = dato.get('accion_correctiva')
            resultado_ac = dato.get('resultado_ac')


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

            return JsonResponse({'existe': True})
        else:
            return JsonResponse({'existe': False})

@login_required
def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)

