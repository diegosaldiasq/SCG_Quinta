from django import forms
from django.forms.models import inlineformset_factory
from .models import RegistroLayout, RegistroCapa, LayoutTorta, Ingrediente


class RegistroLayoutForm(forms.ModelForm):
    cliente = forms.ChoiceField(required=False, choices=[], label="Cliente")
    producto_manual = forms.ChoiceField(required=False, choices=[], label="Producto")
    codigo_auto = forms.CharField(
        required=False,
        label="Código",
        widget=forms.TextInput(attrs={"readonly": "readonly"})
    )

    class Meta:
        model = RegistroLayout
        fields = [
            "planta",
            "layout",
            "fecha",
            "turno",
            "linea",
            "lote",
            "operador",
            "peso_real_obtenido_g",
            "observaciones",
        ]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "observaciones": forms.Textarea(attrs={"rows": 2}),
            "layout": forms.HiddenInput(),
            "operador": forms.TextInput(attrs={"readonly": "readonly"}),
            "peso_real_obtenido_g": forms.NumberInput(attrs={"step": "0.1", "min": "0"}),
        }

    def __init__(self, *args, **kwargs):
        operador_inicial = kwargs.pop("operador_inicial", "")
        super().__init__(*args, **kwargs)

        self.fields["layout"].required = False

        if operador_inicial and not self.initial.get("operador"):
            self.initial["operador"] = operador_inicial

        layouts_qs = (
            LayoutTorta.objects
            .filter(activo=True)
            .select_related("producto")
            .order_by("planta", "producto__cliente", "producto__nombre", "producto__codigo", "-version")
        )

        self.fields["layout"].queryset = layouts_qs

        planta = self.data.get("planta") or getattr(self.instance, "planta", None)
        cliente = self.data.get("cliente") or self.initial.get("cliente")

        clientes_qs = layouts_qs
        if planta:
            clientes_qs = clientes_qs.filter(planta=planta)

        clientes_unicos = []
        vistos = set()
        for item in clientes_qs:
            c = (item.producto.cliente or "").strip()
            if c and c not in vistos:
                vistos.add(c)
                clientes_unicos.append((c, c))

        self.fields["cliente"].choices = [("", "Selecciona cliente")] + clientes_unicos

        productos_qs = layouts_qs
        if planta:
            productos_qs = productos_qs.filter(planta=planta)
        if cliente:
            productos_qs = productos_qs.filter(producto__cliente=cliente)

        productos_unicos = []
        vistos_prod = set()
        for item in productos_qs:
            key = (item.producto.id, item.producto.nombre)
            if key not in vistos_prod:
                vistos_prod.add(key)
                productos_unicos.append((item.producto.id, item.producto.nombre))

        self.fields["producto_manual"].choices = [("", "Selecciona producto")] + productos_unicos


class RegistroCapaForm(forms.ModelForm):
    class Meta:
        model = RegistroCapa
        fields = ["ingrediente_usado", "peso_real_g", "comentario"]
        widgets = {
            "peso_real_g": forms.NumberInput(attrs={"step": "0.1", "min": "0"}),
            "comentario": forms.TextInput(attrs={"placeholder": "Opcional"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ingrediente_usado"].required = False
        self.fields["ingrediente_usado"].queryset = (
            Ingrediente.objects.filter(activo=True).order_by("categoria", "nombre")
        )


RegistroCapaFormSet = inlineformset_factory(
    RegistroLayout,
    RegistroCapa,
    form=RegistroCapaForm,
    extra=0,
    can_delete=False,
)

class HistorialRegistroFilterForm(forms.Form):
    planta = forms.ChoiceField(
        required=False,
        choices=[("", "Todas")] + list(RegistroLayout._meta.get_field("planta").choices),
        label="Planta",
    )
    turno = forms.ChoiceField(
        required=False,
        choices=[("", "Todos")] + list(RegistroLayout._meta.get_field("turno").choices),
        label="Turno",
    )
    linea = forms.ChoiceField(
        required=False,
        choices=[("", "Todas")] + list(RegistroLayout._meta.get_field("linea").choices),
        label="Línea",
    )
    layout = forms.ModelChoiceField(
        required=False,
        queryset=LayoutTorta.objects.select_related("producto").order_by("producto__cliente", "producto__nombre"),
        label="Layout",
        empty_label="Todos",
    )
    desde = forms.DateField(
        required=False,
        label="Desde",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    hasta = forms.DateField(
        required=False,
        label="Hasta",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    lote = forms.CharField(
        required=False,
        label="Lote",
    )
    operador = forms.CharField(
        required=False,
        label="Operador",
    )
    verificado = forms.ChoiceField(
        required=False,
        label="Verificación",
        choices=[
            ("", "Todos"),
            ("si", "Verificados"),
            ("no", "No verificados"),
        ],
    )