from django.urls import path

from . import views

urlpatterns = [
    path("", views.control_parametros_bizcocho, name="control_parametros_bizcocho"),
    path("vista_control_parametros_bizcocho/", views.vista_control_parametros_bizcocho, name="vista_control_parametros_bizcocho"),
    path("selecciones/", views.redireccionar_selecciones_2, name="redireccionar_selecciones_2"),
    path('api/graficos-control-parametros-bizcocho/', views.api_graficos_control_parametros_bizcocho, name='api_graficos_control_parametros_bizcocho'),
]