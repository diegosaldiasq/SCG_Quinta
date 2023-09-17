from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def vista_selecciones(request):
    return render(request, 'selecciones/selecciones.html')

def redireccionar_historial_termometro(request):
    url_historial_termometro = reverse('historial_termometro')
    return HttpResponseRedirect(url_historial_termometro)

def redireccionar_inicio(request):
    url_inicio = reverse('index')
    return HttpResponseRedirect(url_inicio)

def redireccionar_monitoreo_del_agua(request):
    url_monitoreo_del_agua = reverse('monitoreo_del_agua')
    return HttpResponseRedirect(url_monitoreo_del_agua)

def redireccionar_monitoreo_de_plagas(request):
    url_monitoreo_de_plagas = reverse('monitoreo_de_plagas')
    return HttpResponseRedirect(url_monitoreo_de_plagas)

def redireccionar_higiene_y_conducta_personal(request):
    url_higiene_y_conducta_personal = reverse('higiene_y_conducta_personal')
    return HttpResponseRedirect(url_higiene_y_conducta_personal)

def redireccionar_recepcion_mpme(request):
    url_repecion_mpme = reverse('recepcion_mpme')
    return HttpResponseRedirect(url_repecion_mpme)

def redireccionar_ppc2_detector_metales(request):
    url_pcc2_detector_metales = reverse('pcc2_detector_metales')
    return HttpResponseRedirect(url_pcc2_detector_metales)

def redireccionar_control_de_transporte(request):
    url_control_de_transporte = reverse('control_de_transporte')
    return HttpResponseRedirect(url_control_de_transporte)

def redireccionar_temperatura_despacho_ptjumbo(request):
    url_temperatura_despacho_ptjumbo = reverse('temperatura_despacho_ptjumbo')
    return HttpResponseRedirect(url_temperatura_despacho_ptjumbo)

def redireccionar_temperatura_despacho_ptsisa(request):
    url_temperatura_despacho_ptsisa = reverse('temperatura_despacho_ptsisa')
    return HttpResponseRedirect(url_temperatura_despacho_ptsisa)

def redireccionar_reclamo_a_proveedores(request):
    url_reclamo_a_proveedores = reverse('reclamo_a_proveedores')
    return HttpResponseRedirect(url_reclamo_a_proveedores)

def redireccionar_rechazo_mp_in_me(request):
    url_rechazo_mp_in_me = reverse('rechazo_mp_in_me')
    return HttpResponseRedirect(url_rechazo_mp_in_me)