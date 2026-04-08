from datetime import datetime, time

from django.contrib import messages
from django.db import transaction
from django.db.models import Prefetch, Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST

from .forms import HistorialTrazabilidadFilterForm, RegistroTrazabilidadForm
from .models import (
    Cliente,
    Producto,
    ProductoIngrediente,
    Proveedor,
    RegistroTrazabilidad,
    DetalleTrazabilidadIngrediente,
)
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator
import pytz
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font


@require_GET
def obtener_productos_por_cliente(request):
    cliente_id = request.GET.get("cliente_id")
    productos = []

    if cliente_id:
        qs = Producto.objects.filter(cliente_id=cliente_id).order_by("nombre")
        productos = [
            {
                "id": p.id,
                "nombre": p.nombre,
                "codigo": p.codigo,
                "codigo_registro": p.codigo_registro or "",
                "version": p.version or "",
                "fecha_modificacion": p.fecha_modificacion.strftime("%Y-%m-%d") if p.fecha_modificacion else "",
            }
            for p in qs
        ]

    return JsonResponse({"productos": productos})


@require_GET
def obtener_ingredientes_por_producto(request):
    producto_id = request.GET.get("producto_id")
    ingredientes = []

    if producto_id:
        relaciones = (
            ProductoIngrediente.objects
            .filter(producto_id=producto_id)
            .select_related("ingrediente", "proveedor")
            .order_by("orden", "ingrediente__nombre")
        )

        ingredientes = [
            {
                "id": r.ingrediente.id,
                "nombre": r.ingrediente.nombre,
                "proveedor_id": r.proveedor.id if r.proveedor else "",
                "proveedor_nombre": r.proveedor.nombre if r.proveedor else "",
            }
            for r in relaciones
        ]

    return JsonResponse({"ingredientes": ingredientes})


@require_GET
def obtener_proveedores(request):
    proveedores = Proveedor.objects.all().order_by("nombre")
    data = [{"id": p.id, "nombre": p.nombre} for p in proveedores]
    return JsonResponse({"proveedores": data})


@login_required
def registrar_trazabilidad(request):
    form = RegistroTrazabilidadForm()

    if request.method == "POST":
        form = RegistroTrazabilidadForm(request.POST)

        ingredientes_ids = request.POST.getlist("ingrediente_id[]")
        lotes = request.POST.getlist("lote[]")
        fechas_elaboracion = request.POST.getlist("fecha_elaboracion[]")
        fechas_vencimiento = request.POST.getlist("fecha_vencimiento[]")
        proveedores_ids = request.POST.getlist("proveedor_id[]")
        acciones_correctivas = request.POST.getlist("accion_correctiva[]")

        if form.is_valid():
            if not ingredientes_ids:
                messages.error(request, "El producto seleccionado no tiene ingredientes para registrar.")
                return render(
                    request,
                    "trazabilidad_productos/registrar_trazabilidad.html",
                    {
                        "form": form,
                        "clientes": Cliente.objects.all().order_by("nombre"),
                    },
                )

            try:
                with transaction.atomic():
                    registro = form.save(commit=False)
                    producto = registro.producto
                    registro.codigo_producto = producto.codigo
                    registro.save()

                    for i, ingrediente_id in enumerate(ingredientes_ids):
                        lote = lotes[i].strip() if i < len(lotes) and lotes[i] else ""
                        fecha_elab = fechas_elaboracion[i].strip() if i < len(fechas_elaboracion) and fechas_elaboracion[i] else None
                        fecha_venc = fechas_vencimiento[i].strip() if i < len(fechas_vencimiento) and fechas_vencimiento[i] else None
                        proveedor_id = proveedores_ids[i] if i < len(proveedores_ids) else None
                        accion = acciones_correctivas[i].strip() if i < len(acciones_correctivas) and acciones_correctivas[i] else ""

                        if not ingrediente_id:
                            continue

                        if not lote or not proveedor_id:
                            raise ValueError("Todos los ingredientes deben tener lote y proveedor configurado.")
                        
                        if not fecha_elab and not fecha_venc:
                            raise ValueError("Cada ingrediente debe tener al menos fecha de elaboración o fecha de vencimiento.")

                        if fecha_elab and fecha_venc and fecha_venc < fecha_elab:
                            raise ValueError("La fecha de vencimiento no puede ser anterior a la fecha de elaboración.")

                        DetalleTrazabilidadIngrediente.objects.create(
                            registro=registro,
                            ingrediente_id=ingrediente_id,
                            proveedor_id=proveedor_id,
                            lote=lote,
                            fecha_elaboracion=fecha_elab,
                            fecha_vencimiento=fecha_venc,
                            accion_correctiva=accion,
                        )

                messages.success(request, "Registro de trazabilidad guardado correctamente.")
                return redirect("trazabilidad_productos:registrar_trazabilidad")

            except Exception as e:
                messages.error(request, f"Error al guardar el registro: {str(e)}")

    contexto = {
        "form": form,
        "clientes": Cliente.objects.all().order_by("nombre"),
    }
    return render(request, "trazabilidad_productos/registrar_trazabilidad.html", contexto)


