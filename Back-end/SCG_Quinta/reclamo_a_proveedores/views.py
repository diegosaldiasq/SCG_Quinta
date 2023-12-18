from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioReclamoProveedores
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
import json

# Create your views here.

@login_required
def reclamo_a_proveedores(request):
    return render(request, 'reclamo_a_proveedores/r_informe_reclamo_a_proveedores.html')

@login_required
def vista_reclamo_a_proveedores(request):
    if request.method == 'POST':
        nombre_tecnologo = request.user.nombre_completo
        fecha_registro = timezone.now()
        nombre_proveedor = request.POST.get('nombre_proveedor')
        fecha_reclamo = timezone.make_aware(datetime.strptime(request.POST.get('fecha_reclamo'), '%Y-%m-%d'), timezone=timezone.utc)
        nombre_del_producto = request.POST.get('nombre_del_producto')
        fecha_elaboracion = timezone.make_aware(datetime.strptime(request.POST.get('fecha_elaboracion'), '%Y-%m-%d'), timezone=timezone.utc)
        lote = request.POST.get('lote')
        fecha_vencimiento = timezone.make_aware(datetime.strptime(request.POST.get('fecha_vencimiento'), '%Y-%m-%d'), timezone=timezone.utc)
        no_conformidad = request.POST.get('no_conformidad')
        clasificacion = request.POST.get('clasificacion')
        cantidad_involucrada = request.POST.get('cantidad_involucrada')
        unidad_de_medida = request.POST.get('unidad_de_medida')
        archivo_foto = request.FILES.get('archivo_foto')
        
        print(archivo_foto)

        datos = DatosFormularioReclamoProveedores(
            nombre_tecnologo=nombre_tecnologo,
            fecha_registro=fecha_registro,
            nombre_proveedor=nombre_proveedor,
            fecha_reclamo=fecha_reclamo,
            nombre_del_producto=nombre_del_producto,
            fecha_elaboracion=fecha_elaboracion,
            lote=lote,
            fecha_vencimiento=fecha_vencimiento,
            no_conformidad=no_conformidad,
            clasificacion=clasificacion,
            cantidad_involucrada=cantidad_involucrada,
            unidad_de_medida=unidad_de_medida,
            archivo_foto=archivo_foto
            )
        datos.save()

        return JsonResponse({'existe': True})
    else:
        return JsonResponse({'existe': False})

@login_required
def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)
