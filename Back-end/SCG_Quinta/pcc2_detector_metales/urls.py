from django.urls import path

from . import views

urlpatterns = [
    path("", views.pcc2_detector_metales, name="pcc2_detector_metales"),
    path("vista_pcc2_detector_metales/", views.vista_pcc2_detector_metales, name="vista_ppc2_detector_metales"),
    path("selecciones/", views.redireccionar_selecciones, name="redireccionar_seleciones")
]