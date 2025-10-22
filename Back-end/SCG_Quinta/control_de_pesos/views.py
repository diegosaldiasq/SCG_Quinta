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
    # Opcional: valores únicos para filtros rápidos (cliente, turno, etc.)
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
    Devuelve lista de productos y códigos disponibles para un cliente (para poblar el combo Producto).
    GET ?cliente=Jumbo
    """
    cliente = request.GET.get('cliente', '')
    qs = DatosFormularioControlDePesos.objects.filter(cliente=cliente).order_by().values('producto', 'codigo_producto').distinct()
    data = [{'producto': r['producto'], 'codigo': r['codigo_producto']} for r in qs if r['producto']]
    return JsonResponse({'ok': True, 'productos': data})


@login_required
@require_GET
def api_graficos_control_pesos(request):
    """
    Endpoint de datos para las gráficas.
    Filtros por ?cliente=&producto=&turno=&lote=&desde=YYYY-MM-DD&hasta=YYYY-MM-DD
    """
    qs = DatosFormularioControlDePesos.objects.all()

    cliente = request.GET.get('cliente', '').strip()
    producto = request.GET.get('producto', '').strip()
    turno = request.GET.get('turno', '').strip()
    lote = request.GET.get('lote', '').strip()
    desde = request.GET.get('desde', '').strip()
    hasta = request.GET.get('hasta', '').strip()

    if cliente:
        qs = qs.filter(cliente=cliente)
    if producto:
        qs = qs.filter(producto=producto)
    if turno:
        qs = qs.filter(turno=turno)
    if lote:
        qs = qs.filter(lote=lote)
    if desde:
        # Interpretar como fecha local a medianoche
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

    # Orden por tiempo
    qs = qs.order_by('fecha_registro').values(
        'id', 'fecha_registro', 'cliente', 'producto', 'codigo_producto',
        'peso_receta', 'peso_real', 'lote', 'turno'
    )

    # Empaquetar para frontend
    registros = []
    for r in qs:
        registros.append({
            'id': r['id'],
            'ts': r['fecha_registro'].isoformat(),
            'cliente': r['cliente'],
            'producto': r['producto'],
            'codigo_producto': r['codigo_producto'],
            'peso_receta': r['peso_receta'],
            'peso_real': r['peso_real'],
            'desviacion': (r['peso_real'] or 0) - (r['peso_receta'] or 0),
            'lote': r['lote'],
            'turno': r['turno'],
        })

    return JsonResponse({'ok': True, 'registros': registros})

