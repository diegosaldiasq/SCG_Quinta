from django.urls import path
from django.http import HttpResponse
from django.shortcuts import render, redirect

from . import views

urlpatterns = [
    #path("", views.calculo_oee, name="calculo_oee"),
    path('crear_turno/', views.crear_turno, name='crear_turno'),
    path('turno-exito/', lambda request: HttpResponse("Turno registrado con éxito."), name='turno_exito'),
    path('resumen/<int:turno_id>/', views.resumen_turno, name='resumen_turno'),
    path('cerrar_turno/<int:turno_id>/', views.cerrar_turno, name='cerrar_turno'),
    path('lista_turnos/', views.lista_turnos, name='lista_turnos'),
    path('detalle-turno/<int:turno_id>/', views.detalle_turno, name='detalle_turno'),
    path('marcar-verificado/<int:turno_id>/', views.marcar_verificado, name='marcar_verificado'),
    path('intermedio/', views.imtermedio, name='intermedio')
]