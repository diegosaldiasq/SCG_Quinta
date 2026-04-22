from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.db.models.functions import Trim, Upper
import json

from .models import DatosFormularioControlDePesos


@login_required
def control_de_pesos(request):
    return render(request, 'control_de_pesos/r_control_de_pesos.html')


@csrf_exempt
@login_required
def vista_control_de_pesos(request):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'mensaje': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'mensaje': 'JSON inválido'}, status=400)

    dato = data.get('dato', None)
    if not dato:
        return JsonResponse({'ok': False, 'mensaje': 'No se recibió información'}, status=400)

    cliente = dato.get('cliente')
    codigo_producto = dato.get('codigo_producto')
    producto = dato.get('producto')
    peso_receta = dato.get('peso_receta')
    lote = dato.get('lote')
    turno = dato.get('turno')

    muestras = dato.get('muestras', [])

    # Compatibilidad por si viene el formato antiguo
    if not muestras and dato.get('peso_real') not in [None, ""]:
        muestras = [{
            'peso_real': dato.get('peso_real'),
            'altura': dato.get('altura')
        }]

    if not cliente or not producto or not peso_receta or not lote or not turno:
        return JsonResponse({
            'ok': False,
            'mensaje': 'Faltan datos obligatorios del encabezado'
        }, status=400)

    if not muestras:
        return JsonResponse({
            'ok': False,
            'mensaje': 'Debes ingresar al menos una muestra'
        }, status=400)

    nombre_tecnologo = getattr(request.user, 'nombre_completo', None) or request.user.username
    guardados = 0

    for muestra in muestras:
        peso_real = muestra.get('peso_real')
        altura = muestra.get('altura')

        if peso_real in [None, ""]:
            continue

        DatosFormularioControlDePesos.objects.create(
            nombre_tecnologo=nombre_tecnologo,
            fecha_registro=timezone.now(),
            cliente=cliente,
            codigo_producto=codigo_producto,
            producto=producto,
            peso_receta=int(peso_receta),
            peso_real=int(float(peso_real)),
            altura=float(altura) if altura not in [None, ""] else None,
            lote=lote,
            turno=turno
        )
        guardados += 1

    if guardados == 0:
        return JsonResponse({
            'ok': False,
            'mensaje': 'No se guardó ninguna muestra válida'
        }, status=400)

    return JsonResponse({
        'ok': True,
        'existe': True,
        'mensaje': f'Se guardaron {guardados} muestra(s) correctamente'
    })


@login_required
def redireccionar_selecciones_2(request):
    url_selecciones = reverse('vista_selecciones_2')
    return HttpResponseRedirect(url_selecciones)


@login_required
def graficos_control_pesos(request):
    clientes = DatosFormularioControlDePesos.objects.order_by().values_list('cliente', flat=True).distinct()
    turnos = DatosFormularioControlDePesos.objects.order_by().values_list('turno', flat=True).distinct()

    ctx = {
        'clientes': [c for c in clientes if c],
        'turnos': [t for t in turnos if t],
    }
    return render(request, 'control_de_pesos/graficos_control_pesos.html', ctx)


@login_required
@require_GET
def api_productos_por_cliente(request):
    cliente = (request.GET.get('cliente') or '').strip()
    if not cliente:
        return JsonResponse({'ok': True, 'productos': []})

    qs = (
        DatosFormularioControlDePesos.objects
        .annotate(cliente_norm=Upper(Trim('cliente')))
        .filter(cliente_norm__contains=cliente.upper())
        .order_by()
        .values('producto', 'codigo_producto')
        .distinct()
    )

    data = [
        {
            'producto': (r['producto'] or '').strip(),
            'codigo': r['codigo_producto']
        }
        for r in qs if (r['producto'] or '').strip()
    ]
    return JsonResponse({'ok': True, 'productos': data})


@login_required
@require_GET
def api_graficos_control_pesos(request):
    qs = (
        DatosFormularioControlDePesos.objects
        .annotate(
            cliente_norm=Upper(Trim('cliente')),
            producto_norm=Upper(Trim('producto')),
            turno_norm=Upper(Trim('turno')),
            lote_norm=Trim('lote'),
        )
    )

    cliente = (request.GET.get('cliente') or '').strip()
    producto = (request.GET.get('producto') or '').strip()
    turno = (request.GET.get('turno') or '').strip()
    lote = (request.GET.get('lote') or '').strip()
    desde = (request.GET.get('desde') or '').strip()
    hasta = (request.GET.get('hasta') or '').strip()

    if cliente:
        qs = qs.filter(cliente_norm__contains=cliente.upper())

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
        'id',
        'fecha_registro',
        'cliente',
        'producto',
        'codigo_producto',
        'peso_receta',
        'peso_real',
        'altura',
        'lote',
        'turno'
    )

    registros = []
    for r in qs:
        peso_receta = int(r['peso_receta']) if r['peso_receta'] is not None else None
        peso_real = int(r['peso_real']) if r['peso_real'] is not None else None
        altura = int(r['altura']) if r['altura'] is not None else None

        registros.append({
            'id': r['id'],
            'ts': r['fecha_registro'].isoformat(),
            'cliente': r['cliente'],
            'producto': r['producto'],
            'codigo_producto': r['codigo_producto'],
            'peso_receta': peso_receta,
            'peso_real': peso_real,
            'altura': altura,
            'desviacion': (peso_real or 0) - (peso_receta or 0),
            'lote': r['lote'],
            'turno': r['turno'],
        })

    return JsonResponse({'ok': True, 'registros': registros})


@login_required
def redireccionar_intermedio_4(request):
    url_intermedio = reverse('intermedio_4')
    return HttpResponseRedirect(url_intermedio)