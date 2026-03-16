from django import forms
from django.forms import modelform_factory
from django.forms.models import inlineformset_factory
from .models import RegistroLayout, RegistroCapa, LayoutTorta, Ingrediente


class RegistroLayoutForm(forms.ModelForm):
    cliente = forms.ChoiceField(
        required=False,
        choices=[],
        label="Cliente"
    )
    producto_manual = forms.ChoiceField(
        required=False,
        choices=[],
        label="Producto"
    )
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
            "observaciones",
        ]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "observaciones": forms.Textarea(attrs={"rows": 2}),
            "layout": forms.HiddenInput(),  # ocultamos el layout real
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["layout"].required = False

        layouts_qs = (
            LayoutTorta.objects
            .filter(activo=True)
            .select_related("producto")
            .order_by("planta", "producto__cliente", "producto__nombre", "producto__codigo", "-version")
        )

        self.fields["layout"].queryset = layouts_qs

        planta = None
        cliente = None

        if self.data.get("planta"):
            planta = self.data.get("planta")
        elif self.instance and self.instance.pk:
            planta = self.instance.planta

        if self.data.get("cliente"):
            cliente = self.data.get("cliente")

        clientes = layouts_qs
        if planta:
            clientes = clientes.filter(planta=planta)

        clientes_unicos = []
        vistos = set()
        for item in clientes:
            c = (item.producto.cliente or "").strip()
            if c and c not in vistos:
                vistos.add(c)
                clientes_unicos.append((c, c))

        self.fields["cliente"].choices = [("", "Selecciona cliente")] + clientes_unicos

        productos = layouts_qs
        if planta:
            productos = productos.filter(planta=planta)
        if cliente:
            productos = productos.filter(producto__cliente=cliente)

        productos_unicos = []
        vistos_prod = set()
        for item in productos:
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

        # Ingrediente usado es opcional (si no seleccionas, se asume el planificado)
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
