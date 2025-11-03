from django.urls import path

from . import views

urlpatterns = [
    path("", views.control_parametros_gorreri, name="control_parametros_gorreri"),
    path("vista_control_parametros_gorreri/", views.vista_control_parametros_gorreri, name="vista_control_parametros_gorreri"),
    path("selecciones/", views.redireccionar_selecciones_2, name="redireccionar_selecciones_2"),
    path('parametros/gorreri/', views.control_parametros_gorreri, name='control_parametros_gorreri'),
    path('parametros/gorreri/graficos/', views.graficos_parametros_gorreri, name='graficos_parametros_gorreri'),
    path('parametros/gorreri/api/', views.api_graficos_parametros_gorreri, name='api_graficos_parametros_gorreri'),
]