from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioControlDePesosInsumosKuchen
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@login_required
def control_de_pesos_insumos_kuchen(request):
    return render(request, 'control_de_pesos_insumos_kuchen/r_control_de_pesos_insumos_kuchen.html')

@csrf_exempt
@login_required 
def vista_control_de_pesos_insumos_kuchen(request):
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
            altura = dato.get('altura')
            lote = dato.get('lote')
            turno = dato.get('turno')

            if altura == '':
                altura = None

            datos = DatosFormularioControlDePesosInsumosKuchen(
                nombre_tecnologo=nombre_tecnologo,
                fecha_registro=fecha_registro,
                cliente=cliente,
                codigo_producto=codigo_producto,
                producto=producto,
                peso_receta=peso_receta,
                peso_real=peso_real,
                altura=altura,
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

# --- Renderiza la página de gráficos
@login_required
def graficos_control_pesos_insumos_kuchen(request):
    clientes = (
        DatosFormularioControlDePesosInsumosKuchen.objects
        .values_list("cliente", flat=True).distinct().order_by("cliente")
    )
    turnos = (
        DatosFormularioControlDePesosInsumosKuchen.objects
        .values_list("turno", flat=True).distinct().order_by("turno")
    )
    return render(
        request,
        "control_de_pesos_insumos_kuchen/graficos_control_pesos_insumos_kuchen.html",
        {"clientes": clientes, "turnos": turnos},
    )

# --- Devuelve productos por cliente (para combo dependiente)
@login_required
def api_productos_por_cliente_insumos_kuchen(request):
    cli = request.GET.get("cliente", "").strip()
    if not cli:
        return JsonResponse({"ok": True, "productos": []})
    qs = DatosFormularioControlDePesosInsumosKuchen.objects.filter(cliente=cli)
    productos = (
        qs.values("producto")
          .distinct()
          .order_by("producto")
    )
    # salida: [{"producto": "Kuchen manzana"}, ...]
    return JsonResponse({"ok": True, "productos": list(productos)})

# --- API de datos para graficar
@login_required
def api_graficos_control_pesos_insumos_kuchen(request):
    """
    Filtros (GET):
    - cliente, producto, turno, lote (contiene)
    - desde, hasta (YYYY-MM-DD)
    """
    try:
        qs = DatosFormularioControlDePesosInsumosKuchen.objects.all()

        cliente = request.GET.get("cliente", "").strip()
        producto = request.GET.get("producto", "").strip()
        turno    = request.GET.get("turno", "").strip()
        lote     = request.GET.get("lote", "").strip()
        desde    = request.GET.get("desde", "").strip()
        hasta    = request.GET.get("hasta", "").strip()

        if cliente:
            qs = qs.filter(cliente=cliente)
        if producto:
            qs = qs.filter(producto=producto)
        if turno:
            qs = qs.filter(turno=turno)
        if lote:
            qs = qs.filter(lote__icontains=lote)

        # Fechas (cubre el día completo)
        if desde:
            try:
                d = datetime.strptime(desde, "%Y-%m-%d").date()
                qs = qs.filter(fecha_registro__gte=datetime.combine(d, time.min, tzinfo=timezone.get_current_timezone()))
            except ValueError:
                pass
        if hasta:
            try:
                h = datetime.strptime(hasta, "%Y-%m-%d").date()
                qs = qs.filter(fecha_registro__lte=datetime.combine(h, time.max, tzinfo=timezone.get_current_timezone()))
            except ValueError:
                pass

        qs = qs.order_by("fecha_registro")

        registros = []
        for r in qs:
            try:
                peso_receta = float(r.peso_receta) if r.peso_receta is not None else None
                peso_real   = float(r.peso_real)   if r.peso_real   is not None else None
                desv        = (peso_real - peso_receta) if (peso_real is not None and peso_receta is not None) else None
            except Exception:
                peso_receta = peso_real = desv = None

            registros.append({
                "id": r.id,
                "ts": r.fecha_registro.isoformat(),
                "cliente": r.cliente,
                "producto": r.producto,
                "codigo_producto": r.codigo_producto,
                "peso_receta": peso_receta,
                "peso_real": peso_real,
                "altura": r.altura,
                "desviacion": desv,
                "lote": r.lote,
                "turno": r.turno,
            })

        return JsonResponse({"ok": True, "registros": registros})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)
    
@login_required
def redireccionar_intermedio_4(request):
    url_intermedio = reverse('intermedio_4')
    return HttpResponseRedirect(url_intermedio)
