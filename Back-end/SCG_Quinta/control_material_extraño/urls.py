from django.urls import path

from . import views

urlpatterns = [
    path("", views.control_material_extraño, name="control_material_extraño"),
    path("vista_control_material_extraño/", views.vista_control_material_extraño, name="vista_control_material_extraño"),
    path("selecciones/", views.redireccionar_selecciones, name="redireccionar_selecciones")
]