@login_required
def historial_trazabilidad(request):
    form = HistorialTrazabilidadFilterForm(request.GET or None)
    registros_qs = (
        RegistroTrazabilidad.objects
        .select_related("cliente", "producto")
        .prefetch_related(
            Prefetch(
                "detalles",
                queryset=DetalleTrazabilidadIngrediente.objects.select_related("ingrediente", "proveedor")
            )
        )
        .all()
        .order_by("-fecha_registro")
    )

    if form.is_valid():
        cliente = form.cleaned_data.get("cliente")
        producto = form.cleaned_data.get("producto")
        desde = form.cleaned_data.get("desde")
        hasta = form.cleaned_data.get("hasta")
        lote_producto = form.cleaned_data.get("lote_producto")
        lote_ingrediente = form.cleaned_data.get("lote_ingrediente")
        estado_verificacion = form.cleaned_data.get("estado_verificacion")

        if cliente:
            registros_qs = registros_qs.filter(cliente=cliente)

        if producto:
            registros_qs = registros_qs.filter(producto=producto)

        if desde:
            registros_qs = registros_qs.filter(fecha_elaboracion_producto__gte=desde)

        if hasta:
            registros_qs = registros_qs.filter(fecha_elaboracion_producto__lte=hasta)

        if lote_producto:
            registros_qs = registros_qs.filter(lote_producto__icontains=lote_producto.strip())

        if lote_ingrediente:
            registros_qs = registros_qs.filter(
                detalles__lote__icontains=lote_ingrediente.strip()
            ).distinct()

        if estado_verificacion == "no_verificados":
            registros_qs = registros_qs.filter(verificado=False)
        elif estado_verificacion == "verificados":
            registros_qs = registros_qs.filter(verificado=True)

    paginator = Paginator(registros_qs, 10)
    page_number = request.GET.get("page")
    registros = paginator.get_page(page_number)

    contexto = {
        "form": form,
        "registros": registros,
    }
    return render(request, "trazabilidad_productos/historial_trazabilidad.html", contexto)

@login_required
def redireccionar_intermedio(request):
    url_index = reverse('intermedio')
    return HttpResponseRedirect(url_index)

@login_required
def redireccionar_intermedio_2(request):
    url_index = reverse('intermedio_2')
    return HttpResponseRedirect(url_index)

@require_POST
@login_required
def verificar_trazabilidad(request, registro_id):
    registro = get_object_or_404(RegistroTrazabilidad, id=registro_id)

    if registro.verificado:
        messages.warning(request, "Este registro ya fue verificado.")
        return redirect("historial_trazabilidad")

    registro.verificado = True
    registro.fecha_verificacion = timezone.now()

    nombre_usuario = ""

    if hasattr(request.user, "nombre") and request.user.nombre:
        nombre_usuario = request.user.nombre
    elif hasattr(request.user, "username") and request.user.username:
        nombre_usuario = request.user.username
    elif hasattr(request.user, "email") and request.user.email:
        nombre_usuario = request.user.email
    else:
        nombre_usuario = str(request.user)

    registro.nombre_verificador = nombre_usuario

    registro.save(update_fields=["verificado", "fecha_verificacion", "nombre_verificador"])

    messages.success(request, "Registro verificado correctamente.")
    return redirect("trazabilidad_productos:historial_trazabilidad")


