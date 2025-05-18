from django.urls import path

from . import views

urlpatterns = [
    path("index/", views.index, name="index"),
    path("selecciones/", views.redireccionar_selecciones, name="redireccionar_selecciones"),
    path("selecciones_2/", views.redireccionar_selecciones_2, name="redireccionar_selecciones_2"),
    path("main/", views.redireccionar_main, name="redireccionar_main"),
    path("descargas/", views.descargas, name="descargas"),
    path("descargas_2/", views.descargas_2, name="descargas_2"),
    path("permisos/", views.permisos, name="permisos"),
    path("vista_permisos/", views.vista_permisos, name="vista_permisos"),
    path("permisos_faltante/", views.permisos_faltante, name="permisos_faltante"),
    path("intermedio/", views.intermedio, name="intermedio"),
    path("intermedio_2/", views.intermedio_2, name="intermedio_2"),
    path("intermedio_3/", views.intermedio_3, name="intermedio_3"),
    path("set_fechas/", views.set_fechas, name="set_fechas"),
    path("no_hay_datos/", views.no_hay_datos, name="no_hay_datos"),
    path("seleccion_verifica/", views.seleccion_verifica, name="seleccion_verifica"),
    path("seleccion_verifica_2/", views.seleccion_verifica_2, name="seleccion_verifica_2"),
    path("verificar/", views.verificar, name="verificar"),
    path("verificar_2/", views.verificar_2, name="verificar_2"),
    path("verificar_registros/", views.verificar_registros, name="verificar_registros"),
    path("descargar_registros/", views.descargar_registros, name="descargar_registros"),
    path("en_desarrollo/", views.en_desarrollo, name="en_desarrollo"),
    path("ver_foto/", views.ver_foto, name="ver_foto")
]