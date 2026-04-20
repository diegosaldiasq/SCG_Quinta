from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Prefetch, Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView
from decimal import Decimal, InvalidOperation
from django.db.models import Sum

from .forms import (
    RegistroLayoutForm,
    RegistroCapaFormSet,
    HistorialRegistroFilterForm,
)
from .models import (
    LayoutTorta,
    RegistroLayout,
    RegistroCapa,
    Ingrediente,
)


class RegistroCreateView(LoginRequiredMixin, View):
    template_name = "control_layout_tortas/registro_create.html"

    def _nombre_operador(self, request):
        user = request.user

        nombre_completo = getattr(user, "nombre_completo", "")
        if nombre_completo and str(nombre_completo).strip():
            return str(nombre_completo).strip()

        username = getattr(user, "username", "")
        if username and str(username).strip():
            return str(username).strip()

        email = getattr(user, "email", "")
        if email and str(email).strip():
            return str(email).strip()

        return str(user)

    def _resolver_layout(self, planta, cliente, producto_id):
        if not planta or not cliente or not producto_id:
            return None

        return (
            LayoutTorta.objects
            .filter(
                activo=True,
                planta=planta,
                producto_id=producto_id,
                producto__cliente=cliente,
            )
            .select_related("producto")
            .order_by("-version")
            .first()
        )

    def _calcular_resumen(self, layout):
        if not layout:
            return {
                "total_capas": 0,
                "peso_objetivo_total": Decimal("0.0"),
                "porcentaje_perdida": Decimal("0.0"),
                "peso_final_con_perdida": Decimal("0.0"),
            }

        capas_qs = layout.capas.all()

        total_capas = capas_qs.count()
        peso_objetivo_total = capas_qs.aggregate(
            total=Sum("peso_objetivo_g")
        )["total"] or Decimal("0.0")

        try:
            porcentaje_perdida = layout.producto.porcentaje_perdida or Decimal("0.0")
        except Exception:
            porcentaje_perdida = Decimal("0.0")

        peso_final_con_perdida = peso_objetivo_total * (
            Decimal("1") - (porcentaje_perdida / Decimal("100"))
        )

        return {
            "total_capas": total_capas,
            "peso_objetivo_total": round(peso_objetivo_total, 1),
            "porcentaje_perdida": round(porcentaje_perdida, 2),
            "peso_final_con_perdida": round(peso_final_con_perdida, 1),
        }

    def _to_decimal_or_none(self, value):
        if value in (None, ""):
            return None
        try:
            return Decimal(str(value).replace(",", "."))
        except (InvalidOperation, TypeError, ValueError):
            return None

    def _build_detalle_rows(self, layout, post_data=None):
        if not layout:
            return []

        ingredientes = list(
            Ingrediente.objects.filter(activo=True).order_by("nombre")
        )

        posted_capa_ids = post_data.getlist("capa_id") if post_data else []
        posted_ingredientes = post_data.getlist("ingrediente_usado") if post_data else []
        posted_pesos = post_data.getlist("peso_real_g") if post_data else []
        posted_comentarios = post_data.getlist("comentario") if post_data else []

        capas = list(
            layout.capas.select_related("ingrediente").order_by("orden")
        )

        rows = []
        for idx, capa in enumerate(capas):
            ingrediente_usado_id = ""
            peso_real_g = ""
            comentario = ""

            if idx < len(posted_capa_ids):
                try:
                    if str(posted_capa_ids[idx]) == str(capa.id):
                        ingrediente_usado_id = posted_ingredientes[idx] if idx < len(posted_ingredientes) else ""
                        peso_real_g = posted_pesos[idx] if idx < len(posted_pesos) else ""
                        comentario = posted_comentarios[idx] if idx < len(posted_comentarios) else ""
                except Exception:
                    pass

            rows.append({
                "idx": idx,
                "capa": capa,
                "ingredientes": ingredientes,
                "ingrediente_usado_id": str(ingrediente_usado_id or ""),
                "peso_real_g": peso_real_g,
                "comentario": comentario,
            })

        return rows

    def _calcular_peso_real_desde_rows(self, rows):
        total = Decimal("0.0")
        for row in rows:
            peso = self._to_decimal_or_none(row.get("peso_real_g"))
            if peso is not None:
                total += peso
        return round(total, 1)

    def _set_campos_visualizacion_form(self, form, layout):
        if not layout:
            return

        producto = layout.producto
        codigo = producto.codigo or ""

        if "cliente" in form.fields:
            form.fields["cliente"].initial = producto.cliente

        if "producto_manual" in form.fields:
            form.fields["producto_manual"].initial = producto.id

        if "codigo_auto" in form.fields:
            form.fields["codigo_auto"].initial = codigo
            form.initial["codigo_auto"] = codigo
            form.fields["codigo_auto"].widget.attrs["value"] = codigo

        if "layout" in form.fields:
            form.fields["layout"].initial = layout.id
            form.initial["layout"] = layout.id

    def _contexto_base(self, form, layout=None, detalle_rows=None, peso_real_obtenido_actual=0):
        resumen = self._calcular_resumen(layout)

        codigo_producto = ""
        if layout and layout.producto:
            codigo_producto = layout.producto.codigo or ""

        return {
            "form": form,
            "layout_actual": layout,
            "detalle_rows": detalle_rows or [],
            "total_capas": resumen["total_capas"],
            "peso_objetivo_total": resumen["peso_objetivo_total"],
            "porcentaje_perdida": resumen["porcentaje_perdida"],
            "peso_final_con_perdida": resumen["peso_final_con_perdida"],
            "peso_real_obtenido_actual": peso_real_obtenido_actual,
            "codigo_producto_actual": codigo_producto,
        }

    def get(self, request):
        form = RegistroLayoutForm(
            operador_inicial=self._nombre_operador(request)
        )

        return render(
            request,
            self.template_name,
            self._contexto_base(form=form),
        )

    @transaction.atomic
    def post(self, request):
        post_data = request.POST.copy()

        planta = post_data.get("planta")
        cliente = post_data.get("cliente")
        producto_id = post_data.get("producto_manual")

        layout_obj = self._resolver_layout(planta, cliente, producto_id)
        if layout_obj:
            post_data["layout"] = str(layout_obj.id)

        post_data["operador"] = self._nombre_operador(request)

        form = RegistroLayoutForm(
            post_data,
            operador_inicial=self._nombre_operador(request),
        )

        if not form.is_valid():
            return render(
                request,
                self.template_name,
                self._contexto_base(form=form),
            )

        layout = form.cleaned_data.get("layout")
        self._set_campos_visualizacion_form(form, layout)

        detalle_rows = self._build_detalle_rows(layout, request.POST)
        peso_real_preview = self._calcular_peso_real_desde_rows(detalle_rows)

        guardar = "_guardar" in request.POST

        # Solo preview, sin guardar en BD
        if not guardar:
            return render(
                request,
                self.template_name,
                self._contexto_base(
                    form=form,
                    layout=layout,
                    detalle_rows=detalle_rows,
                    peso_real_obtenido_actual=peso_real_preview,
                ),
            )

        # Guardado definitivo
        registro = form.save(commit=False)
        registro.operador = self._nombre_operador(request)
        registro.verificado = False
        registro.completado = False

        resumen = self._calcular_resumen(layout)
        registro.total_capas = resumen["total_capas"]
        registro.peso_objetivo_total_g = resumen["peso_objetivo_total"]
        registro.porcentaje_perdida = resumen["porcentaje_perdida"]
        registro.peso_final_con_perdida_g = resumen["peso_final_con_perdida"]
        registro.peso_real_obtenido_g = peso_real_preview

        registro.save()

        detalles_creados = []
        for row in detalle_rows:
            ingrediente_usado_id = row.get("ingrediente_usado_id") or None
            peso_real_g = self._to_decimal_or_none(row.get("peso_real_g"))
            comentario = row.get("comentario") or ""

            detalles_creados.append(
                RegistroCapa(
                    registro=registro,
                    capa=row["capa"],
                    ingrediente_usado_id=int(ingrediente_usado_id) if ingrediente_usado_id else None,
                    peso_real_g=peso_real_g,
                    comentario=comentario,
                )
            )

        if detalles_creados:
            RegistroCapa.objects.bulk_create(detalles_creados)

        registro.completado = True
        registro.save(update_fields=["completado"])

        messages.success(request, "Registro guardado correctamente.")
        return redirect("control_layout_tortas:registro_detalle", pk=registro.id)


