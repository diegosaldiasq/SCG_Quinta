from django.urls import path

from . import views

urlpatterns = [
    path("", views.reclamo_a_proveedores, name="reclamo_a_proveedores"),
    path("vista_reclamo_a_proveedores/", views.vista_reclamo_a_proveedores, name="vista_reclamo_a_proveedores"),
    path("selecciones/", views.redireccionar_selecciones, name="redireccionar_selecciones")
]