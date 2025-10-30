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
    path('descargar_resumenturnooee/', views.descargar_resumenturnooee, name='descargar_resumenturnooee'),
    path('api/resumen_turno_oee/opciones/', views.resumen_turno_oee_opciones, name='resumen_turno_oee_opciones'),
    path('api/resumen_turno_oee/', views.resumen_turno_oee_api, name='resumen_turno_oee_api'),
    path('graficos_oee/', views.graficos_oee, name='graficos_oee'),
    path('api/detenciones/', views.detenciones_turno_api, name='detenciones_turno_api'),
    path('graficos_detencion/', views.graficos_detencion, name='graficos_detencion'),
    path("graficos/panel-oee-detenciones/", views.panel_oee_y_detenciones, name="panel_oee_y_detenciones"),
    path('redireccionar_intermedio_4/', views.redireccionar_intermedio_4, name='redireccionar_intermedio_4')
]