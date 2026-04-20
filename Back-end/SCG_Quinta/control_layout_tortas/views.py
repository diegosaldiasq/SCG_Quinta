from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView
from decimal import Decimal
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

    def _resumen_layout(self, layout, registro=None):
        """
        Calcula el resumen que se mostrará debajo de Turno / Línea / Operador:
        - total_capas
        - peso_objetivo_total
        - porcentaje_perdida
        - peso_final_con_perdida
        - peso_real_obtenido_g
        """

        if not layout:
            return {
                "total_capas": 0,
                "peso_objetivo_total": Decimal("0.0"),
                "porcentaje_perdida": Decimal("0.0"),
                "peso_final_con_perdida": Decimal("0.0"),
                "peso_real_obtenido_g": "",
            }

        total_capas = layout.capas.count()

        peso_objetivo_total = (
            layout.capas.aggregate(total=Sum("peso_objetivo_g")).get("total")
            or Decimal("0.0")
        )

        porcentaje_perdida = getattr(layout.producto, "porcentaje_perdida", Decimal("0.0")) or Decimal("0.0")

        peso_final_con_perdida = peso_objetivo_total * (
            Decimal("1") - (porcentaje_perdida / Decimal("100"))
        )

        peso_real_obtenido_g = ""
        if registro and getattr(registro, "peso_real_obtenido_g", None) is not None:
            peso_real_obtenido_g = registro.peso_real_obtenido_g

        return {
            "total_capas": total_capas,
            "peso_objetivo_total": round(peso_objetivo_total, 1),
            "porcentaje_perdida": round(porcentaje_perdida, 2),
            "peso_final_con_perdida": round(peso_final_con_perdida, 1),
            "peso_real_obtenido_g": peso_real_obtenido_g,
        }

    def _contexto_base(self, form, formset=None, registro=None, auto_cargado=False):
        layout = None
        if registro and registro.layout_id:
            layout = registro.layout
        elif form.is_bound:
            layout_id = form.data.get("layout")
            if layout_id:
                layout = LayoutTorta.objects.filter(pk=layout_id).select_related("producto").first()
        elif getattr(form.instance, "pk", None) and getattr(form.instance, "layout_id", None):
            layout = form.instance.layout

        resumen = self._resumen_layout(layout, registro=registro)

        context = {
            "form": form,
            "formset": formset,
            "total_capas": resumen["total_capas"],
            "peso_objetivo_total": resumen["peso_objetivo_total"],
            "porcentaje_perdida": resumen["porcentaje_perdida"],
            "peso_final_con_perdida": resumen["peso_final_con_perdida"],
            "peso_real_obtenido_g": resumen["peso_real_obtenido_g"],
        }

        if registro:
            context["registro_id"] = registro.id

        if auto_cargado:
            context["auto_cargado"] = True

        return context

    def get(self, request):
        form = RegistroLayoutForm(
            operador_inicial=self._nombre_operador(request)
        )

        return render(
            request,
            self.template_name,
            self._contexto_base(form=form, formset=None, registro=None),
        )

    @transaction.atomic
    def post(self, request):
        post_data = request.POST.copy()

        planta = post_data.get("planta")
        cliente = post_data.get("cliente")
        producto_id = post_data.get("producto_manual")

        # Resolver layout automáticamente si no viene informado
        if not post_data.get("layout") and planta and cliente and producto_id:
            layout_obj = (
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
            if layout_obj:
                post_data["layout"] = str(layout_obj.id)

        # Operador siempre desde el usuario logueado
        post_data["operador"] = self._nombre_operador(request)

        form = RegistroLayoutForm(
            post_data,
            operador_inicial=self._nombre_operador(request),
        )

        if not form.is_valid():
            return render(
                request,
                self.template_name,
                self._contexto_base(form=form, formset=None, registro=None),
            )

        registro_id = post_data.get("registro_id")
        auto_cargar = post_data.get("_auto_cargar_capas") == "1"
        guardar = "_guardar" in request.POST

        if registro_id:
            registro = get_object_or_404(
                RegistroLayout.objects.select_related("layout", "layout__producto"),
                pk=registro_id
            )

            for campo in [
                "planta",
                "layout",
                "fecha",
                "turno",
                "linea",
                "lote",
                "observaciones",
                "peso_real_obtenido_g",
            ]:
                setattr(registro, campo, form.cleaned_data[campo])

            registro.operador = self._nombre_operador(request)
            registro.save()
        else:
            registro = form.save(commit=False)
            registro.operador = self._nombre_operador(request)
            registro.verificado = False
            registro.completado = False
            registro.save()

            for capa in registro.layout.capas.all():
                RegistroCapa.objects.get_or_create(
                    registro=registro,
                    capa=capa
                )

            # refrescar con relaciones para el resumen
            registro = (
                RegistroLayout.objects
                .select_related("layout", "layout__producto")
                .get(pk=registro.pk)
            )

        if guardar:
            formset = RegistroCapaFormSet(
                post_data,
                instance=registro,
                prefix="detalles"
            )

            if formset.is_valid():
                formset.save()
                registro.completado = True
                registro.save(update_fields=["completado"])
                messages.success(request, "Registro guardado correctamente.")
                return redirect("control_layout_tortas:registro_detalle", pk=registro.id)

            form_recargado = RegistroLayoutForm(
                instance=registro,
                operador_inicial=self._nombre_operador(request),
                initial={
                    "cliente": registro.layout.producto.cliente,
                    "producto_manual": registro.layout.producto.id,
                    "codigo_auto": registro.layout.producto.codigo,
                    "operador": self._nombre_operador(request),
                    "peso_real_obtenido_g": registro.peso_real_obtenido_g,
                }
            )

            return render(
                request,
                self.template_name,
                self._contexto_base(
                    form=form_recargado,
                    formset=formset,
                    registro=registro,
                ),
            )

        # Auto-carga o vista intermedia
        formset = RegistroCapaFormSet(instance=registro, prefix="detalles")

        form_recargado = RegistroLayoutForm(
            instance=registro,
            operador_inicial=self._nombre_operador(request),
            initial={
                "cliente": registro.layout.producto.cliente,
                "producto_manual": registro.layout.producto.id,
                "codigo_auto": registro.layout.producto.codigo,
                "operador": self._nombre_operador(request),
                "peso_real_obtenido_g": registro.peso_real_obtenido_g,
            }
        )

        return render(
            request,
            self.template_name,
            self._contexto_base(
                form=form_recargado,
                formset=formset,
                registro=registro,
                auto_cargado=auto_cargar,
            ),
        )


class RegistroDetalleView(LoginRequiredMixin, View):
    template_name = "control_layout_tortas/registro_detalle.html"

    def get(self, request, pk):
        registro = get_object_or_404(RegistroLayout, pk=pk)
        detalles = (
            registro.detalles
            .select_related("capa", "capa__ingrediente", "ingrediente_usado")
            .all()
        )
        return render(request, self.template_name, {"registro": registro, "detalles": detalles})


class HistorialRegistroListView(ListView):
    model = RegistroLayout
    template_name = "control_layout_tortas/historial_registros.html"
    context_object_name = "registros"
    paginate_by = 10

    def get_queryset(self):
        qs = (
            RegistroLayout.objects
            .select_related("layout", "layout__producto")
            .filter(completado=True)
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