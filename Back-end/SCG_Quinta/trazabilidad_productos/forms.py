from django import forms
from .models import RegistroTrazabilidad, Cliente, Producto


class RegistroTrazabilidadForm(forms.ModelForm):
    class Meta:
        model = RegistroTrazabilidad
        fields = [
            "cliente",
            "producto",
            "codigo_producto",
            "lote_producto",
            "fecha_elaboracion_producto",
            "turno",
            "linea",
            "elaborado_por",
            "observaciones",
        ]
        widgets = {
            "codigo_producto": forms.TextInput(attrs={"readonly": "readonly"}),
            "fecha_elaboracion_producto": forms.DateInput(attrs={"type": "date"}),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        cliente = cleaned_data.get("cliente")
        producto = cleaned_data.get("producto")

        if cliente and producto and producto.cliente_id != cliente.id:
            self.add_error("producto", "El producto seleccionado no pertenece al cliente elegido.")

        return cleaned_data


class HistorialTrazabilidadFilterForm(forms.Form):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all().order_by("nombre"),
        required=False
    )
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all().order_by("nombre"),
        required=False
    )
    desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"})
    )
    hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"})
    )
    lote_producto = forms.CharField(required=False)
    lote_ingrediente = forms.CharField(required=False)

    estado_verificacion = forms.ChoiceField(
        required=False,
        choices=[
            ("", "Todos"),
            ("no_verificados", "No verificadas"),
            ("verificados", "Verificadas"),
        ]
    )