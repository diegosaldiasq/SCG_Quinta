from django import forms
from .models import TurnoOEE

# Definición de opciones para los campos de selección
CLIENTES = [
    ("Cliente A", "Cliente A"),
    ("Cliente B", "Cliente B"),
    ("Cliente C", "Cliente C"),
]

CODIGOS = [
    ("COD001", "COD001"),
    ("COD002", "COD002"),
    ("COD003", "COD003"),
]

PRODUCTOS = [
    ("Producto X", "Producto X"),
    ("Producto Y", "Producto Y"),
    ("Producto Z", "Producto Z"),
]

class TurnoOEEForm(forms.ModelForm):
    cliente = forms.ChoiceField(choices=CLIENTES, widget=forms.Select(attrs={'class': 'input'}))
    codigo = forms.ChoiceField(choices=CODIGOS, widget=forms.Select(attrs={'class': 'input'}))
    producto = forms.ChoiceField(choices=PRODUCTOS, widget=forms.Select(attrs={'class': 'input'}))
    fecha = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.TextInput(attrs={
            'placeholder': 'DD-MM-YYYY',
            'pattern': '\\d{2}-\\d{2}-\\d{4}',  # Validación HTML
            'class': 'input'
        })
    )
    class Meta:
        model = TurnoOEE
        fields = ['fecha', 'cliente', 'codigo', 'producto', 'linea', 'turno', 'hora_inicio', 'hora_fin', 'tiempo_planeado', 'produccion_planeada']

class ProduccionRealForm(forms.ModelForm):
    class Meta:
        model = TurnoOEE
        fields = ['produccion_real']