from django import forms
from .models import RegistroSalaCremas
from control_de_pesos.models import ProductoControlPeso


class RegistroSalaCremasForm(forms.ModelForm):

    producto_control_peso = forms.ModelChoiceField(
        queryset=ProductoControlPeso.objects.filter(
            activo=True,
            area='TORTAS'
        ).order_by('cliente', 'producto'),
        label='Producto',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_producto_control_peso'
        })
    )

    class Meta:
        model = RegistroSalaCremas
        fields = [
            "turno",
            "producto_control_peso",
            "lote",
            "tipo_crema",
            "aplicacion",
            "densidad",
            "temperatura",
            "numero_batidora",
            "observaciones",
        ]

        widgets = {
            "turno": forms.Select(attrs={"class": "form-control"}),

            "lote": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Lote"
            }),

            "tipo_crema": forms.Select(attrs={"class": "form-control"}),
            "aplicacion": forms.Select(attrs={"class": "form-control"}),

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