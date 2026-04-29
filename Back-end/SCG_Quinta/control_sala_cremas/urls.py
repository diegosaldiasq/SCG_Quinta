from django.urls import path
from . import views

app_name = "control_sala_cremas"

urlpatterns = [
    path("registro/", views.registro_sala_cremas, name="registro_sala_cremas"),
    path("historial/", views.historial_sala_cremas, name="historial_sala_cremas"),
    path("descargar-excel/", views.descargar_sala_cremas_excel, name="descargar_sala_cremas_excel"),
    path("api/clientes/", views.api_clientes_sala_cremas, name="api_clientes_sala_cremas"),
    path("api/productos/", views.api_productos_por_cliente_sala_cremas, name="api_productos_por_cliente_sala_cremas"),
    path("verificar/<int:pk>/", views.verificar_registro_sala_cremas, name="verificar_registro_sala_cremas"),
    path("selecciones/", views.redireccionar_selecciones_2, name="redireccionar_selecciones_2"),
]