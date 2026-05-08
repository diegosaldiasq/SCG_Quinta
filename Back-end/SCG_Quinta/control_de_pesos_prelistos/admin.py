from django.contrib import admin

from .models import (
    DatosFormularioControlDePesosPrelistos
)


@admin.register(DatosFormularioControlDePesosPrelistos)
class DatosFormularioControlDePesosPrelistosAdmin(admin.ModelAdmin):

    list_display = (
        "fecha_registro",
        "nombre_tecnologo",
        "cliente",
        "codigo_producto",
        "producto",
        "peso_receta",
        "peso_real",
        "altura",
        "desviacion_porcentaje",
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

    readonly_fields = (
        "fecha_registro",
        "desviacion_porcentaje",
    )

    ordering = (
        "-fecha_registro",
    )

    list_per_page = 50