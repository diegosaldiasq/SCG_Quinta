from django.urls import path

from . import views

urlpatterns = [
    path("", views.pcc2_detector_metales, name="pcc2_detector_metales")
]