class RegistroDetalleView(LoginRequiredMixin, View):
    template_name = "control_layout_tortas/registro_detalle.html"

    def get(self, request, pk):
        registro = get_object_or_404(
            RegistroLayout.objects.select_related(
                "layout",
                "layout__producto",
                "verificado_por",
            ),
            pk=pk
        )

        detalles = (
            RegistroCapa.objects
            .filter(registro=registro)
            .select_related(
                "capa",
                "capa__ingrediente",
                "ingrediente_usado",
            )
            .order_by("capa__orden")
        )

        return render(request, self.template_name, {
            "registro": registro,
            "detalles": detalles,
        })


class HistorialRegistroListView(ListView):
    model = RegistroLayout
    template_name = "control_layout_tortas/historial_registros.html"
    context_object_name = "registros"
    paginate_by = 10

    def get_queryset(self):
        qs = (
            RegistroLayout.objects
            .select_related("layout", "layout__producto")
            .prefetch_related(
                Prefetch(
                    "detalles",
                    queryset=RegistroCapa.objects.select_related("capa", "ingrediente_usado")
                )
            )
            .filter(completado=True)
            .annotate(
                capas_con_peso=Count(
                    "detalles",
                    filter=Q(detalles__peso_real_g__isnull=False)
                ),
            )
            .order_by("-fecha", "-creado_en")
        )

        self.filter_form = HistorialRegistroFilterForm(self.request.GET or None)

        if self.filter_form.is_valid():
            planta = self.filter_form.cleaned_data.get("planta")
            turno = self.filter_form.cleaned_data.get("turno")
            linea = self.filter_form.cleaned_data.get("linea")
            layout = self.filter_form.cleaned_data.get("layout")
            desde = self.filter_form.cleaned_data.get("desde")
            hasta = self.filter_form.cleaned_data.get("hasta")
            lote = self.filter_form.cleaned_data.get("lote")
            operador = self.filter_form.cleaned_data.get("operador")
            verificado = self.filter_form.cleaned_data.get("verificado")

            if planta:
                qs = qs.filter(planta=planta)

            if turno:
                qs = qs.filter(turno=turno)

            if linea:
                qs = qs.filter(linea=linea)

            if layout:
                qs = qs.filter(layout=layout)

            if desde:
                qs = qs.filter(fecha__gte=desde)

            if hasta:
                qs = qs.filter(fecha__lte=hasta)

            if lote:
                qs = qs.filter(lote__icontains=lote)

            if operador:
                qs = qs.filter(operador__icontains=operador)

            if verificado == "si":
                qs = qs.filter(verificado=True)
            elif verificado == "no":
                qs = qs.filter(verificado=False)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = getattr(self, "filter_form", HistorialRegistroFilterForm())

        for registro in context["registros"]:
            detalles = list(registro.detalles.all())

            registro.ok_count = sum(1 for d in detalles if d.cumple is True)
            registro.no_count = sum(1 for d in detalles if d.cumple is False)

        return context


@login_required
@transaction.atomic
def verificar_registro(request, pk):
    if request.method != "POST":
        return redirect("control_layout_tortas:historial_registros")

    registro = get_object_or_404(RegistroLayout, pk=pk)
    registro.verificado = True
    registro.verificado_por = request.user
    registro.fecha_verificacion = timezone.now()
    registro.save(update_fields=["verificado", "verificado_por", "fecha_verificacion"])

    messages.success(request, "Registro verificado correctamente.")
    return redirect(request.POST.get("next") or reverse("control_layout_tortas:historial_registros"))


@login_required
@transaction.atomic
def desverificar_registro(request, pk):
    if request.method != "POST":
        return redirect("control_layout_tortas:historial_registros")

    registro = get_object_or_404(RegistroLayout, pk=pk)
    registro.verificado = False
    registro.verificado_por = None
    registro.fecha_verificacion = None
    registro.save(update_fields=["verificado", "verificado_por", "fecha_verificacion"])

    messages.warning(request, "Registro marcado como pendiente nuevamente.")
    return redirect(request.POST.get("next") or reverse("control_layout_tortas:historial_registros"))


@login_required
def redireccionar_intermedio(request):
    url_index = reverse("intermedio")
    return HttpResponseRedirect(url_index)