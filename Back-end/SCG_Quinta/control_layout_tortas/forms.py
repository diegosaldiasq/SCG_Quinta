from django import forms
from django.forms import modelform_factory
from django.forms.models import inlineformset_factory
from .models import RegistroLayout, RegistroCapa, LayoutTorta


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

        # 🚫 1. Por defecto: NO mostrar ningún layout
        self.fields["layout"].required = False
        self.fields["layout"].queryset = LayoutTorta.objects.none()

        # 🔍 2. Detectar planta (POST o instancia)
        planta = None

        if self.data.get("planta"):
            # cuando el usuario selecciona planta y envía el form
            planta = self.data.get("planta")
        elif self.instance and self.instance.planta:
            # cuando se vuelve a cargar el form (ej: error)
            planta = self.instance.planta

        # ✅ 3. Si hay planta, mostrar SOLO layouts activos de esa planta
        if planta:
            self.fields["layout"].queryset = (
                LayoutTorta.objects
                .filter(activo=True, planta=planta)
                .select_related("producto")
            )

RegistroCapaForm = modelform_factory(
    RegistroCapa,
    fields=["peso_real_g", "comentario"],
    widgets={
        "peso_real_g": forms.NumberInput(attrs={"step": "0.1", "min": "0"}),
        "comentario": forms.TextInput(attrs={"placeholder": "Opcional"}),
    },
)

RegistroCapaFormSet = inlineformset_factory(
    RegistroLayout,
    RegistroCapa,
    form=RegistroCapaForm,
    fields=["peso_real_g", "comentario"],
    extra=0,
    can_delete=False,
)
