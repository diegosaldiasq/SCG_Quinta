from datetime import datetime, time

from django.contrib import messages
from django.db import transaction
from django.db.models import Prefetch, Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET
from django.urls import reverse
from django.http import HttpResponseRedirect

from .forms import HistorialTrazabilidadFilterForm, RegistroTrazabilidadForm
from .models import (
    Cliente,
    Producto,
    ProductoIngrediente,
    Proveedor,
    RegistroTrazabilidad,
    DetalleTrazabilidadIngrediente,
)


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
                "proveedor_id": r.proveedor.id,
                "proveedor_nombre": r.proveedor.nombre,
            }
            for r in relaciones
        ]

    return JsonResponse({"ingredientes": ingredientes})


@require_GET
def obtener_proveedores(request):
    proveedores = Proveedor.objects.all().order_by("nombre")
    data = [{"id": p.id, "nombre": p.nombre} for p in proveedores]
    return JsonResponse({"proveedores": data})


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
                        lote = lotes[i].strip() if i < len(lotes) else ""
                        fecha_elab = fechas_elaboracion[i] if i < len(fechas_elaboracion) else ""
                        fecha_venc = fechas_vencimiento[i] if i < len(fechas_vencimiento) else ""
                        proveedor_id = proveedores_ids[i] if i < len(proveedores_ids) else None
                        accion = acciones_correctivas[i].strip() if i < len(acciones_correctivas) else ""

                        if not ingrediente_id:
                            continue

                        if not lote or not fecha_elab or not fecha_venc or not proveedor_id:
                            raise ValueError("Todos los ingredientes deben tener lote, fechas y proveedor.")

                        if fecha_venc < fecha_elab:
                            raise ValueError("La fecha de vencimiento no puede ser anterior a la fecha de elaboración.")

                        DetalleTrazabilidadIngrediente.objects.create(
                            registro=registro,
                            ingrediente_id=ingrediente_id,
                            lote=lote,
                            fecha_elaboracion=fecha_elab,
                            fecha_vencimiento=fecha_venc,
                            proveedor_id=proveedor_id,
                            accion_correctiva=accion,
                        )

                messages.success(request, "Registro de trazabilidad guardado correctamente.")
                return redirect("registrar_trazabilidad")

            except Exception as e:
                messages.error(request, f"Error al guardar el registro: {str(e)}")

    contexto = {
        "form": form,
        "clientes": Cliente.objects.all().order_by("nombre"),
    }
    return render(request, "trazabilidad_productos/registrar_trazabilidad.html", contexto)


def historial_trazabilidad(request):
    form = HistorialTrazabilidadFilterForm(request.GET or None)

    registros = (
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

        if cliente:
            registros = registros.filter(cliente=cliente)

        if producto:
            registros = registros.filter(producto=producto)

        if desde:
            registros = registros.filter(
                fecha_registro__gte=datetime.combine(desde, time.min)
            )

        if hasta:
            registros = registros.filter(
                fecha_registro__lte=datetime.combine(hasta, time.max)
            )

        if lote_producto:
            registros = registros.filter(lote_producto__icontains=lote_producto.strip())

        if lote_ingrediente:
            registros = registros.filter(detalles__lote__icontains=lote_ingrediente.strip()).distinct()

    contexto = {
        "form": form,
        "registros": registros,
    }
    return render(request, "trazabilidad_productos/historial_trazabilidad.html", contexto)

def redireccionar_intermedio(request):
    url_index = reverse('intermedio')
    return HttpResponseRedirect(url_index)