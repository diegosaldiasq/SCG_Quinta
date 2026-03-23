from django.urls import path
from . import views

app_name = 'ventas_geo'

urlpatterns = [
    path('cargar/', views.cargar_ventas, name='cargar_ventas'),
    path('resultado/<int:carga_id>/', views.resultado_carga, name='resultado_carga'),
    path('dashboard/', views.dashboard_ventas_geo, name='dashboard'),
]