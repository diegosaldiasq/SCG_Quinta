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
        form = RegistroLayoutForm(request.POST)
        formset = None

        # Paso intermedio: cargar layouts por planta si layout no viene
        if "_cargar_capas" in request.POST:
            planta = request.POST.get("planta")
            if not planta:
                messages.error(request, "Selecciona una planta.")
                return render(request, self.template_name, {"form": form, "formset": None})

            if not request.POST.get("layout"):
                messages.info(request, "Ahora selecciona el layout (torta) y vuelve a presionar 'Cargar capas'.")
                return render(request, self.template_name, {"form": form, "formset": None})

        # Desde aquí necesitamos cabecera válida (layout incluido)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form, "formset": None})

        # Recuperar o crear registro cabecera
        registro_id = request.POST.get("registro_id")
        if registro_id:
            registro = get_object_or_404(RegistroLayout, pk=registro_id)
            # opcional: actualizar cabecera si cambió algo
            # (si quieres forzar actualización, lo hacemos después)
        else:
            registro = form.save(commit=False)
            registro.save()

        # Asegurar detalle por capa objetivo
        for capa in registro.layout.capas.all():
            RegistroCapa.objects.get_or_create(registro=registro, capa=capa)

        # ✅ Si el usuario presionó "Cargar capas": formset NO bound (genera management form)
        if "_cargar_capas" in request.POST:
            formset = RegistroCapaFormSet(instance=registro, prefix="detalles")
            messages.info(request, "Capas cargadas. Ingresa los pesos reales y guarda.")
            return render(request, self.template_name, {
                "form": RegistroLayoutForm(instance=registro),
                "formset": formset,
                "registro_id": registro.id,
            })

        # ✅ Si presionó "Guardar": formset bound a POST (aquí sí vienen los hidden)
        if "_guardar" in request.POST:
            formset = RegistroCapaFormSet(request.POST, instance=registro, prefix="detalles")
            if formset.is_valid():
                formset.save()
                messages.success(request, "Registro guardado correctamente.")
                return redirect("control_layout_tortas:registro_detalle", pk=registro.id)

            return render(request, self.template_name, {
                "form": RegistroLayoutForm(instance=registro),
                "formset": formset,
                "registro_id": registro.id,
            })

        # fallback
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
