from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioControlDePesos
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
import json

# Create your views here.

@login_required
def control_de_pesos(request):
    return render(request, 'control_de_pesos/r_control_de_pesos.html')

@login_required
def vista_control_de_pesos(request):
     if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        dato = data.get('dato', None)
        if dato:
            nombre_tecnologo = request.user.nombre_completo
            fecha_registro = timezone.now()
            cliente = dato.get('cliente')
            producto = dato.get('producto')
            peso_receta = dato.get('peso_receta')
            peso_real = dato.get('peso_real')
            lote = dato.get('lote')
            turno = dato.get('turno')

            datos = DatosFormularioControlDePesos(
                nombre_tecnologo=nombre_tecnologo,
                fecha_registro=fecha_registro,
                cliente=cliente,
                producto=producto,
                peso_receta=peso_receta,
                peso_real=peso_real,
                lote=lote,
                turno=turno
                )
            datos.save()

            return JsonResponse({'existe': True})
        else:
            return JsonResponse({'existe': False})

@login_required
def redireccionar_selecciones_2(request):
    url_selecciones = reverse('vista_selecciones_2')
    return HttpResponseRedirect(url_selecciones)


