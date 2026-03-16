from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from .forms import RegistroLayoutForm, RegistroCapaFormSet
from .models import LayoutTorta, RegistroLayout, RegistroCapa


class RegistroCreateView(View):
    template_name = "control_layout_tortas/registro_create.html"

    def get(self, request):
        form = RegistroLayoutForm()
        return render(request, self.template_name, {"form": form, "formset": None})

    @transaction.atomic
    def post(self, request):
        post_data = request.POST.copy()

        planta = post_data.get("planta")
        cliente = post_data.get("cliente")
        producto_id = post_data.get("producto_manual")

        # Si no viene layout, lo resolvemos automáticamente
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

        form = RegistroLayoutForm(post_data)
        formset = None

        if "_cargar_capas" in request.POST:
            if not planta:
                messages.error(request, "Selecciona una planta.")
                return render(request, self.template_name, {"form": form, "formset": None})

            if not cliente:
                messages.error(request, "Selecciona un cliente.")
                return render(request, self.template_name, {"form": form, "formset": None})

            if not producto_id:
                messages.error(request, "Selecciona un producto.")
                return render(request, self.template_name, {"form": form, "formset": None})

        if not form.is_valid():
            return render(request, self.template_name, {"form": form, "formset": None})

        registro_id = post_data.get("registro_id")
        if registro_id:
            registro = get_object_or_404(RegistroLayout, pk=registro_id)
        else:
            registro = form.save(commit=False)
            registro.save()

        for capa in registro.layout.capas.all():
            RegistroCapa.objects.get_or_create(registro=registro, capa=capa)

        if "_cargar_capas" in request.POST:
            formset = RegistroCapaFormSet(instance=registro, prefix="detalles")
            messages.info(request, "Capas cargadas. Ingresa los pesos reales y guarda.")
            return render(request, self.template_name, {
                "form": RegistroLayoutForm(instance=registro),
                "formset": formset,
                "registro_id": registro.id,
            })

        if "_guardar" in request.POST:
            formset = RegistroCapaFormSet(post_data, instance=registro, prefix="detalles")
            if formset.is_valid():
                formset.save()
                messages.success(request, "Registro guardado correctamente.")
                return redirect("control_layout_tortas:registro_detalle", pk=registro.id)

            return render(request, self.template_name, {
                "form": RegistroLayoutForm(instance=registro),
                "formset": formset,
                "registro_id": registro.id,
            })

        return render(request, self.template_name, {"form": form, "formset": None})
    

class RegistroDetalleView(View):
    template_name = "control_layout_tortas/registro_detalle.html"

    def get(self, request, pk):
        registro = get_object_or_404(RegistroLayout, pk=pk)
        detalles = (
            registro.detalles
            .select_related(
                "capa",
                "capa__ingrediente",
                "ingrediente_usado",
            )
            .all()
        )
        return render(request, self.template_name, {"registro": registro, "detalles": detalles})
