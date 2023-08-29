from django.urls import path

from . import views

urlpatterns = [
    path("", views.temperatura_despacho_ptsisa, name="temperatura_despacho_ptsisa")
]