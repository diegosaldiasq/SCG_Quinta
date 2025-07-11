from django import forms
from .models import TurnoOEE

class TurnoOEEForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'input',
            'id': 'id_fecha',
        }),
        help_text="Fecha del turno"
    )
    CLIENTE_CHOICES = [
        ('Jumbo', 'Jumbo'),
        ('SISA', 'SISA'),
        ('Walmart', 'Walmart'),
        ('Unimarc', 'Unimarc'),
    ]
    cliente = forms.ChoiceField(
        choices=[('', '--Seleccionar cliente--')] + CLIENTE_CHOICES,
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
    turno = forms.CharField(
        required=True,
        help_text="Turno es igual al lote del turno, ej: 123BCA",
        widget=forms.TextInput(attrs={
            'id': 'id_turno',
            'placeholder': '123BCA'
        })
    )
    LINEA_CHOICES = [
        ('Línea 1', 'Línea 1'),
        ('Línea 2', 'Línea 2'),
        ('Línea 3', 'Línea 3'),
        ('Línea 3A', 'Línea 3A'),
        ('Línea 3B', 'Línea 3B'),
        ('Isla', 'Isla'),
        ('Gorreri pasteleria', 'Gorreri pasteleria'),
        ('Gorreri kuchen', 'Gorreri kuchen'),
    ]
    linea    = forms.ChoiceField(
        choices= [('', '--Seleccionar linea--')] + LINEA_CHOICES,
        widget=forms.Select(attrs={'id': 'id_linea'}))
    class Meta:
        model = TurnoOEE
        fields = ['fecha', 'cliente', 'producto', 'codigo', 'linea', 'turno', 'hora_inicio', 'hora_fin', 'tiempo_planeado', 'produccion_planeada']
        widgets = {
            'hora_inicio': forms.TimeInput(format='%H:%M', attrs={
                'type': 'time', 'id': 'id_hora_inicio'
            }),
            'hora_fin':    forms.TimeInput(format='%H:%M', attrs={
                'type': 'time', 'id': 'id_hora_fin'
            }),
            'tiempo_planeado': forms.NumberInput(attrs={
                'readonly': 'readonly',
                'id': 'id_tiempo_planeado',
                'placeholder': 'Se calcula automáticamente'
            }),
            # … otros widgets …
        }

class ProduccionRealForm(forms.ModelForm):
    class Meta:
        model = TurnoOEE
        fields = ['produccion_real']