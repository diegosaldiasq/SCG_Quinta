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
    path("temperatura_despacho_ptjumbo/", views.redireccionar_temperatura_despacho_ptjumbo, name="redireccionar_temperatura_despacho_ptjumbo")
]

