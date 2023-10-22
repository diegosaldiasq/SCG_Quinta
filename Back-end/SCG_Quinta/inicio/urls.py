from django.urls import path

from . import views

urlpatterns = [
    path("index/", views.index, name="index"),
    path("selecciones/", views.redireccionar_selecciones, name="redireccionar_selecciones"),
    path("main/", views.redireccionar_main, name="redireccionar_main"),
    path("descargas/", views.descargas, name="descargas"),
    path("descargar_monitoreo_del_agua/", views.descargar_monitoreo_del_agua, name="descargar_monitoreo_del_agua"),
    path("descargar_higiene_y_conducta_personal/", views.descargar_higiene_y_conducta_personal, name="descargar_higiene_y_conducta_personal"),
    path("descargar_monitoreo_de_plagas/", views.descargar_monitoreo_de_plagas, name="descargar_monitoreo_de_plagas"),
    path("descargar_recepcion_mpme/", views.descargar_recepcion_mpme, name="descargar_recepcion_mpme"),
    path("descargar_pcc2_detector_metales/", views.descargar_pcc2_detector_metales, name="descargar_pcc2_detector_metales"),
    path("descargar_control_de_transporte/", views.descargar_control_de_transporte, name="descargar_control_de_transporte"),
    path("descargar_temperatura_despacho_ptjumbo/", views.descargar_temperatura_despacho_ptjumbo, name="descargar_temperatura_despacho_ptjumbo"),
    path("descargar_temperatura_despacho_ptsisa/", views.descargar_temperatura_despacho_ptsisa, name="descargar_temperatura_despacho_ptsisa"),
    path("descargar_historial_termometro/", views.descargar_historial_termometro, name="descargar_historial_termometro"),
    path("descargar_reclamo_a_proveedores/", views.descargar_reclamo_a_proveedores, name="descargar_reclamo_a_proveedores"),
    path("descargar_rechazo_mp_in_me/", views.descargar_rechazo_mp_in_me, name="descargar_rechazo_mp_in_me"),
    path("informe_de_incidentes/", views.descargar_informe_de_incidentes, name="descargar_informe_de_incidentes"),
    path("descargar_control_material_extraño/", views.descargar_control_material_extraño, name="descargar_control_material_extraño")
]