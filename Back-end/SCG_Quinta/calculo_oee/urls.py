from django.urls import path

from . import views

urlpatterns = [
    path("", views.calculo_oee, name="calculo_oee"),
    path('turno-exito/', lambda request: HttpResponse("Turno registrado con éxito."), name='turno_exito'),
    path('resumen/<int:turno_id>/', views.resumen_turno, name='resumen_turno'),
    path('cerrar-turno/<int:turno_id>/', views.cerrar_turno, name='cerrar_turno')
]