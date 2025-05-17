from django.urls import path

from . import views

urlpatterns = [
    path("", views.control_de_pesos, name="control_de_pesos"),
    path("vista_control_de_pesos/", views.vista_control_de_transporte, name="vista_control_de_pesos"),
    path("selecciones/", views.redireccionar_selecciones, name="redireccionar_selecciones")
]