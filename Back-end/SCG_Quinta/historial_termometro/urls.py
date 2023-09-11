from django.urls import path

from . import views

urlpatterns = [
    path("", views.historial_termometro, name="historial_termometro"),
    path("vista_historial_termometro/", views.vista_historial_termometro, name="vista_historial_termometro_app2")
]