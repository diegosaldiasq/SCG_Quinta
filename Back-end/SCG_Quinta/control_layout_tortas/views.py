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
        formset = None
        return render(request, self.template_name, {"form": form, "formset": formset})

    @transaction.atomic
    def post(self, request):
        form = RegistroLayoutForm(request.POST)
        formset = None

        # ✅ Paso intermedio: usuario apretó "Cargar capas" solo para cargar layouts por planta
        if "_cargar_capas" in request.POST:
            planta = request.POST.get("planta")

            # si no hay planta, solo vuelves con el form y un mensaje
            if not planta:
                messages.error(request, "Selecciona una planta.")
                return render(request, self.template_name, {"form": form, "formset": None})

            # aquí el __init__ del form ya habrá filtrado queryset por planta (porque viene en self.data)
            # pero todavía no guardamos nada: solo pedimos que seleccione un layout
            if not request.POST.get("layout"):
                messages.info(request, "Ahora selecciona el layout (torta) y vuelve a presionar 'Cargar capas'.")
                return render(request, self.template_name, {"form": form, "formset": None})

        # ✅ Desde aquí, ya exigimos layout y el resto
        # (puedes volver a dejar layout.required=True si quieres, pero no es obligatorio)
        if form.is_valid() and ("_cargar_capas" in request.POST or "_guardar" in request.POST):
            registro_id = request.POST.get("registro_id")

            if registro_id:
                registro = get_object_or_404(RegistroLayout, pk=registro_id)
            else:
                registro = form.save(commit=False)
                registro.save()

            for capa in registro.layout.capas.all():
                RegistroCapa.objects.get_or_create(registro=registro, capa=capa)

            formset = RegistroCapaFormSet(request.POST, instance=registro)

            if "_cargar_capas" in request.POST:
                messages.info(request, "Capas cargadas. Ingresa los pesos reales y guarda.")
                return render(request, self.template_name, {
                    "form": RegistroLayoutForm(instance=registro),
                    "formset": formset,
                    "registro_id": registro.id
                })

            if formset.is_valid():
                formset.save()
                messages.success(request, "Registro guardado correctamente.")
                return redirect("control_layout_tortas:registro_detalle", pk=registro.id)

            return render(request, self.template_name, {
                "form": RegistroLayoutForm(instance=registro),
                "formset": formset,
                "registro_id": registro.id
            })

        return render(request, self.template_name, {"form": form, "formset": formset})


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
