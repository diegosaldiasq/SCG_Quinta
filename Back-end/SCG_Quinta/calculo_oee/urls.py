from django.urls import path
from django.http import HttpResponse
from django.shortcuts import render, redirect

from . import views

urlpatterns = [
    #path("", views.calculo_oee, name="calculo_oee"),
    path('crear_turno/', views.crear_turno, name='crear_turno'),
    path('turno-exito/', lambda request: HttpResponse("Turno registrado con éxito."), name='turno_exito'),
    path('resumen/<int:lote_id>/', views.resumen_turno, name='resumen_turno'),
    path('cerrar_turno/<int:lote_id>/', views.cerrar_turno, name='cerrar_turno'),
    path('lista_turnos/', views.lista_turnos, name='lista_turnos'),
    path('detalle_turno/<int:lote_id>/', views.detalle_turno, name='detalle_turno'),
    path('marcar_verificado/<int:lote_id>/', views.marcar_verificado, name='marcar_verificado'),
    path('redireccionar_intermedio/', views.redireccionar_intermedio, name='redireccionar_intermedio'),
    path('descargar_resumenturnooee/', views.descargar_resumenturnooee, name='descargar_resumenturnooee')
]