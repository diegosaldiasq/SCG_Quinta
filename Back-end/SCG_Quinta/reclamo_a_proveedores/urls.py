from django.urls import path

from . import views

urlpatterns = [
    path("", views.reclamo_a_proveedores, name="reclamo_a_proveedores")
]