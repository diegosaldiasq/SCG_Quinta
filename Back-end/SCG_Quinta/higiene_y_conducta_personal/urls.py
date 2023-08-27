from django.urls import path

from . import views

urlpatterns = [
    path("", views.higiene_y_conducta_personal, name="higiene_y_conducta_personal")
]