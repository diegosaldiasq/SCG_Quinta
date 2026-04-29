from django import forms
from .models import RegistroSalaCremas


class RegistroSalaCremasForm(forms.ModelForm):
    class Meta:
        model = RegistroSalaCremas
        fields = [
            "turno",
            "cliente",
            "producto",
            "codigo",
            "lote",
            "densidad",
            "temperatura",
            "numero_batidora",
            "observaciones",
        ]

        widgets = {
            "turno": forms.Select(attrs={"class": "form-control"}),
            "cliente": forms.Select(attrs={"class": "form-control", "id": "id_cliente"}),
            "producto": forms.Select(attrs={"class": "form-control", "id": "id_producto"}),
            "codigo": forms.TextInput(attrs={
                "class": "form-control",
                "id": "id_codigo",
                "readonly": "readonly",
            }),
            "lote": forms.TextInput(attrs={"class": "form-control", "placeholder": "Lote"}),
            "densidad": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.001",
                "placeholder": "Ej: 0.850",
            }),
            "temperatura": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "Ej: 18.5",
            }),
            "numero_batidora": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "N° batidora",
            }),
            "observaciones": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Observaciones del proceso",
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["cliente"].choices = [("", "Seleccione cliente")]
        self.fields["producto"].choices = [("", "Seleccione producto")]