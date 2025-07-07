from django import forms
from .models import TurnoOEE

class TurnoOEEForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',  # Calendario nativo del navegador
            'class': 'input',
            'placeholder': 'dd-mm-yyyy'
        }), 
        input_formats=['%d-%m-%Y'],  # Formato de entrada para el campo de fecha
        help_text="Fecha del turno (formato: DD-MM-YYYY)"
    )
    CLIENTE_CHOICES = [
        ('Cliente A', 'Cliente A'),
        ('Cliente B', 'Cliente B'),
        ('Cliente C', 'Cliente C'),
    ]
    cliente = forms.ChoiceField(
        choices=CLIENTE_CHOICES,
        widget=forms.Select(attrs={'id': 'id_cliente'})
    )
    producto = forms.ChoiceField(
        choices=[('', '--Seleccionar cliente primero--')],
        widget=forms.Select(attrs={'id': 'id_producto'})
    )
    codigo = forms.CharField(
        widget=forms.TextInput(attrs={
            'readonly': 'readonly',
            'id': 'id_codigo',
            'placeholder': 'Se autocompleta'
        })
    )
    class Meta:
        model = TurnoOEE
        fields = ['fecha', 'cliente', 'producto', 'codigo', 'linea', 'turno', 'hora_inicio', 'hora_fin', 'tiempo_planeado', 'produccion_planeada']

class ProduccionRealForm(forms.ModelForm):
    class Meta:
        model = TurnoOEE
        fields = ['produccion_real']