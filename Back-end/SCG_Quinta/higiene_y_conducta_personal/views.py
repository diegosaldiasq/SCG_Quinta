from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioHigieneConductaPersonal
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime

# Create your views here.

def higiene_y_conducta_personal(request):
    return render(request, 'higiene_y_conducta_personal/r_higuiene_y_conducta_personal.html')

def vista_higiene_y_conducta_personal(request):
    if request.method == 'POST':
        fecha_ingreso = timezone.make_aware(datetime.strptime(request.POST.get('fecha_ingreso'), '%Y-%m-%dT%H:%M'), timezone=timezone.utc)
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

def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)