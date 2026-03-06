from django.urls import path
from . import views

urlpatterns = [
    path("registrar/", views.registrar_trazabilidad, name="registrar_trazabilidad"),
    path("historial/", views.historial_trazabilidad, name="historial_trazabilidad"),

    path("ajax/productos/", views.obtener_productos_por_cliente, name="obtener_productos_por_cliente"),
    path("ajax/ingredientes/", views.obtener_ingredientes_por_producto, name="obtener_ingredientes_por_producto"),
    path("ajax/proveedores/", views.obtener_proveedores, name="obtener_proveedores"),
]