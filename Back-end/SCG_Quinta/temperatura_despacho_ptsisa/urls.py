from django.urls import path

from . import views

urlpatterns = [
    path("", views.temperatura_despacho_ptsisa, name="temperatura_despacho_ptsisa"),
    path("", views.vista_temperatura_despacho_ptsisa, name="vista_temperatura_despacho_pt_sisa"),
    path("selecciones/", views.redireccionar_selecciones, name="redireccionar_selecciones")
]