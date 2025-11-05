from django.urls import path

from . import views

urlpatterns = [
    path("", views.control_parametros_bizcocho, name="control_parametros_bizcocho"),
    path("vista_control_parametros_bizcocho/", views.vista_control_parametros_bizcocho, name="vista_control_parametros_bizcocho"),
    path("selecciones/", views.redireccionar_selecciones_2, name="redireccionar_selecciones_2"),
    path('api/graficos-control-parametros-bizcocho/', views.api_graficos_control_parametros_bizcocho, name='api_graficos_control_parametros_bizcocho'),
    path('graficos-control-parametros-bizcocho/', views.graficos_control_parametros_bizcocho, name='graficos_control_parametros_bizcocho'),
    path('intermedio-4/', views.redireccionar_intermedio_4, name='redireccionar_intermedio_4'),
    path('api/productos-por-proveedor/', views.api_productos_por_proveedor, name='api_productos_por_proveedor'),
]