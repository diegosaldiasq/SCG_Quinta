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

    def _guardar_resumen_en_registro(self, registro):
        resumen = self._calcular_resumen(registro.layout)

        registro.total_capas = resumen["total_capas"]
        registro.peso_objetivo_total_g = resumen["peso_objetivo_total"]
        registro.porcentaje_perdida = resumen["porcentaje_perdida"]
        registro.peso_final_con_perdida_g = resumen["peso_final_con_perdida"]
        registro.save(update_fields=[
            "total_capas",
            "peso_objetivo_total_g",
            "porcentaje_perdida",
            "peso_final_con_perdida_g",
        ])

        return resumen

    def _sincronizar_capas_con_layout(self, registro):
        """
        Elimina las capas actuales del registro y crea las que correspondan
        exactamente al layout actual.
        """
        RegistroCapa.objects.filter(registro=registro).delete()

        nuevas = []
        for capa in registro.layout.capas.all().order_by("orden"):
            nuevas.append(
                RegistroCapa(
                    registro=registro,
                    capa=capa,
                    ingrediente_usado=None,
                    peso_real_g=None,
                    comentario="",
                )
            )

        if nuevas:
            RegistroCapa.objects.bulk_create(nuevas)

    def _calcular_peso_real_desde_formset(self, formset):
        total = Decimal("0.0")

        for form in formset.forms:
            if not hasattr(form, "cleaned_data"):
                continue

            if not form.cleaned_data:
                continue

            if form.cleaned_data.get("DELETE"):
                continue

            peso = form.cleaned_data.get("peso_real_g")
            if peso is not None:
                total += Decimal(str(peso))

        return round(total, 1)

    def _contexto_desde_registro(self, registro, form, formset=None, auto_cargado=False):
        return {
            "form": form,
            "formset": formset,
            "registro_id": registro.id,
            "auto_cargado": auto_cargado,
            "total_capas": registro.total_capas or 0,
            "peso_objetivo_total": registro.peso_objetivo_total_g or 0,
            "porcentaje_perdida": registro.porcentaje_perdida or 0,
            "peso_final_con_perdida": registro.peso_final_con_perdida_g or 0,
            "peso_real_obtenido_actual": registro.peso_real_obtenido_g or 0,
        }

    def get(self, request):
        form = RegistroLayoutForm(
            operador_inicial=self._nombre_operador(request)
        )

        context = {
            "form": form,
            "formset": None,
            "total_capas": 0,
            "peso_objetivo_total": 0,
            "porcentaje_perdida": 0,
            "peso_final_con_perdida": 0,
            "peso_real_obtenido_actual": 0,
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request):
        post_data = request.POST.copy()

        planta = post_data.get("planta")
        cliente = post_data.get("cliente")
        producto_id = post_data.get("producto_manual")

        # Resolver layout automáticamente según selección actual
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

        post_data["operador"] = self._nombre_operador(request)

        form = RegistroLayoutForm(
            post_data,
            operador_inicial=self._nombre_operador(request),
        )

        if not form.is_valid():
            return render(request, self.template_name, {
                "form": form,
                "formset": None,
                "total_capas": 0,
                "peso_objetivo_total": 0,
                "porcentaje_perdida": 0,
                "peso_final_con_perdida": 0,
                "peso_real_obtenido_actual": 0,
            })

        registro_id = post_data.get("registro_id")
        auto_cargar = post_data.get("_auto_cargar_capas") == "1"
        guardar = "_guardar" in request.POST

        layout_cambio = False

        if registro_id:
            registro = get_object_or_404(
                RegistroLayout.objects.select_related("layout", "layout__producto"),
                pk=registro_id
            )

            layout_anterior_id = registro.layout_id
            nuevo_layout = form.cleaned_data["layout"]

            for campo in [
                "planta",
                "layout",
                "fecha",
                "turno",
                "linea",
                "lote",
                "observaciones",
            ]:
                setattr(registro, campo, form.cleaned_data[campo])

            registro.operador = self._nombre_operador(request)

            if layout_anterior_id != nuevo_layout.id:
                layout_cambio = True
                registro.peso_real_obtenido_g = None
                registro.completado = False

            registro.save()
        else:
            registro = form.save(commit=False)
            registro.operador = self._nombre_operador(request)
            registro.verificado = False
            registro.completado = False
            registro.peso_real_obtenido_g = None
            registro.save()
            layout_cambio = True

        # Si cambió el layout, rehacer detalle completo
        if layout_cambio:
            self._sincronizar_capas_con_layout(registro)

        # Asegurar resumen actualizado según layout actual
        self._guardar_resumen_en_registro(registro)

        # Si el usuario apretó Guardar definitivo
        if guardar:
            formset = RegistroCapaFormSet(
                post_data,
                instance=registro,
                prefix="detalles"
            )

            if formset.is_valid():
                formset.save()

                peso_real_total = self._calcular_peso_real_desde_formset(formset)
                registro.peso_real_obtenido_g = peso_real_total
                registro.completado = True
                registro.save(update_fields=["peso_real_obtenido_g", "completado"])

                messages.success(request, "Registro guardado correctamente.")
                return redirect("control_layout_tortas:registro_detalle", pk=registro.id)

            peso_real_total = self._calcular_peso_real_desde_formset(formset)

            form_recargado = RegistroLayoutForm(
                instance=registro,
                operador_inicial=self._nombre_operador(request),
                initial={
                    "cliente": registro.layout.producto.cliente,
                    "producto_manual": registro.layout.producto.id,
                    "codigo_auto": registro.layout.producto.codigo,
                    "operador": self._nombre_operador(request),
                }
            )

            contexto = self._contexto_desde_registro(
                registro=registro,
                form=form_recargado,
                formset=formset,
            )
            contexto["peso_real_obtenido_actual"] = peso_real_total
            return render(request, self.template_name, contexto)

        # Si solo está auto-cargando capas o refrescando cabecera
        formset = RegistroCapaFormSet(instance=registro, prefix="detalles")

        form_recargado = RegistroLayoutForm(
            instance=registro,
            operador_inicial=self._nombre_operador(request),
            initial={
                "cliente": registro.layout.producto.cliente,
                "producto_manual": registro.layout.producto.id,
                "codigo_auto": registro.layout.producto.codigo,
                "operador": self._nombre_operador(request),
            }
        )

        return render(
            request,
            self.template_name,
            self._contexto_desde_registro(
                registro=registro,
                form=form_recargado,
                formset=formset,
                auto_cargado=auto_cargar,
            )
        )


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