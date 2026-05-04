from django.contrib import admin
from .models import RegistroTemperaturaPostSpiral, DetalleTemperaturaPostSpiral


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
        'cantidad_temperaturas',
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

@admin.register(DetalleTemperaturaPostSpiral)
class DetalleTemperaturaPostSpiralAdmin(admin.ModelAdmin):
    list_display = [
        'registro',
        'numero',
        'temperatura',
        'accion_correctiva',
        'creado_en',
    ]

    search_fields = [
        'registro__cliente',
        'registro__producto',
        'registro__codigo',
        'registro__lote',
    ]

    list_filter = [
        'registro__turno',
        'registro__cliente',
    ]