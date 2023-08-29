from django.urls import path

from . import views

urlpatterns = [
    path("", views.temperatura_despacho_ptjumbo, name="temperatura_despacho_ptjumbo")
]