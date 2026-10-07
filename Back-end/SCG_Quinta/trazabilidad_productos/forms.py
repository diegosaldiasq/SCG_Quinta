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
    turno = forms.ChoiceField(required=False, choices=[("", "Todos los turnos")])
    linea = forms.ChoiceField(required=False, choices=[("", "Todas las líneas")])
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo, etiqueta in (("turno", "Todos los turnos"), ("linea", "Todas las líneas")):
            valores = (
                RegistroTrazabilidad.objects
                .exclude(**{f"{campo}__isnull": True})
                .exclude(**{campo: ""})
                .order_by(campo)
                .values_list(campo, flat=True)
                .distinct()
            )
            self.fields[campo].choices = [("", etiqueta)] + [(valor, valor) for valor in valores]