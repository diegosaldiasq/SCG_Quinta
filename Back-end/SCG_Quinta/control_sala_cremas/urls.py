from django.urls import path
from . import views

app_name = "control_sala_cremas"

urlpatterns = [
    path("registro/", views.registro_sala_cremas, name="registro_sala_cremas"),
    path("historial/", views.historial_sala_cremas, name="historial_sala_cremas"),
    path("descargar-excel/", views.descargar_sala_cremas_excel, name="descargar_sala_cremas_excel"),
]