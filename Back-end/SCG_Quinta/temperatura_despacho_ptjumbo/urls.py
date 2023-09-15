from django.urls import path

from . import views

urlpatterns = [
    path("", views.temperatura_despacho_ptjumbo, name="temperatura_despacho_ptjumbo"),
    path("", views.vista_temperatura_despacho_ptjumbo, name="vista_temperatura_despachp_ptjumbo"),
    path("selecciones/", views.redireccionar_selecciones, name="redireccionar_selecciones")
]