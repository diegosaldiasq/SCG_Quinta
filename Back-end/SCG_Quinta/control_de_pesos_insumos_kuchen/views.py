from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioControlDePesosInsumosKuchen
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, time
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt
from control_de_pesos.models import ProductoControlPeso

# Create your views here.

@login_required
def control_de_pesos_insumos_kuchen(request):
    return render(request, 'control_de_pesos_insumos_kuchen/r_control_de_pesos_insumos_kuchen.html')

@csrf_exempt
@login_required
def vista_control_de_pesos_insumos_kuchen(request):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'mensaje': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'mensaje': 'JSON inválido'}, status=400)

    dato = data.get('dato', None)

    if not dato:
        return JsonResponse({'ok': False, 'existe': False, 'mensaje': 'No se recibió información'}, status=400)

    nombre_tecnologo = request.user.nombre_completo

    cliente = dato.get('cliente')
    codigo_producto = dato.get('codigo_producto')
    producto = dato.get('producto')
    peso_receta = dato.get('peso_receta')
    lote = dato.get('lote')
    turno = dato.get('turno')
    muestras = dato.get('muestras', [])

    # Compatibilidad con formato antiguo
    if not muestras and dato.get('peso_real') not in [None, ""]:
        muestras = [{
            'peso_real': dato.get('peso_real'),
            'altura': dato.get('altura')
        }]

    if not cliente or not producto or not peso_receta or not lote or not turno:
        return JsonResponse({
            'ok': False,
            'existe': False,
            'mensaje': 'Faltan datos obligatorios'
        }, status=400)

    if not muestras:
        return JsonResponse({
            'ok': False,
            'existe': False,
            'mensaje': 'Debes ingresar al menos una muestra'
        }, status=400)

    guardados = 0

    for muestra in muestras:
        peso_real = muestra.get('peso_real')
        altura = muestra.get('altura')

        if peso_real in [None, ""]:
            continue

        DatosFormularioControlDePesosInsumosKuchen.objects.create(
            nombre_tecnologo=nombre_tecnologo,
            fecha_registro=timezone.now(),
            cliente=cliente,
            codigo_producto=codigo_producto,
            producto=producto,
            peso_receta=int(float(peso_receta)),
            peso_real=int(float(peso_real)),
            altura=int(float(altura)) if altura not in [None, ""] else None,
            lote=lote,
            turno=turno
        )

        guardados += 1

    if guardados == 0:
        return JsonResponse({
            'ok': False,
            'existe': False,
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

    try:

        qs = DatosFormularioControlDePesosInsumosKuchen.objects.all()

        cliente = request.GET.get("cliente", "").strip()
        producto = request.GET.get("producto", "").strip()
        turno = request.GET.get("turno", "").strip()
        lote = request.GET.get("lote", "").strip()
        desde = request.GET.get("desde", "").strip()
        hasta = request.GET.get("hasta", "").strip()

        if cliente:
            qs = qs.filter(cliente=cliente)

        if producto:
            qs = qs.filter(producto=producto)

        if turno:
            qs = qs.filter(turno=turno)

        if lote:
            qs = qs.filter(lote__icontains=lote)

        # =========================
        # FILTRO DESDE
        # =========================
        if desde:
            try:
                d = datetime.strptime(desde, "%Y-%m-%d").date()

                qs = qs.filter(
                    fecha_registro__gte=datetime.combine(
                        d,
                        time.min,
                        tzinfo=timezone.get_current_timezone()
                    )
                )

            except ValueError:
                pass

        # =========================
        # FILTRO HASTA
        # =========================
        if hasta:
            try:
                h = datetime.strptime(hasta, "%Y-%m-%d").date()

                qs = qs.filter(
                    fecha_registro__lte=datetime.combine(
                        h,
                        time.max,
                        tzinfo=timezone.get_current_timezone()
                    )
                )

            except ValueError:
                pass

        qs = qs.order_by("fecha_registro")

        registros = []

        for r in qs:

            producto_base = ProductoControlPeso.objects.filter(
                area="INSUMOS_KUCHEN",
                cliente__iexact=r.cliente,
                codigo=r.codigo_producto,
                producto__iexact=r.producto,
                activo=True
            ).first()

            peso_receta = (
                int(producto_base.peso_receta)
                if producto_base and producto_base.peso_receta is not None
                else (
                    int(r.peso_receta)
                    if r.peso_receta is not None
                    else None
                )
            )

            perdida_operacional = (
                float(producto_base.porcentaje_perdida)
                if producto_base and producto_base.porcentaje_perdida is not None
                else 0
            )

            peso_maximo = None

            if (
                peso_receta is not None and
                perdida_operacional < 100
            ):
                peso_maximo = round(
                    peso_receta / (
                        1 - (perdida_operacional / 100)
                    ),
                    2
                )

            altura_objetivo = (
                int(producto_base.altura)
                if producto_base and producto_base.altura
                else None
            )

            peso_real = (
                int(r.peso_real)
                if r.peso_real is not None
                else None
            )

            altura_real = (
                int(r.altura)
                if r.altura is not None
                else None
            )

            registros.append({
                "id": r.id,

                "ts": r.fecha_registro.isoformat(),

                "cliente": r.cliente,
                "producto": r.producto,
                "codigo_producto": r.codigo_producto,

                "peso_receta": peso_receta,
                "peso_minimo": peso_receta,

                "peso_maximo": peso_maximo,

                "perdida_operacional": perdida_operacional,

                "peso_real": peso_real,

                "altura": altura_real,
                "altura_objetivo": altura_objetivo,

                "desviacion": (
                    (peso_real or 0) -
                    (peso_receta or 0)
                ),

                "lote": r.lote,
                "turno": r.turno,
            })

        return JsonResponse({
            "ok": True,
            "registros": registros
        })

    except Exception as e:

        return JsonResponse({
            "ok": False,
            "error": str(e)
        }, status=500)
    
@login_required
def redireccionar_intermedio_4(request):
    url_intermedio = reverse('intermedio_4')
    return HttpResponseRedirect(url_intermedio)
