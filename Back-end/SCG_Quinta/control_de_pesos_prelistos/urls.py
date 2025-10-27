from django.urls import path

from . import views

urlpatterns = [
    path("", views.control_de_pesos_prelistos, name="control_de_pesos_prelistos"),
    path("vista_control_de_pesos_prelistos/", views.vista_control_de_pesos_prelistos, name="vista_control_de_pesos_prelistos"),
    path("selecciones/", views.redireccionar_selecciones_2, name="redireccionar_selecciones_2"),
    path('prelistos/graficos/', views.graficos_control_pesos_prelistos, name='graficos_control_pesos_prelistos'),
    path('prelistos/api/productos/', views.api_productos_por_cliente_prelistos, name='api_productos_por_cliente_prelistos'),
    path('prelistos/api/datos/', views.api_graficos_control_pesos_prelistos, name='api_graficos_control_pesos_prelistos'),
    path('redireccionar_intermedio_4/', views.redireccionar_intermedio_4, name='redireccionar_intermedio_4')
]