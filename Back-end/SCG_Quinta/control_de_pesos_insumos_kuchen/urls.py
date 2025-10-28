from django.urls import path

from . import views

urlpatterns = [
    path("", views.control_de_pesos_insumos_kuchen, name="control_de_pesos_insumos_kuchen"),
    path("vista_control_de_pesos_insumos_kuchen/", views.vista_control_de_pesos_insumos_kuchen, name="vista_control_de_pesos_insumos_kuchen"),
    path("selecciones/", views.redireccionar_selecciones_2, name="redireccionar_selecciones_2"),
    path("control-de-pesos/insumos-kuchen/graficos/", views.graficos_control_pesos_insumos_kuchen, name="graficos_control_pesos_insumos_kuchen"),
    path("api/control-de-pesos/insumos-kuchen/productos/", views.api_productos_por_cliente_insumos_kuchen, name="api_productos_por_cliente_insumos_kuchen"),
    path("api/control-de-pesos/insumos-kuchen/graficos/", views.api_graficos_control_pesos_insumos_kuchen, name="api_graficos_control_pesos_insumos_kuchen"),
    path('redireccionar_intermedio_4/', views.redireccionar_intermedio_4, name='redireccionar_intermedio_4')
]