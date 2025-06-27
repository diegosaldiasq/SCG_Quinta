from django import forms
from .models import TurnoOEE

class TurnoOEEForm(forms.ModelForm):
    class Meta:
        model = TurnoOEE
        fields = ['fecha', 'cliente', 'codigo', 'producto', 'linea', 'turno', 'hora_inicio', 'hora_fin', 'tiempo_planeado', 'produccion_planeada']

class ProduccionRealForm(forms.ModelForm):
    class Meta:
        model = TurnoOEE
        fields = ['produccion_real']