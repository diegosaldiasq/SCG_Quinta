from django.urls import path

from . import views

urlpatterns = [
    path("", views.rechazo_mp_in_me, name="rechazo_mp_in_me"),
    path("vista_rechazo_mp_in_me/", views.vista_rechazo_mp_in_me, name="vista_rechazo_mp_in_me"),
    path("selecciones/", views.redireccionar_selecciones, name="redireccionar_selecciones")
]