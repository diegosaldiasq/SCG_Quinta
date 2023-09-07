from django.urls import path

from . import views

urlpatterns = [
    path("", views.rechazo_mp_in_me, name="rechazo_mp_in_me")
]