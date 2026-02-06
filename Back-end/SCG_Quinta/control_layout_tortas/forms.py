from django import forms
from django.forms import modelform_factory
from django.forms.models import inlineformset_factory
from .models import RegistroLayout, RegistroCapa, LayoutTorta, Ingrediente


class RegistroLayoutForm(forms.ModelForm):
    class Meta:
        model = RegistroLayout
        fields = [
            "planta",
            "layout",
            "fecha",
            "turno",
            "linea",
            "lote",
            "operador",
            "observaciones",
        ]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "observaciones": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["layout"].required = False

        # ✅ por defecto: mostrar todos los activos
        self.fields["layout"].queryset = (
            LayoutTorta.objects
            .filter(activo=True)
            .select_related("producto")
        )

        planta = None
        if self.data.get("planta"):
            planta = self.data.get("planta")
        elif self.instance and self.instance.planta:
            planta = self.instance.planta

        if planta:
            self.fields["layout"].queryset = self.fields["layout"].queryset.filter(planta=planta)

class RegistroCapaForm(forms.ModelForm):
    class Meta:
        model = RegistroCapa
        fields = ["ingrediente_usado", "peso_real_g", "comentario"]
        widgets = {
            "peso_real_g": forms.NumberInput(attrs={"step": "0.1", "min": "0"}),
            "comentario": forms.TextInput(attrs={"placeholder": "Opcional"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ingrediente usado es opcional (si no seleccionas, se asume el planificado)
        self.fields["ingrediente_usado"].required = False
        self.fields["ingrediente_usado"].queryset = (
            Ingrediente.objects.filter(activo=True).order_by("categoria", "nombre")
        )

RegistroCapaFormSet = inlineformset_factory(
    RegistroLayout,
    RegistroCapa,
    form=RegistroCapaForm,
    extra=0,
    can_delete=False,
)
