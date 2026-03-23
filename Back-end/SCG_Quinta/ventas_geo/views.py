from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CargaVentasForm
from .models import CargaVentas, Venta, Producto
from .services import procesar_carga_ventas


def cargar_ventas(request):
    if request.method == 'POST':
        form = CargaVentasForm(request.POST, request.FILES)
        if form.is_valid():
            carga = form.save()

            try:
                procesar_carga_ventas(carga)
                messages.success(request, 'Archivo procesado correctamente.')
                return redirect('ventas_geo:resultado_carga', carga_id=carga.id)
            except Exception as e:
                messages.error(request, f'Error al procesar el archivo: {e}')
                return redirect('ventas_geo:cargar_ventas')
    else:
        form = CargaVentasForm()

    return render(request, 'ventas_geo/cargar_ventas.html', {
        'form': form
    })


def resultado_carga(request, carga_id):
    carga = get_object_or_404(CargaVentas, id=carga_id)
    errores = carga.errores.all()

    return render(request, 'ventas_geo/resultado_carga.html', {
        'carga': carga,
        'errores': errores,
    })


def dashboard_ventas_geo(request):
    producto_id = request.GET.get('producto')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')

    ventas = Venta.objects.select_related('producto', 'local')

    if producto_id:
        ventas = ventas.filter(producto_id=producto_id)

    if fecha_desde:
        ventas = ventas.filter(fecha__gte=fecha_desde)

    if fecha_hasta:
        ventas = ventas.filter(fecha__lte=fecha_hasta)

    puntos = (
        ventas.values(
            'local__nombre',
            'local__direccion',
            'local__comuna',
            'local__ciudad',
            'local__latitud',
            'local__longitud',
        )
        .annotate(total_vendido=Sum('cantidad'))
        .order_by('-total_vendido')
    )

    puntos_list = list(puntos)
    max_total = max((p['total_vendido'] or 0 for p in puntos_list), default=1)

    heat_data = []
    marcadores = []

    for p in puntos_list:
        lat = p['local__latitud']
        lon = p['local__longitud']
        total = p['total_vendido'] or 0

        if lat is not None and lon is not None:
            intensidad = total / max_total if max_total > 0 else 0

            # para que los puntos bajos no desaparezcan completamente
            intensidad = max(0.2, intensidad)

            heat_data.append([float(lat), float(lon), float(intensidad)])

            marcadores.append({
                'local': p['local__nombre'],
                'direccion': p['local__direccion'],
                'comuna': p['local__comuna'],
                'ciudad': p['local__ciudad'],
                'latitud': float(lat),
                'longitud': float(lon),
                'total_vendido': float(total),
            })

    productos = Producto.objects.all()
    total_general = ventas.aggregate(total=Sum('cantidad'))['total'] or 0

    return render(request, 'ventas_geo/dashboard.html', {
        'productos': productos,
        'producto_id': producto_id,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'heat_data': heat_data,
        'marcadores': marcadores,
        'total_general': total_general,
        'cantidad_puntos': len(marcadores),
        'max_total': max_total,
    })