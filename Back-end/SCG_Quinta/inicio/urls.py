from django.urls import path

from . import views

urlpatterns = [
    path("index/", views.index, name="index"),
    path("selecciones/", views.redireccionar_selecciones, name="redireccionar_selecciones"),
    path("main/", views.redireccionar_main, name="redireccionar_main"),
    path("descargas/", views.descargas, name="descargas"),
    path("permisos/", views.permisos, name="permisos"),
    path("vista_permisos/", views.vista_permisos, name="vista_permisos"),
    path("permisos_faltante/", views.permisos_faltante, name="permisos_faltante"),
    path("intermedio/", views.intermedio, name="intermedio"),
    path("set_fechas/", views.set_fechas, name="set_fechas"),
    path("no_hay_datos/", views.no_hay_datos, name="no_hay_datos"),
    path("seleccion_verifica/", views.seleccion_verifica, name="seleccion_verifica"),
    path("verificar/", views.verificar, name="verificar"),
    path("verificar_registros/", views.verificar_registros, name="verificar_registros"),
    path("descargar_registros/", views.descargar_registros, name="descargar_registros"),
    path("en_desarrollo/", views.en_desarrollo, name="en_desarrollo"),
    path("ver_foto/", views.ver_foto, name="ver_foto")
]