@login_required
def descargar_historial_trazabilidad_excel(request):
    registros = (
        RegistroTrazabilidad.objects
        .select_related("cliente", "producto")
        .prefetch_related("detalles__ingrediente", "detalles__proveedor")
        .all()
        .order_by("-fecha_registro")
    )

    cliente_id = request.GET.get("cliente")
    producto_id = request.GET.get("producto")
    desde = request.GET.get("desde")
    hasta = request.GET.get("hasta")
    lote_producto = request.GET.get("lote_producto")
    lote_ingrediente = request.GET.get("lote_ingrediente")
    estado_verificacion = request.GET.get("estado_verificacion")

    if cliente_id:
        registros = registros.filter(cliente_id=cliente_id)

    if producto_id:
        registros = registros.filter(producto_id=producto_id)

    if desde:
        try:
            desde_date = datetime.strptime(desde, "%Y-%m-%d").date()
            registros = registros.filter(fecha_elaboracion_producto__gte=desde_date)
        except ValueError:
            pass

    if hasta:
        try:
            hasta_date = datetime.strptime(hasta, "%Y-%m-%d").date()
            registros = registros.filter(fecha_elaboracion_producto__lte=hasta_date)
        except ValueError:
            pass

    if lote_producto:
        registros = registros.filter(lote_producto__icontains=lote_producto.strip())

    if lote_ingrediente:
        registros = registros.filter(detalles__lote__icontains=lote_ingrediente.strip()).distinct()

    if estado_verificacion == "no_verificados":
        registros = registros.filter(verificado=False)
    elif estado_verificacion == "verificados":
        registros = registros.filter(verificado=True)

    if not registros.exists():
        return render(request, "inicio/no_hay_datos.html")

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="historial_trazabilidad.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Trazabilidad"

    encabezados = [
        "Cliente", "Producto", "Código", "Lote producto", "Fecha elab. producto",
        "Turno", "Línea", "Elaborado por", "Fecha registro",
        "Ingrediente", "Proveedor", "Lote ingrediente", "Fecha elaboración",
        "Fecha vencimiento", "Acción correctiva", "Observaciones",
        "Codigo registro", "Version", "Fecha modificacion",
        "Verificado", "Fecha verificacion", "Nombre verificador",
    ]
    ws.append(encabezados)

    for cell in ws[1]:
        cell.font = Font(bold=True)

    tz_santiago = pytz.timezone("America/Santiago")

    def convertir_fecha_hora(fecha):
        if not fecha:
            return ""
        if timezone.is_aware(fecha):
            return fecha.astimezone(tz_santiago).replace(tzinfo=None)
        return fecha

    for registro in registros:
        detalles = registro.detalles.all()

        codigo_registro = getattr(registro.producto, "codigo_registro", "") or ""
        version = getattr(registro.producto, "version", "") or ""
        fecha_modificacion = getattr(registro.producto, "fecha_modificacion", None)

        verificado = "Sí" if registro.verificado else "No"
        fecha_verificacion = convertir_fecha_hora(registro.fecha_verificacion)
        nombre_verificador = registro.nombre_verificador or ""

        if detalles.exists():
            for detalle in detalles:
                ws.append([
                    registro.cliente.nombre if registro.cliente else "",
                    registro.producto.nombre if registro.producto else "",
                    registro.codigo_producto or "",
                    registro.lote_producto or "",
                    registro.fecha_elaboracion_producto,
                    registro.turno or "",
                    registro.linea or "",
                    registro.elaborado_por or "",
                    convertir_fecha_hora(registro.fecha_registro),
                    detalle.ingrediente.nombre if detalle.ingrediente else "",
                    detalle.proveedor.nombre if detalle.proveedor else "",
                    detalle.lote or "",
                    detalle.fecha_elaboracion,
                    detalle.fecha_vencimiento,
                    detalle.accion_correctiva or "",
                    registro.observaciones or "",
                    codigo_registro,
                    version,
                    fecha_modificacion,
                    verificado,
                    fecha_verificacion,
                    nombre_verificador,
                ])
        else:
            ws.append([
                registro.cliente.nombre if registro.cliente else "",
                registro.producto.nombre if registro.producto else "",
                registro.codigo_producto or "",
                registro.lote_producto or "",
                registro.fecha_elaboracion_producto,
                registro.turno or "",
                registro.linea or "",
                registro.elaborado_por or "",
                convertir_fecha_hora(registro.fecha_registro),
                "",
                "",
                "",
                "",
                "",
                "",
                registro.observaciones or "",
                codigo_registro,
                version,
                fecha_modificacion,
                verificado,
                fecha_verificacion,
                nombre_verificador,
            ])

    anchos = {
        "A": 18, "B": 28, "C": 14, "D": 18, "E": 20, "F": 14, "G": 14, "H": 18,
        "I": 22, "J": 24, "K": 18, "L": 18, "M": 20, "N": 20, "O": 28, "P": 30,
        "Q": 18, "R": 12, "S": 20, "T": 12, "U": 22, "V": 22,
    }
    for col, ancho in anchos.items():
        ws.column_dimensions[col].width = ancho

    wb.save(response)
    return response