from django.urls import path

from . import views

urlpatterns = [
    path("", views.control_de_pesos_insumos_kuchen, name="control_de_pesos_insumos_kuchen"),
    path("vista_control_de_pesos_insumos_kuchen/", views.vista_control_de_pesos, name="vista_control_de_pesos_insumos_kuchen"),
    path("selecciones/", views.redireccionar_selecciones_2, name="redireccionar_selecciones_2")
]