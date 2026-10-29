from django.urls import path

from . import views, weekly_views

app_name = "productividad_turnos"
urlpatterns = [
    path("", views.panel, name="inicio"),
    path("diario/", views.panel, {"periodo": "dia"}, name="diario"),
    path("semanal/", views.panel, {"periodo": "semana"}, name="semanal"),
    path("registrar/", views.seleccionar, name="seleccionar"),
    path("historial/", views.historial, name="historial"),
    path("programacion/", views.programacion, name="programacion"),
    path("programacion-semanal/", weekly_views.programacion_semanal, name="programacion_semanal"),
    path("programacion/<int:pk>/", views.programacion, name="editar_programacion"),
    path("registro/<int:pk>/", views.registro, name="registro"),
    path("registro/<int:pk>/verificar/", views.verificar, name="verificar"),
    path("registro/<int:pk>/reabrir/", views.reabrir, name="reabrir"),
    path("api/resumen/", views.api_resumen, name="api_resumen"),
    path("exportar/", views.exportar, name="exportar"),
]