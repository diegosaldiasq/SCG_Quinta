from django.urls import path

from . import views

urlpatterns = [
    path("", views.informe_de_incidentes, name="informe_de_incidentes")
]