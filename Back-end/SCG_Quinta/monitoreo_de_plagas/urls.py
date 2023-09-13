from django.urls import path

from . import views

urlpatterns = [
    path("", views.monitoreo_de_plagas, name="monitoreo_de_plagas"),
    path("", views.vista_monitoreo_de_plagas, name="vista_monitoreo_de plagas"),
    path("selecciones/", views.redireccionar_selecciones, name="redireccionar_sellecciones")
]