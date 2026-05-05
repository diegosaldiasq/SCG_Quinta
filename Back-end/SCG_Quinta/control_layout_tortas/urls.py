from django.urls import path
from . import views
from .views import (
    RegistroCreateView,
    RegistroDetalleView,
    HistorialRegistroListView,
)

app_name = "control_layout_tortas"

urlpatterns = [
    path("nuevo/", RegistroCreateView.as_view(), name="registro_nuevo"),
    path("historial/", HistorialRegistroListView.as_view(), name="historial_registros"),
    path("<int:pk>/", RegistroDetalleView.as_view(), name="registro_detalle"),
    path("<int:pk>/verificar/", views.verificar_registro, name="verificar_registro"),
    path("<int:pk>/desverificar/", views.desverificar_registro, name="desverificar_registro"),
    path("intermedio/", views.redireccionar_intermedio, name="redireccionar_intermedio"),
    path("api/clientes/", views.api_clientes_por_planta, name="api_clientes_por_planta"),
    path("api/productos/", views.api_productos_por_planta_cliente, name="api_productos_por_planta_cliente"),
    path("api/layout/", views.api_layout_por_producto, name="api_layout_por_producto"),
]