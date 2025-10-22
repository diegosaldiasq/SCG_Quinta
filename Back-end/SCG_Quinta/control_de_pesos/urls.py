from django.urls import path

from . import views

urlpatterns = [
    path("", views.control_de_pesos, name="control_de_pesos"),
    path("vista_control_de_pesos/", views.vista_control_de_pesos, name="vista_control_de_pesos"),
    path("selecciones/", views.redireccionar_selecciones_2, name="redireccionar_selecciones_2"),
    path('graficos/', views.graficos_control_pesos, name='graficos_control_pesos'),
    path('api/graficos_control_pesos/', views.api_graficos_control_pesos, name='api_graficos_control_pesos'),
    path('api/productos_por_cliente/', views.api_productos_por_cliente, name='api_productos_por_cliente'),
    path('redireccionar_intermedio_4/', views.redireccionar_intermedio_4, name='redireccionar_intermedio_4')
]