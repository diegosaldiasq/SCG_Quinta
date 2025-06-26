from django import forms
from .models import TurnoOEE

class TurnoOEEForm(forms.ModelForm):
    class Meta:
        model = TurnoOEE
        fields = ['fecha', 'linea', 'turno', 'hora_inicio', 'hora_fin', 'tiempo_planeado']

class ProduccionRealForm(forms.ModelForm):
    class Meta:
        model = TurnoOEE
        fields = ['produccion_real']