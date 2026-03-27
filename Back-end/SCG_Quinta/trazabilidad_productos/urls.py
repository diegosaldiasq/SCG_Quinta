from django.urls import path
from . import views

app_name = "trazabilidad_productos"

urlpatterns = [
    path("registrar/", views.registrar_trazabilidad, name="registrar_trazabilidad"),
    path("historial/", views.historial_trazabilidad, name="historial_trazabilidad"),

    path("ajax/productos/", views.obtener_productos_por_cliente, name="obtener_productos_por_cliente"),
    path("ajax/ingredientes/", views.obtener_ingredientes_por_producto, name="obtener_ingredientes_por_producto"),
    path("ajax/proveedores/", views.obtener_proveedores, name="obtener_proveedores"),
    path("intermedio/", views.redireccionar_intermedio, name="redireccionar_intermedio"),
    path("intermedio_2/", views.redireccionar_intermedio_2, name="redireccionar_intermedio_2"),
    path("verificar/<int:registro_id>/", views.verificar_trazabilidad, name="verificar_trazabilidad"),
    path("historial/excel/", views.descargar_historial_trazabilidad_excel, name="descargar_historial_trazabilidad_excel"),
]