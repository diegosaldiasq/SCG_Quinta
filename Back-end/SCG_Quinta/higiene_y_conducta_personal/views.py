from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioHigieneConductaPersonal
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import json

# Create your views here.

@login_required
def higiene_y_conducta_personal(request):
    return render(request, 'higiene_y_conducta_personal/r_higuiene_y_conducta_personal.html')

@login_required
def vista_higiene_y_conducta_personal(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        dato = data.get('dato', None)
        if dato:
            fecha_ingreso = timezone.now()
            nombre_personal = dato.get('nombre_personal')
            turno = dato.get('turno')
            planta = dato.get('planta')
            area = dato.get('area')
            cumplimiento = dato.get('cumplimiento')
            desviacion = dato.get('desviacion')
            accion_correctiva = dato.get('accion_correctiva')
            verificacion_accion_correctiva = dato.get('verificacion_accion_correctiva')
            observacion = dato.get('observacion')
            nombre_tecnologo = request.user.nombre_completo

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

            return JsonResponse({'existe': True})
        else:
            return JsonResponse({'existe': False})

@login_required
def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)