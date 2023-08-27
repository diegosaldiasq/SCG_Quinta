from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioHigieneConductaPersonal

# Create your views here.

def higiene_y_conducta_personal(request):
    if request.method == 'POST' and request.is_ajax():
        fecha_ingreso = request.POST.get('fecha_ingreso')
        nombre_personal = request.POST.get('nombre_personal')
        turno = request.POST.get('turno')
        planta = request.POST.get('planta')
        area = request.POST.get('area')
        cumplimiento = request.POST.get('cumplimiento')
        desviacion = request.POST.get('desviacion')
        accion_correctiva = request.POST.get('accion_correctiva')
        verificacion_accion_correctiva = request.POST.get('verificacion_accion_correctiva')
        observacion = request.POST.get('observacion')
        nombre_tecnologo = request.POST.get('nombre_tecnologo')

        datos = DatosFormularioHigieneConductaPersonal(
            fecha_ingreso=fecha_ingreso,
            nombre_personal=nombre_personal,
            turno=turno,
            planta=planta,
            area=area,
            cumplimiento=cumplimiento,
            desviacion=desviacion,
            accion_correctiva=accion_correctiva,
            verificacion_accion_correctiva=verificacion_accion_correctiva,
            observacion=observacion,
            nombre_tecnologo=nombre_tecnologo
            )
        datos.save()

        return JsonResponse({'mensaje': 'Datos guardados exitosamente'})