from django.urls import path

from . import views

urlpatterns = [
    path("", views.control_de_pesos_prelistos, name="control_de_pesos_prelistos"),
    path("vista_control_de_pesos_prelistos/", views.vista_control_de_pesos_prelistos, name="vista_control_de_pesos_prelistos"),
    path("selecciones/", views.redireccionar_selecciones_2, name="redireccionar_selecciones_2")
]