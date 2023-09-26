from django.urls import path

from . import views

urlpatterns = [
    path("", views.monitoreo_del_agua, name="monitoreo_del_agua"),
    path("vista_monitoreo_del_agua/", views.vista_monitoreo_del_agua, name="vista_monitoreo_del_agua"),
    path("selecciones/", views.redireccionar_selecciones, name="redireccionar_selecciones")
]