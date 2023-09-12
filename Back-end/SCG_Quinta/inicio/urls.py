from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("selecciones/", views.redireccionar_selecciones, name="redireccionar_selecciones")
]