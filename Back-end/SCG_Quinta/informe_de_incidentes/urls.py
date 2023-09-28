from django.urls import path

from . import views

urlpatterns = [
    path("", views.informe_de_incidentes, name="informe_de_incidentes"),
    path("vista_informe_de_incidentes/", views.vista_informe_de_incidentes, name="vista_informe_de_incidentes"),
    path("selecciones/", views.redireccionar_selecciones, name="redireccionar_selecciones")
]