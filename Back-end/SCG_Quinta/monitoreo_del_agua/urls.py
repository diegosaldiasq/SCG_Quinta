from django.urls import path

from . import views

urlpatterns = [
    path("", views.monitoreo_del_agua, name="monitoreo_del_agua")
]