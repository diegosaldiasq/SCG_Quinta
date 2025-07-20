from django.contrib import admin

# Register your models here.

from .models import TurnoOEE, ResumenTurnoOee

@admin.register(TurnoOEE)
class TurnoOEEAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'cliente', 'producto', 'linea', 'turno', 'numero_personas', 'lote')
    search_fields = ('cliente', 'producto', 'linea', 'turno')
    list_filter = ('fecha', 'linea', 'turno')   
    ordering = ('-fecha',)  

@admin.register(ResumenTurnoOee)    
class ResumenTurnoOeeAdmin(admin.ModelAdmin):
    # todas las columnas que se mostrarán en la lista
    list_display = ('fecha', 'cliente', 'producto', 'linea', 'turno', 'lote', 'supervisor', 'tiempo_paro', 'produccion_real', 'oee', 'verificado')
    search_fields = ('cliente', 'producto', 'linea', 'turno', 'lote__lote')
    list_filter = ('fecha', 'linea', 'turno', 'verificado')
    ordering = ('-fecha',)  # Ordenar por fecha de forma descendente