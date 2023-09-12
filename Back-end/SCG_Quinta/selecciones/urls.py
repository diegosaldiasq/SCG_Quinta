from django.urls import path

from . import views

urlpatterns = [
    path("", views.vista_selecciones, name="vista_selecciones"),
    path("monitoreo_del_agua/", views.redireccionar_monitoreo_del_agua, name="redireccionar_monitoreo_del_agua"),
    path("historial_termometro/", views.redireccionar_historial_termometro, name='redireccionar_historial_termometro'),
    path("inicio/", views.redireccionar_inicio, name="redireccionar_inicio")
]

