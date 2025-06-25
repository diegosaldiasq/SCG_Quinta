from django.urls import path

from . import views

urlpatterns = [
    path("", views.vista_selecciones, name="vista_selecciones"),
    path("monitoreo_del_agua/", views.redireccionar_monitoreo_del_agua, name="redireccionar_monitoreo_del_agua"),
    path("historial_termometro/", views.redireccionar_historial_termometro, name='redireccionar_historial_termometro'),
    path("inicio/", views.redireccionar_inicio, name="redireccionar_inicio"),
    path("monitoreo_de_plagas/", views.redireccionar_monitoreo_de_plagas, name="redireccionar_monitoreo_de_plagas"),
    path("higiene_y_conducta_personal/", views.redireccionar_higiene_y_conducta_personal, name="redireccionar_higiene_y_conducta_personal"),
    path("recepcion_mpme/", views.redireccionar_recepcion_mpme, name="redireccionar_recepcion_mpme"),
    path("pcc2_detector_metales/", views.redireccionar_ppc2_detector_metales, name="redireccionar_pcc2_detector_metales"),
    path("control_de_transporte/", views.redireccionar_control_de_transporte, name="redireccionar_control_de_transporte"),
    path("temperatura_despacho_ptjumbo/", views.redireccionar_temperatura_despacho_ptjumbo, name="redireccionar_temperatura_despacho_ptjumbo"),
    path("temperatura_despacho_ptsisa/", views.redireccionar_temperatura_despacho_ptsisa, name="redireccionar_temperatura_despacho_ptsisa"),
    path("reclamo_a_proveedores/", views.redireccionar_reclamo_a_proveedores, name="redireccionar_reclamo_a_proveedores"),
    path("rechazo_mp_in_me/", views.redireccionar_rechazo_mp_in_me, name="redireccionar_rechazo_mp_in_me"),
    path("informe_de_incidentes/", views.redireccionar_informe_de_incidentes, name="redireccionar_informe_de_incidentes"),
    path("control_material_extraño/", views.redireccionar_control_material_extraño, name="redireccionar_control_material_extraño"),
    path("index/", views.redireccionar_index, name="redireccionar_index"),
    path("en_construccion/", views.en_construccion, name="en_construccion"),
    path("control_de_pesos/", views.redireccionar_control_de_pesos, name="redireccionar_control_de_pesos"),
    path("vista_selecciones_2/", views.vista_selecciones_2, name="vista_selecciones_2"),
    path("control_parametros_gorreri/", views.redireccionar_control_parametros_gorreri, name="redireccionar_control_parametros_gorreri"),
    path("control_de_pesos_prelistos/", views.redireccionar_control_de_pesos_prelistos, name="redireccionar_control_de_pesos_prelistos")
]

