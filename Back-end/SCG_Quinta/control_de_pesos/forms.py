from django import forms

from .models import ProductoControlPeso


class ProductoControlPesoForm(forms.ModelForm):
    class Meta:
        model = ProductoControlPeso
        fields = (
            "area",
            "cliente",
            "codigo",
            "producto",
            "peso_receta",
            "porcentaje_perdida",
            "altura",
            "diff_altura",
            "un_pp",
            "activo",
        )

        labels = {
            "area": "Área",
            "cliente": "Cliente",
            "codigo": "Código",
            "producto": "Producto",
            "peso_receta": "Peso receta (gr)",
            "porcentaje_perdida": "Pérdida operacional (%)",
            "altura": "Altura objetivo (mm)",
            "diff_altura": "Diferencia de altura (mm)",
            "un_pp": "Unidades por persona",
            "activo": "Producto activo",
        }

        widgets = {
            "area": forms.Select(attrs={
                "class": "campo-formulario",
            }),
            "cliente": forms.Select(attrs={
                "class": "campo-formulario",
            }),
            "codigo": forms.TextInput(attrs={
                "class": "campo-formulario",
                "placeholder": "Ej: 393040",
                "autocomplete": "off",
            }),
            "producto": forms.TextInput(attrs={
                "class": "campo-formulario",
                "placeholder": "Nombre del producto",
                "autocomplete": "off",
            }),
            "peso_receta": forms.NumberInput(attrs={
                "class": "campo-formulario",
                "min": "0",
                "step": "1",
            }),
            "porcentaje_perdida": forms.NumberInput(attrs={
                "class": "campo-formulario",
                "min": "0",
                "max": "99.99",
                "step": "0.01",
            }),
            "altura": forms.NumberInput(attrs={
                "class": "campo-formulario",
                "min": "0",
                "step": "1",
                "placeholder": "Opcional",
            }),
            "diff_altura": forms.NumberInput(attrs={
                "class": "campo-formulario",
                "min": "0",
                "step": "0.01",
            }),
            "un_pp": forms.NumberInput(attrs={
                "class": "campo-formulario",
                "min": "0",
                "step": "0.01",
                "placeholder": "Opcional",
            }),
            "activo": forms.CheckboxInput(attrs={
                "class": "campo-checkbox",
            }),
        }

    def clean_codigo(self):
        return self.cleaned_data["codigo"].strip()

    def clean_producto(self):
        return self.cleaned_data["producto"].strip()

    def clean_porcentaje_perdida(self):
        porcentaje = self.cleaned_data["porcentaje_perdida"]

        if porcentaje < 0 or porcentaje >= 100:
            raise forms.ValidationError(
                "La pérdida debe estar entre 0 y 99,99%."
            )

        return porcentaje

    def clean_diff_altura(self):
        diferencia = self.cleaned_data["diff_altura"]

        if diferencia is not None and diferencia < 0:
            raise forms.ValidationError(
                "La diferencia de altura no puede ser negativa."
            )

        return diferencia