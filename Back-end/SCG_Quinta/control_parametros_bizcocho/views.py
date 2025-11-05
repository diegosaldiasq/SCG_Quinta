from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioControlParametrosBizcocho
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import Upper, Trim
from django.views.decorators.http import require_GET

# Create your views here.

@login_required
def control_parametros_bizcocho(request):
    return render(request, 'control_parametros_bizcocho/r_control_parametros_bizcocho.html')    

@csrf_exempt
@login_required 
def vista_control_parametros_bizcocho(request): 
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            dato = data.get('dato', None)
            if dato:
                try:
                    nombre_tecnologo = request.user.nombre_completo
                    fecha_registro = timezone.now()
                    proveedor = dato.get('proveedor')
                    producto = dato.get('producto')
                    cantidad_agua = float(dato.get('cantidad_agua'))
                    cantidad_huevo = float(dato.get('cantidad_huevo'))
                    velocidad_bomba = int(dato.get('velocidad_bomba'))
                    velocidad_turbo = int(dato.get('velocidad_turbo'))
                    contrapresion = float(dato.get('contrapresion'))
                    contrapresion_trasera = float(dato.get('contrapresion_trasera'))
                    inyeccion_de_aire = int(dato.get('inyeccion_de_aire'))
                    densidad = float(dato.get('densidad'))
                    t_final = float(dato.get('t_final'))
                    lote = dato.get('lote')
                    turno = dato.get('turno')
    
                    datos = DatosFormularioControlParametrosBizcocho(
                        nombre_tecnologo=nombre_tecnologo,
                        fecha_registro=fecha_registro,
                        proveedor=proveedor,
                        producto=producto,
                        cantidad_agua=cantidad_agua,
                        cantidad_huevo=cantidad_huevo,
                        velocidad_bomba=velocidad_bomba,
                        velocidad_turbo=velocidad_turbo,
                        contrapresion=contrapresion,
                        contrapresion_trasera=contrapresion_trasera,
                        inyeccion_de_aire=inyeccion_de_aire,
                        densidad=densidad,
                        t_final=t_final,
                        lote=lote,
                        turno=turno
                        )
                    datos.save()
    
                    return JsonResponse({'existe': True})   
                except Exception as e:
                    return JsonResponse({'existe': False, 'error': str(e)}) 

            else:
                return JsonResponse({'existe': False, 'error': 'No se recibieron datos.'})
        else:
            return JsonResponse({'existe': False, 'error': 'Método no permitido.'})     
        
@login_required
def redireccionar_selecciones_2(request):
    url_selecciones = reverse('vista_selecciones_2')
    return HttpResponseRedirect(url_selecciones)

@login_required
@require_GET
def api_graficos_control_parametros_bizcocho(request):
    """
    Devuelve los registros filtrados para graficar parámetros de bizcocho.
    Filtros: ?proveedor=&producto=&turno=&lote=&desde=YYYY-MM-DD&hasta=YYYY-MM-DD
    """
    qs = (
        DatosFormularioControlParametrosBizcocho.objects
        .annotate(
            proveedor_norm=Upper(Trim('proveedor')),
            producto_norm=Upper(Trim('producto')),
            turno_norm=Upper(Trim('turno')),
            lote_norm=Trim('lote'),
        )
    )

    proveedor = (request.GET.get('proveedor') or '').strip()
    producto  = (request.GET.get('producto')  or '').strip()
    turno     = (request.GET.get('turno')     or '').strip()
    lote      = (request.GET.get('lote')      or '').strip()
    desde     = (request.GET.get('desde')     or '').strip()
    hasta     = (request.GET.get('hasta')     or '').strip()

    # puedes dejar proveedor “laxo” si escriben distinto
    if proveedor:
        qs = qs.filter(proveedor_norm__contains=proveedor.upper())

    # producto: si quieres evitar que mezcle “media…” con “torta…”, cámbialo a = en vez de contains
    if producto:
        qs = qs.filter(producto_norm=producto.upper())

    if turno:
        qs = qs.filter(turno_norm=turno.upper())

    if lote:
        qs = qs.filter(lote_norm=lote)

    if desde:
        try:
            dt_desde = datetime.fromisoformat(desde)
            qs = qs.filter(fecha_registro__date__gte=dt_desde.date())
        except Exception:
            pass

    if hasta:
        try:
            dt_hasta = datetime.fromisoformat(hasta)
            qs = qs.filter(fecha_registro__date__lte=dt_hasta.date())
        except Exception:
            pass

    qs = qs.order_by('fecha_registro').values(
        'id', 'fecha_registro', 'proveedor', 'producto',
        'cantidad_agua', 'cantidad_huevo',
        'velocidad_bomba', 'velocidad_turbo',
        'contrapresion', 'contrapresion_trasera',
        'inyeccion_de_aire', 'densidad', 't_final',
        'lote', 'turno'
    )

    registros = []
    for r in qs:
        registros.append({
            'id': r['id'],
            'ts': r['fecha_registro'].isoformat(),
            'proveedor': r['proveedor'],
            'producto': r['producto'],
            'cantidad_agua': r['cantidad_agua'],
            'cantidad_huevo': r['cantidad_huevo'],
            'velocidad_bomba': r['velocidad_bomba'],
            'velocidad_turbo': r['velocidad_turbo'],
            'contrapresion': r['contrapresion'],
            'contrapresion_trasera': r['contrapresion_trasera'],
            'inyeccion_de_aire': r['inyeccion_de_aire'],
            'densidad': r['densidad'],
            't_final': r['t_final'],
            'lote': r['lote'],
            'turno': r['turno'],
        })

    return JsonResponse({'ok': True, 'registros': registros})   

@login_required
def graficos_control_parametros_bizcocho(request):
    return render(request, 'control_parametros_bizcocho/graficos_control_parametros_bizcocho.html')