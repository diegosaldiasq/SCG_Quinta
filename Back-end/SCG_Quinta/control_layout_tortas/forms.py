from django import forms
from django.forms import modelform_factory
from django.forms.models import inlineformset_factory
from .models import RegistroLayout, RegistroCapa


class RegistroLayoutForm(forms.ModelForm):
    class Meta:
        model = RegistroLayout
        fields = ["planta", "layout", "fecha", "turno", "linea", "lote", "operador", "observaciones"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "observaciones": forms.Textarea(attrs={"rows": 2}),
        }


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
