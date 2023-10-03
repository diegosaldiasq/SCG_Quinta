from django.urls import path

from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("ingresa_rut/", views.ingresa_rut, name="ingresa_rut"),
    path("crear_cuenta/", views.crear_cuenta, name="crear_cuenta")
]