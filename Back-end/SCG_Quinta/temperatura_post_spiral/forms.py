from django import forms

from control_sala_cremas.models import ProductoSalaCremas
from .models import RegistroTemperaturaPostSpiral, DetalleTemperaturaPostSpiral
from django.forms import inlineformset_factory
from decimal import Decimal, InvalidOperation


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

    temperatura_permanencia = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control input-temperatura',
            'inputmode': 'decimal',
            'autocomplete': 'off',
            'placeholder': 'Ej: -12.0'
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
            'temperatura_permanencia',
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
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones generales'
            }),
        }

    def clean_temperatura_permanencia(self):
        valor = self.cleaned_data.get('temperatura_permanencia')

        if valor in [None, '']:
            return None

        valor = str(valor).strip().replace(',', '.')

        try:
            return Decimal(valor)
        except InvalidOperation:
            raise forms.ValidationError('Ingrese una temperatura válida.')

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

class DetalleTemperaturaPostSpiralForm(forms.ModelForm):

    temperatura = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control input-temperatura',
            'inputmode': 'decimal',
            'autocomplete': 'off',
            'placeholder': 'Ej: -12.0'
        })
    )

    class Meta:
        model = DetalleTemperaturaPostSpiral
        fields = [
            'temperatura',
            'accion_correctiva',
        ]

        widgets = {
            'accion_correctiva': forms.Textarea(attrs={
                'class': 'form-control input-accion',
                'rows': 2,
                'placeholder': 'Completar solo si aplica'
            }),
        }

    def clean_temperatura(self):

        valor = self.cleaned_data.get('temperatura')

        if valor in [None, '']:
            return None

        valor = str(valor).strip().replace(',', '.')

        try:
            return Decimal(valor)
        except InvalidOperation:
            raise forms.ValidationError(
                'Ingrese una temperatura válida.'
            )


DetalleTemperaturaPostSpiralFormSet = inlineformset_factory(
    RegistroTemperaturaPostSpiral,
    DetalleTemperaturaPostSpiral,
    form=DetalleTemperaturaPostSpiralForm,
    extra=0,
    max_num=100,
    min_num=10,
    validate_min=True,
    can_delete=False
)