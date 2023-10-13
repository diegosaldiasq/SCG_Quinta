from django.urls import path

from . import views

urlpatterns = [
    path("index/", views.index, name="index"),
    path("selecciones/", views.redireccionar_selecciones, name="redireccionar_selecciones"),
    path("main/", views.redireccionar_main, name="redireccionar_main")
]