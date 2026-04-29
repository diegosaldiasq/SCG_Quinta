from django import forms

from control_sala_cremas.models import ProductoSalaCremas
from .models import RegistroTemperaturaPostSpiral


class RegistroTemperaturaPostSpiralForm(forms.ModelForm):
    cliente_selector = forms.ChoiceField(
        label='Cliente',
        required=True,
        choices=[],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_cliente_selector'
        })
    )

    class Meta:
        model = RegistroTemperaturaPostSpiral
        fields = [
            'cliente_selector',
            'producto_sala_cremas',
            'turno',
            'lote',
            'tiempo_permanencia_producto',
            'temperatura',
            'accion_correctiva',
            'observaciones',
        ]

        widgets = {
            'producto_sala_cremas': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_producto_sala_cremas'
            }),
            'turno': forms.Select(attrs={'class': 'form-control'}),
            'lote': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese lote'
            }),
            'tiempo_permanencia_producto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 45 min'
            }),
            'temperatura': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Ej: 4.5'
            }),
            'accion_correctiva': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Completar solo si aplica'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones generales'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        clientes = (
            ProductoSalaCremas.objects
            .exclude(cliente__isnull=True)
            .exclude(cliente__exact='')
            .values_list('cliente', flat=True)
            .distinct()
            .order_by('cliente')
        )

        self.fields['cliente_selector'].choices = [('', 'Seleccione cliente')] + [
            (cliente, cliente) for cliente in clientes
        ]

        self.fields['producto_sala_cremas'].queryset = ProductoSalaCremas.objects.none()
        self.fields['producto_sala_cremas'].empty_label = 'Seleccione producto'

        if 'cliente_selector' in self.data:
            cliente = self.data.get('cliente_selector')
            self.fields['producto_sala_cremas'].queryset = ProductoSalaCremas.objects.filter(
                cliente=cliente
            ).order_by('producto')

        elif self.instance and self.instance.pk:
            self.fields['producto_sala_cremas'].queryset = ProductoSalaCremas.objects.filter(
                cliente=self.instance.cliente
            ).order_by('producto')
            self.fields['cliente_selector'].initial = self.instance.cliente