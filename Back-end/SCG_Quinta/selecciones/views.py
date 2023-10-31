from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def vista_selecciones(request):
    return render(request, 'selecciones/selecciones.html')

@login_required
def redireccionar_historial_termometro(request):
    url_historial_termometro = reverse('historial_termometro')
    return HttpResponseRedirect(url_historial_termometro)

@login_required
def redireccionar_inicio(request):
    url_inicio = reverse('index')
    return HttpResponseRedirect(url_inicio)

@login_required
def redireccionar_monitoreo_del_agua(request):
    url_monitoreo_del_agua = reverse('monitoreo_del_agua')
    return HttpResponseRedirect(url_monitoreo_del_agua)

@login_required
def redireccionar_monitoreo_de_plagas(request):
    url_monitoreo_de_plagas = reverse('monitoreo_de_plagas')
    return HttpResponseRedirect(url_monitoreo_de_plagas)

@login_required
def redireccionar_higiene_y_conducta_personal(request):
    url_higiene_y_conducta_personal = reverse('higiene_y_conducta_personal')
    return HttpResponseRedirect(url_higiene_y_conducta_personal)

@login_required
def redireccionar_recepcion_mpme(request):
    url_repecion_mpme = reverse('recepcion_mpme')
    return HttpResponseRedirect(url_repecion_mpme)

@login_required
def redireccionar_ppc2_detector_metales(request):
    url_pcc2_detector_metales = reverse('pcc2_detector_metales')
    return HttpResponseRedirect(url_pcc2_detector_metales)

@login_required
def redireccionar_control_de_transporte(request):
    url_control_de_transporte = reverse('control_de_transporte')
    return HttpResponseRedirect(url_control_de_transporte)

@login_required
def redireccionar_temperatura_despacho_ptjumbo(request):
    url_temperatura_despacho_ptjumbo = reverse('temperatura_despacho_ptjumbo')
    return HttpResponseRedirect(url_temperatura_despacho_ptjumbo)

@login_required
def redireccionar_temperatura_despacho_ptsisa(request):
    url_temperatura_despacho_ptsisa = reverse('temperatura_despacho_ptsisa')
    return HttpResponseRedirect(url_temperatura_despacho_ptsisa)

@login_required
def redireccionar_reclamo_a_proveedores(request):
    url_reclamo_a_proveedores = reverse('reclamo_a_proveedores')
    return HttpResponseRedirect(url_reclamo_a_proveedores)

@login_required
def redireccionar_rechazo_mp_in_me(request):
    url_rechazo_mp_in_me = reverse('rechazo_mp_in_me')
    return HttpResponseRedirect(url_rechazo_mp_in_me)

@login_required
def redireccionar_informe_de_incidentes(request):
    url_informe_de_incidentes = reverse('informe_de_incidentes')
    return HttpResponseRedirect(url_informe_de_incidentes)

@login_required
def redireccionar_control_material_extraño(request):
    url_control_material_extraño = reverse('control_material_extraño')
    return HttpResponseRedirect(url_control_material_extraño)

@login_required
def redireccionar_intermedio(request):
    url_intermedio = reverse('intermedio')
    return HttpResponseRedirect(url_intermedio)