from django.contrib import admin
from .models import RegistroTemperaturaPostSpiral


@admin.register(RegistroTemperaturaPostSpiral)
class RegistroTemperaturaPostSpiralAdmin(admin.ModelAdmin):
    list_display = [
        'fecha_hora',
        'usuario',
        'turno',
        'cliente',
        'producto',
        'codigo',
        'lote',
        'temperatura',
        'acciones_correctivas_verificadas',
        'verificado',
    ]

    list_filter = [
        'turno',
        'cliente',
        'verificado',
        'acciones_correctivas_requieren_revision',
        'acciones_correctivas_verificadas',
    ]

    search_fields = [
        'usuario',
        'cliente',
        'producto',
        'codigo',
        'lote',
    ]

    readonly_fields = [
        'cliente',
        'producto',
        'codigo',
        'creado_en',
        'actualizado_en',
        'fecha_verificacion',
        'nombre_verificador',
        'fecha_revision_accion_correctiva',
        'nombre_revisor_accion_correctiva',
    ]