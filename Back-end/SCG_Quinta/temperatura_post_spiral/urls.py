from django.urls import path
from . import views

app_name = 'temperatura_post_spiral'

urlpatterns = [
    path('', views.registrar_temperatura, name='registrar'),
    path('historial/', views.historial, name='historial'),
    path('detalle/<int:pk>/', views.detalle_registro, name='detalle'),

    path('verificar-accion/<int:pk>/', views.verificar_accion_correctiva, name='verificar_accion'),
    path('verificar-final/<int:pk>/', views.verificar_final, name='verificar_final'),

    path('api/productos-por-cliente/', views.api_productos_por_cliente, name='api_productos_por_cliente'),

    path('descargar/', views.descargar_excel, name='descargar_excel'),
]