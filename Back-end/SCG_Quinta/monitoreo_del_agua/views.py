from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioMonitoreoDelAgua


# Create your views here.

def monitoreo_del_agua(request):
    if request.method == 'POST' and request.is_ajax():
        nombre_tecnologo = request.POST.get('nombre_tecnologo')
        fecha_registro = request.POST.get('fecha_registro')
        turno_ = request.POST.get('turno_')
        planta_ = request.POST.get('planta_')
        numero_llave = request.POST.get('numero_llave')
        punto_muestreo = request.POST.get('punto_muestreo')
        sabor_insipido = request.POST.get('sabor_insipido')
        olor_inodora = request.POST.get('olor_inodora')
        color_incoloro = request.POST.get('color_incoloro')
        ph_ = request.POST.get('ph_')
        cloro_libre = request.POST.get('cloro_libre')
        accion_correctiva = request.POST.get('accion_correctiva')
        resultado_ac = request.POST.get('resultado_ac')


        datos = DatosFormularioMonitoreoDelAgua(
            nombre_tecnologo=nombre_tecnologo, 
            fecha_registro=fecha_registro,
            turno_=turno_,
            planta_=planta_,
            numero_llave=numero_llave,
            punto_muestreo=punto_muestreo,
            sabor_insipido=sabor_insipido,
            olor_inodora=olor_inodora,
            color_incoloro=color_incoloro,
            ph_=ph_,
            cloro_libre=cloro_libre,
            accion_correctiva=accion_correctiva,
            resultado_ac=resultado_ac
            )
        datos.save()

        return JsonResponse({'mensaje': 'Datos guardados exitosamente'})