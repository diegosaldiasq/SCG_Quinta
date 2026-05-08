from django.contrib import admin
from .models import DatosFormularioControlDePesosInsumosKuchen


@admin.register(DatosFormularioControlDePesosInsumosKuchen)
class DatosFormularioControlDePesosInsumosKuchenAdmin(admin.ModelAdmin):
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

    list_filter = (
        "cliente",
        "turno",
        "verificado",
        "fecha_registro",
    )

    search_fields = (
        "cliente",
        "codigo_producto",
        "producto",
        "lote",
        "nombre_tecnologo",
    )

    ordering = ("-fecha_registro",)
    list_per_page = 50