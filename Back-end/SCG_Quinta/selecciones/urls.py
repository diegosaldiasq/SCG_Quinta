from django.urls import path

from . import views

urlpatterns = [
    path("selecciones/", views.redireccionar_historial_termometro, name='redireccionar_historial_termometro')
]
