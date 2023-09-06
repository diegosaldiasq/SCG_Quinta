from django.urls import path

from . import views

urlpatterns = [
    path("", views.historial_termometro, name="historial_termometro")
]