from django import forms
from .models import TurnoOEE

class TurnoOEEForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',  # Calendario nativo del navegador
            'class': 'input',
            'placeholder': 'dd-mm-yyyy',
        },
        input_formats=['%d-%m-%Y']  # Formato de fecha esperado
        ))
    class Meta:
        model = TurnoOEE
        fields = ['fecha', 'cliente', 'producto', 'codigo', 'linea', 'turno', 'hora_inicio', 'hora_fin', 'tiempo_planeado', 'produccion_planeada']

class ProduccionRealForm(forms.ModelForm):
    class Meta:
        model = TurnoOEE
        fields = ['produccion_real']