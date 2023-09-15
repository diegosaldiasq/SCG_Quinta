from django.urls import path

from . import views

urlpatterns = [
    path("", views.control_de_transporte, name="control_de_transporte"),
    path("", views.vista_control_de_transporte, name="vista_control_de_transporte"),
    path("selecciones/", views.redireccionar_selecciones, name="redireccionar_selecciones")
]