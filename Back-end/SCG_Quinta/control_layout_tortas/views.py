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

from .forms import (
    RegistroLayoutForm,
    RegistroCapaFormSet,
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

    def get(self, request):
        form = RegistroLayoutForm(operador_inicial=self._nombre_operador(request))
        return render(request, self.template_name, {"form": form, "formset": None})

    @transaction.atomic
    def post(self, request):
        post_data = request.POST.copy()

        planta = post_data.get("planta")
        cliente = post_data.get("cliente")
        producto_id = post_data.get("producto_manual")

        if not post_data.get("layout") and planta and cliente and producto_id:
            layout_obj = (
                LayoutTorta.objects
                .filter(
                    activo=True,
                    planta=planta,
                    producto_id=producto_id,
                    producto__cliente=cliente,
                )
                .order_by("-version")
                .first()
            )
            if layout_obj:
                post_data["layout"] = str(layout_obj.id)

        post_data["operador"] = self._nombre_operador(request)

        form = RegistroLayoutForm(post_data, operador_inicial=self._nombre_operador(request))
        formset = None

        if not form.is_valid():
            return render(request, self.template_name, {"form": form, "formset": None})

        registro_id = post_data.get("registro_id")
        if registro_id:
            registro = get_object_or_404(RegistroLayout, pk=registro_id)
            for campo in ["planta", "layout", "fecha", "turno", "linea", "lote", "observaciones"]:
                setattr(registro, campo, form.cleaned_data[campo])
            registro.operador = self._nombre_operador(request)
            registro.save()
        else:
            registro = form.save(commit=False)
            registro.operador = self._nombre_operador(request)
            registro.save()

        for capa in registro.layout.capas.all():
            RegistroCapa.objects.get_or_create(registro=registro, capa=capa)

        if "_guardar" in request.POST:
            formset = RegistroCapaFormSet(post_data, instance=registro, prefix="detalles")
            if formset.is_valid():
                formset.save()
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
                }
            )

            return render(request, self.template_name, {
                "form": form_recargado,
                "formset": formset,
                "registro_id": registro.id,
            })

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

        return render(request, self.template_name, {
            "form": form_recargado,
            "formset": formset,
            "registro_id": registro.id,
            "auto_cargado": True,
        })


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


class HistorialRegistroListView(LoginRequiredMixin, ListView):
    model = RegistroLayout
    template_name = "control_layout_tortas/historial_registros.html"
    context_object_name = "registros"
    paginate_by = 10

    def get_queryset(self):
        qs = (
            RegistroLayout.objects
            .select_related(
                "layout",
                "layout__producto",
                "verificado_por",
            )
            .prefetch_related(
                Prefetch(
                    "detalles",
                    queryset=RegistroCapa.objects.select_related("capa", "ingrediente_usado")
                )
            )
            .order_by("-fecha", "-creado_en")
        )

        planta = self.request.GET.get("planta")
        cliente = self.request.GET.get("cliente")
        producto = self.request.GET.get("producto")
        lote = self.request.GET.get("lote")
        fecha_desde = self.request.GET.get("fecha_desde")
        fecha_hasta = self.request.GET.get("fecha_hasta")
        estado = self.request.GET.get("estado_verificacion")

        if planta:
            qs = qs.filter(planta=planta)

        if cliente:
            qs = qs.filter(layout__producto__cliente__icontains=cliente)

        if producto:
            qs = qs.filter(layout__producto__nombre__icontains=producto)

        if lote:
            qs = qs.filter(lote__icontains=lote)

        if fecha_desde:
            qs = qs.filter(fecha__gte=fecha_desde)

        if fecha_hasta:
            qs = qs.filter(fecha__lte=fecha_hasta)

        if estado == "verificados":
            qs = qs.filter(verificado=True)
        elif estado == "pendientes":
            qs = qs.filter(verificado=False)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = HistorialRegistroFilterForm(self.request.GET or None)
        querydict = self.request.GET.copy()
        if "page" in querydict:
            querydict.pop("page")
        context["querystring"] = querydict.urlencode()
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