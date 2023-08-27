from django.urls import path

from . import views

urlpatterns = [
    path("", views.recepcion_mpme, name="recepcion_mpme")
]