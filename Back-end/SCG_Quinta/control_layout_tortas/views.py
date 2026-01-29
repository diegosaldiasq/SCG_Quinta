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

        # Paso 1: si aún no existe cabecera guardada, la creamos y armamos detalles
        if form.is_valid() and ("_cargar_capas" in request.POST or "_guardar" in request.POST):
            registro = form.save(commit=False)
            registro.save()

            # Crear detalle por cada capa objetivo (si no existe)
            capas = registro.layout.capas.all()
            for capa in capas:
                RegistroCapa.objects.get_or_create(registro=registro, capa=capa)

            formset = RegistroCapaFormSet(request.POST, instance=registro)

            # Si el usuario solo apretó "Cargar capas", volvemos con formset listo
            if "_cargar_capas" in request.POST:
                messages.info(request, "Capas cargadas. Ingresa los pesos reales y guarda.")
                return render(request, self.template_name, {"form": RegistroLayoutForm(instance=registro), "formset": formset, "registro_id": registro.id})

            # Paso 2: guardar todo
            if formset.is_valid():
                formset.save()
                messages.success(request, "Registro guardado correctamente.")
                return redirect("control_layout_tortas:registro_detalle", pk=registro.id)

            # Si formset inválido, mostramos errores
            return render(request, self.template_name, {"form": RegistroLayoutForm(instance=registro), "formset": formset, "registro_id": registro.id})

        # Si cabecera inválida
        return render(request, self.template_name, {"form": form, "formset": formset})


class RegistroDetalleView(View):
    template_name = "control_layout_tortas/registro_detalle.html"

    def get(self, request, pk):
        registro = get_object_or_404(RegistroLayout, pk=pk)
        detalles = registro.detalles.select_related("capa").all()
        return render(request, self.template_name, {"registro": registro, "detalles": detalles})
