from django.urls import path

from . import views

urlpatterns = [
    path("", views.calculo_oee, name="calculo_oee")
]