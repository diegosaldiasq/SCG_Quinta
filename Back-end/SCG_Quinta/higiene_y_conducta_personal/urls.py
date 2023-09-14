from django.urls import path

from . import views

urlpatterns = [
    path("", views.higiene_y_conducta_personal, name="higiene_y_conducta_personal"),
    path("", views.vista_higiene_y_conducta_personal, name="vista_higiene_y_conducta_personal"),
    path("selecciones/", views.redireccionar_selecciones, name="redireccionar_selecciones")
]