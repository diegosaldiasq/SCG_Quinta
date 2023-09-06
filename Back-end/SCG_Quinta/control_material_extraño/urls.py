from django.urls import path

from . import views

urlpatterns = [
    path("", views.control_material_extraño, name="control_material_extraño")
]