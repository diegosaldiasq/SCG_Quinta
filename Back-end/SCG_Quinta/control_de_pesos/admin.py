from django.contrib import admin
from .models import DatosFormularioControlDePesos, ProductoControlPeso


@admin.register(ProductoControlPeso)
class ProductoControlPesoAdmin(admin.ModelAdmin):
    list_display = (
        "area",
        "cliente",
        "codigo",
        "producto",
        "peso_receta",
        "un_pp",
        "porcentaje_perdida",
        "altura",
        "activo",
    )
    list_filter = ("area", "cliente", "activo")
    search_fields = ("cliente", "codigo", "producto")
    list_editable = ("peso_receta", "un_pp", "porcentaje_perdida", "altura", "activo")


@admin.register(DatosFormularioControlDePesos)
class DatosFormularioControlDePesosAdmin(admin.ModelAdmin):
    list_display = (
        "fecha_registro",
        "nombre_tecnologo",
        "cliente",
        "codigo_producto",
        "producto",
        "peso_receta",
        "peso_real",
        "altura",
        "lote",
        "turno",
        "verificado",
    )
    list_filter = ("cliente", "turno", "verificado")
    search_fields = ("producto", "codigo_producto", "lote", "nombre_tecnologo")