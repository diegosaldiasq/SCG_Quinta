from django.urls import path

from . import views

urlpatterns = [
    path("", views.recepcion_mpme, name="recepcion_mpme"),
    path("vista_recepcion_mpme/", views.vista_recepcion_mpme, name="vista_recepcion_mpme"),
    path("selecciones/", views.redireccionar_selecciones, name="redireccionar_selecciones")
]