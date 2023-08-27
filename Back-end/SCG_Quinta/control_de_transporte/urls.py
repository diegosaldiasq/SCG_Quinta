from django.urls import path

from . import views

urlpatterns = [
    path("", views.control_de_transporte, name="control_de_transporte")
]