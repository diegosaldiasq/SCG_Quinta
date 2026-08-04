from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioControlDePesosPrelistos
from control_de_pesos.models import ProductoControlPeso
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.db.models.functions import Upper, Trim

# Create your views here.

@login_required
def control_de_pesos_prelistos(request):
    return render(request, 'control_de_pesos_prelistos/r_control_de_pesos_prelistos.html')

@csrf_exempt
@login_required
def vista_control_de_pesos_prelistos(request):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'mensaje': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'mensaje': 'JSON inválido'}, status=400)

    dato = data.get('dato', None)
    if not dato:
        return JsonResponse({'ok': False, 'mensaje': 'No se recibió información'}, status=400)

    nombre_tecnologo = request.user.nombre_completo
    fecha_registro = timezone.now()

    cliente = dato.get('cliente')
    codigo_producto = dato.get('codigo_producto')
    producto = dato.get('producto')
    peso_receta = dato.get('peso_receta')
    lote = dato.get('lote')
    turno = dato.get('turno')
    muestras = dato.get('muestras', [])

    # Compatibilidad si alguna vez llega formato antiguo
    if not muestras and dato.get('peso_real') not in [None, ""]:
        muestras = [{'peso_real': dato.get('peso_real')}]

    if not cliente or not producto or not peso_receta or not lote or not turno:
        return JsonResponse({
            'ok': False,
            'mensaje': 'Faltan datos obligatorios'
        }, status=400)

    if not muestras:
        return JsonResponse({
            'ok': False,
            'mensaje': 'Debes ingresar al menos una muestra'
        }, status=400)

    guardados = 0

    for muestra in muestras:
        peso_real = muestra.get('peso_real')

        if peso_real in [None, ""]:
            continue

        DatosFormularioControlDePesosPrelistos.objects.create(
            nombre_tecnologo=nombre_tecnologo,
            fecha_registro=timezone.now(),
            cliente=cliente,
            codigo_producto=codigo_producto,
            producto=producto,
            peso_receta=int(peso_receta),
            peso_real=int(float(peso_real)),
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
def graficos_control_pesos_prelistos(request):
    """
    Render del template de gráficos de control de pesos PRELISTOS.
    """
    clientes = (DatosFormularioControlDePesosPrelistos.objects
                .order_by()
                .values_list('cliente', flat=True)
                .distinct())
    turnos = (DatosFormularioControlDePesosPrelistos.objects
              .order_by()
              .values_list('turno', flat=True)
              .distinct())

    ctx = {
        'clientes': [c for c in clientes if c],
        'turnos': [t for t in turnos if t],
    }
    return render(request, 'control_de_pesos_prelistos/graficos_control_pesos_prelistos.html', ctx)


@login_required
@require_GET
def api_productos_por_cliente_prelistos(request):
    """
    Devuelve lista de productos por cliente (tolerante a mayúsculas/espacios).
    GET ?cliente=Jumbo
    """
    cliente = (request.GET.get('cliente') or '').strip()
    if not cliente:
        return JsonResponse({'ok': True, 'productos': []})

    qs = (DatosFormularioControlDePesosPrelistos.objects
          .annotate(cliente_norm=Upper(Trim('cliente')))
          .filter(cliente_norm=cliente.upper())
          .order_by()
          .values('producto', 'codigo_producto')
          .distinct())

    data = [{'producto': r['producto'], 'codigo': r['codigo_producto']}
            for r in qs if (r['producto'] or '').strip()]
    return JsonResponse({'ok': True, 'productos': data})


@login_required
@require_GET
def api_graficos_control_pesos_prelistos(request):
    qs = DatosFormularioControlDePesosPrelistos.objects.all()

    cliente = (request.GET.get('cliente') or '').strip()
    producto = (request.GET.get('producto') or '').strip()
    turno = (request.GET.get('turno') or '').strip()
    lote = (request.GET.get('lote') or '').strip()
    desde = (request.GET.get('desde') or '').strip()
    hasta = (request.GET.get('hasta') or '').strip()

    if cliente:
        qs = qs.filter(cliente__icontains=cliente)

    if producto:
        qs = qs.filter(producto__iexact=producto)

    if turno:
        qs = qs.filter(turno__iexact=turno)

    if lote:
        qs = qs.filter(lote__iexact=lote)

    if desde:
        try:
            dt_desde = datetime.fromisoformat(desde)
            qs = qs.filter(
                fecha_registro__date__gte=dt_desde.date()
            )
        except (TypeError, ValueError):
            pass

    if hasta:
        try:
            dt_hasta = datetime.fromisoformat(hasta)
            qs = qs.filter(
                fecha_registro__date__lte=dt_hasta.date()
            )
        except (TypeError, ValueError):
            pass

    qs = qs.order_by('fecha_registro').values(
        'id',
        'fecha_registro',
        'cliente',
        'producto',
        'codigo_producto',
        'peso_receta',
        'peso_real',
        'lote',
        'turno',
    )

    registros = []

    for r in qs:
        producto_base = ProductoControlPeso.objects.filter(
            area='PRELISTOS',
            cliente__iexact=r['cliente'],
            codigo=r['codigo_producto'],
            producto__iexact=r['producto'],
            activo=True,
        ).first()

        # En ProductoControlPeso, peso_receta corresponde al peso neto.
        peso_neto = (
            int(producto_base.peso_receta)
            if producto_base
            else (
                int(r['peso_receta'])
                if r['peso_receta'] is not None
                else None
            )
        )

        porcentaje_perdida = (
            float(producto_base.porcentaje_perdida)
            if producto_base
            else 0
        )

        # Peso que debe prepararse antes de la pérdida operacional.
        peso_receta = None

        if (
            peso_neto is not None
            and 0 <= porcentaje_perdida < 100
        ):
            peso_receta = round(
                peso_neto
                / (1 - porcentaje_perdida / 100),
                2,
            )

        peso_real = (
            int(r['peso_real'])
            if r['peso_real'] is not None
            else None
        )

        desviacion = None

        if peso_real is not None and peso_neto is not None:
            if peso_receta is not None:
                if peso_neto <= peso_real <= peso_receta:
                    desviacion = 0
                elif peso_real < peso_neto:
                    desviacion = peso_real - peso_neto
                else:
                    desviacion = peso_real - peso_receta
            else:
                desviacion = peso_real - peso_neto

        registros.append({
            'id': r['id'],
            'ts': r['fecha_registro'].isoformat(),
            'cliente': r['cliente'],
            'producto': r['producto'],
            'codigo_producto': r['codigo_producto'],

            'peso_neto': peso_neto,
            'peso_minimo': peso_neto,
            'peso_receta': peso_receta,
            'peso_maximo': peso_receta,
            'perdida_operacional': porcentaje_perdida,

            'peso_real': peso_real,
            'desviacion': desviacion,
            'lote': r['lote'],
            'turno': r['turno'],
        })

    return JsonResponse({
        'ok': True,
        'registros': registros,
    })

@login_required
def redireccionar_intermedio_4(request):
    url_intermedio = reverse('intermedio_4')
    return HttpResponseRedirect(url_intermedio)
