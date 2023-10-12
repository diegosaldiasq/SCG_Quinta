from django.urls import path

from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("ingresa_rut/", views.ingresa_rut, name="ingresa_rut"),
    path("crear_cuenta/", views.crear_cuenta, name="crear_cuenta"),
    path("vista_crear_cuenta/", views.vista_crear_cuenta, name="vista_crear_cuenta"),
    path("cuenta_creada/", views.cuenta_creada, name="cuenta_creada"),
    path("vista_ingresa_rut/", views.vista_ingresa_rut, name="vista_ingresa_rut"),
    path("pasword/", views.pasword, name="pasword"),
    path("pasword_creado/", views.pasword_creado, name="ingresa_password"),
    path("vista_pasword/", views.vista_pasword, name="vista_pasword"),
]