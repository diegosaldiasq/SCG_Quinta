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
            "cliente": forms.TextInput(attrs={"class": "form-control", "placeholder": "Cliente"}),
            "producto": forms.TextInput(attrs={"class": "form-control", "placeholder": "Producto"}),
            "codigo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Código"}),
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