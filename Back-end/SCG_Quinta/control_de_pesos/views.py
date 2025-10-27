from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioControlDePesos
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.db.models.functions import Trim, Upper
from django.db.models import Value

# Create your views here.

@login_required
def control_de_pesos(request):
    return render(request, 'control_de_pesos/r_control_de_pesos.html')

@csrf_exempt
@login_required 
def vista_control_de_pesos(request):
     if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        dato = data.get('dato', None)
        if dato:
            nombre_tecnologo = request.user.nombre_completo
            fecha_registro = timezone.now()
            cliente = dato.get('cliente')
            codigo_producto = dato.get('codigo_producto')
            producto = dato.get('producto')
            peso_receta = dato.get('peso_receta')
            peso_real = dato.get('peso_real')
            lote = dato.get('lote')
            turno = dato.get('turno')

            datos = DatosFormularioControlDePesos(
                nombre_tecnologo=nombre_tecnologo,
                fecha_registro=fecha_registro,
                cliente=cliente,
                codigo_producto=codigo_producto,
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

@login_required
def graficos_control_pesos(request):
    """
    Render del template de gráficos de control de pesos.
    """
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
    """
    Retorna productos por cliente (tolerante a mayúsculas/espacios y variantes).
    GET ?cliente=Walmart
    """
    cliente = (request.GET.get('cliente') or '').strip()
    if not cliente:
        return JsonResponse({'ok': True, 'productos': []})

    qs = (
        DatosFormularioControlDePesos.objects
        .annotate(cliente_norm=Upper(Trim('cliente')))
        .filter(cliente_norm__contains=cliente.upper())  # laxo: soporta 'WALMART - LIDER'
        .order_by()
        .values('producto', 'codigo_producto')
        .distinct()
    )

    data = [
        {'producto': (r['producto'] or '').strip(), 'codigo': r['codigo_producto']}
        for r in qs if (r['producto'] or '').strip()
    ]
    return JsonResponse({'ok': True, 'productos': data})


@login_required
@require_GET
def api_graficos_control_pesos(request):
    """
    Datos para las gráficas.
    Filtros: ?cliente=&producto=&turno=&lote=&desde=YYYY-MM-DD&hasta=YYYY-MM-DD
    Cliente/Producto: contains (normalizados); Turno/Lote: exacto; Fechas por date.
    """
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
    turno    = (request.GET.get('turno') or '').strip()
    lote     = (request.GET.get('lote') or '').strip()
    desde    = (request.GET.get('desde') or '').strip()
    hasta    = (request.GET.get('hasta') or '').strip()

    if cliente:
        qs = qs.filter(cliente_norm__contains=cliente.upper())
    if producto:
        qs = qs.filter(producto_norm__contains=producto.upper())
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
        'id', 'fecha_registro', 'cliente', 'producto', 'codigo_producto',
        'peso_receta', 'peso_real', 'lote', 'turno'
    )

    registros = []
    for r in qs:
        # coerción defensiva (por si en BD hay nulls)
        peso_receta = int(r['peso_receta']) if r['peso_receta'] is not None else None
        peso_real   = int(r['peso_real'])   if r['peso_real']   is not None else None
        registros.append({
            'id': r['id'],
            'ts': r['fecha_registro'].isoformat(),
            'cliente': r['cliente'],
            'producto': r['producto'],
            'codigo_producto': r['codigo_producto'],
            'peso_receta': peso_receta,
            'peso_real':   peso_real,
            'desviacion': (peso_real or 0) - (peso_receta or 0),
            'lote': r['lote'],
            'turno': r['turno'],
        })

    return JsonResponse({'ok': True, 'registros': registros})

@login_required
def redireccionar_intermedio_4(request):
    url_intermedio = reverse('intermedio_4')
    return HttpResponseRedirect(url_intermedio)