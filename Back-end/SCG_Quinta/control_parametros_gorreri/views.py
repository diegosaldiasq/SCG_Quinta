from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioControlParametrosGorreri
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils.dateparse import parse_date

# Create your views here.

@login_required
def control_parametros_gorreri(request):
    return render(request, 'control_parametros_gorreri/r_control_parametros_gorreri.html')

@csrf_exempt
@login_required 
def vista_control_parametros_gorreri(request):
     if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        dato = data.get('dato', None)
        if dato:
            try:
                nombre_tecnologo = request.user.nombre_completo
                fecha_registro = timezone.now()
                cliente = dato.get('cliente')
                codigo_producto = dato.get('codigo_producto')
                producto = dato.get('producto')
                numero_tm = int(dato.get('numero_tm'))
                velocidad_bomba = int(dato.get('velocidad_bomba'))
                velocidad_turbo = int(dato.get('velocidad_turbo'))
                contrapresion = float(dato.get('contrapresion'))
                inyeccion_de_aire = int(dato.get('inyeccion_de_aire'))
                densidad = float(dato.get('densidad'))
                t_final = float(dato.get('t_final'))
                lote = dato.get('lote')
                turno = dato.get('turno')

                datos = DatosFormularioControlParametrosGorreri(
                    nombre_tecnologo=nombre_tecnologo,
                    fecha_registro=fecha_registro,
                    cliente=cliente,
                    codigo_producto=codigo_producto,
                    producto=producto,
                    numero_tm=numero_tm,
                    velocidad_bomba=velocidad_bomba,
                    velocidad_turbo=velocidad_turbo,
                    contrapresion=contrapresion,
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
            return JsonResponse({'existe': False, 'error': 'No se recibió ningún dato válido.'})

@login_required
def redireccionar_selecciones_2(request):
    url_selecciones = reverse('vista_selecciones_2')
    return HttpResponseRedirect(url_selecciones)

@login_required
def graficos_parametros_gorreri(request):
    """
    Renderiza el template con los gráficos.
    Aquí solo mandamos las listas de clientes, productos y turnos distintos
    para poblar los <select>.
    """
    # sacamos valores distintos de la tabla
    clientes = DatosFormularioControlParametrosGorreri.objects.values_list('cliente', flat=True).distinct().order_by('cliente')
    productos = DatosFormularioControlParametrosGorreri.objects.values_list('producto', flat=True).distinct().order_by('producto')
    turnos = DatosFormularioControlParametrosGorreri.objects.values_list('turno', flat=True).distinct().order_by('turno')
    tms = DatosFormularioControlParametrosGorreri.objects.values_list('numero_tm', flat=True).distinct().order_by('numero_tm')

    ctx = {
        'clientes': clientes,
        'productos': productos,
        'turnos': turnos,
        'tms': tms,
    }
    return render(request, 'control_parametros_gorreri/graficos_parametros_gorreri.html', ctx)


@login_required
def api_graficos_parametros_gorreri(request):
    """
    Devuelve los registros filtrados en JSON para que el front dibuje los gráficos.
    """
    qs = DatosFormularioControlParametrosGorreri.objects.all().order_by('fecha_registro')

    cliente = request.GET.get('cliente') or ''
    producto = request.GET.get('producto') or ''
    turno = request.GET.get('turno') or ''
    lote = request.GET.get('lote') or ''
    tm = request.GET.get('tm') or ''
    desde = request.GET.get('desde') or ''
    hasta = request.GET.get('hasta') or ''

    if cliente:
        qs = qs.filter(cliente=cliente)
    if producto:
        qs = qs.filter(producto=producto)
    if turno:
        qs = qs.filter(turno=turno)
    if lote:
        qs = qs.filter(lote__icontains=lote)
    if tm:
        qs = qs.filter(numero_tm=tm)

    # fechas
    if desde:
        d = parse_date(desde)
        if d:
            qs = qs.filter(fecha_registro__date__gte=d)
    if hasta:
        h = parse_date(hasta)
        if h:
            qs = qs.filter(fecha_registro__date__lte=h)

    registros = []
    for r in qs:
        registros.append({
            'id': r.id,
            'ts': r.fecha_registro.isoformat(),
            'cliente': r.cliente,
            'producto': r.producto,
            'codigo_producto': r.codigo_producto,
            'numero_tm': r.numero_tm,
            'velocidad_bomba': r.velocidad_bomba,
            'velocidad_turbo': r.velocidad_turbo,
            'contrapresion': r.contrapresion,
            'inyeccion_de_aire': r.inyeccion_de_aire,
            'densidad': r.densidad,
            't_final': r.t_final,
            'lote': r.lote,
            'turno': r.turno,
        })

    return JsonResponse({'ok': True, 'registros': registros})

@login_required
def api_productos_por_cliente_parametros_gorreri(request):
    cliente = request.GET.get('cliente', '')
    qs = DatosFormularioControlParametrosGorreri.objects.all()
    if cliente:
        qs = qs.filter(cliente=cliente)
    productos = qs.values_list('producto', flat=True).distinct().order_by('producto')
    return JsonResponse({
        'ok': True,
        'productos': [{'producto': p} for p in productos]
    })