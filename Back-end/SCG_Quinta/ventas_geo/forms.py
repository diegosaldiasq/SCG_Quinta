from django import forms
from .models import CargaVentas


class CargaVentasForm(forms.ModelForm):
    class Meta:
        model = CargaVentas
        fields = ['archivo', 'observacion']
        widgets = {
            'observacion': forms.Textarea(attrs={'rows': 3}),
        }