import json

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import DatosFormularioHigieneConductaPersonal


@login_required
def higiene_y_conducta_personal(request):
    return render(request, 'higiene_y_conducta_personal/r_higuiene_y_conducta_personal.html')


@login_required
@require_POST
def vista_higiene_y_conducta_personal(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({'existe': False, 'error': 'El contenido enviado no es JSON válido.'}, status=400)

    if not isinstance(data, dict):
        return JsonResponse({'existe': False, 'error': 'El formato enviado no es válido.'}, status=400)

    # Conservar compatibilidad con el formulario anterior de un solo registro.
    datos = data.get('datos') if 'datos' in data else [data.get('dato')]
    if not isinstance(datos, list) or not datos:
        return JsonResponse({'existe': False, 'error': 'Agrega al menos una fila de registro.'}, status=400)

    campos = {
        'nombre_personal': 'Nombre colaborador',
        'turno': 'Turno',
        'planta': 'Planta',
        'area': 'Área',
        'cumplimiento': 'Cumplimiento',
        'desviacion': 'Desviación',
        'accion_correctiva': 'AC',
        'verificacion_accion_correctiva': 'VAC',
        'observacion': 'Observación',
    }
    obligatorios = {'nombre_personal', 'turno', 'planta', 'area', 'cumplimiento'}
    registros = []
    for numero, dato in enumerate(datos, start=1):
        if not isinstance(dato, dict):
            return JsonResponse({'existe': False, 'error': f'La fila {numero} no es válida.'}, status=400)
        registro = {}
        for campo, etiqueta in campos.items():
            valor = dato.get(campo, '')
            if not isinstance(valor, str):
                return JsonResponse({'existe': False, 'error': f'Fila {numero}: {etiqueta} debe ser texto.'}, status=400)
            valor = valor.strip()
            if campo in obligatorios and valor in ('', 'blanco'):
                return JsonResponse({'existe': False, 'error': f'Fila {numero}: completa {etiqueta}.'}, status=400)
            registro[campo] = valor
        if len(registro['nombre_personal']) > 100:
            return JsonResponse({'existe': False, 'error': f'Fila {numero}: el nombre no puede superar 100 caracteres.'}, status=400)
        registros.append(registro)

    # Validar todo antes de escribir y deshacer el lote si falla alguna fila.
    fecha_ingreso = timezone.now()
    with transaction.atomic():
        for registro in registros:
            DatosFormularioHigieneConductaPersonal.objects.create(
                fecha_ingreso=fecha_ingreso,
                nombre_tecnologo=request.user.nombre_completo,
                **registro,
            )

    return JsonResponse({'existe': True, 'guardados': len(registros)})


@login_required
def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)