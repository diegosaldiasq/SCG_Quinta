from django.urls import path

from . import views

urlpatterns = [
    path("", views.historial_termometro, name="historial_termometro"),
    path("", views.vista_historial_termometro, name="vista_historial_termometro_app2"),
    path("selecciones/", views.redireccionar_selecciones, name="redireccionar_selecciones")
]