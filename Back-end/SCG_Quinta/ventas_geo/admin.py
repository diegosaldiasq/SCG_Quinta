from django.contrib import admin
from .models import Producto, Local, Venta, CargaVentas, ErrorCargaVenta


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'direccion', 'comuna', 'ciudad', 'latitud', 'longitud')
    search_fields = ('nombre', 'direccion', 'comuna', 'ciudad')
    list_filter = ('ciudad', 'comuna')


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'local', 'cantidad', 'fecha', 'carga')
    search_fields = ('producto__nombre', 'local__nombre', 'local__direccion')
    list_filter = ('fecha', 'producto')


@admin.register(CargaVentas)
class CargaVentasAdmin(admin.ModelAdmin):
    list_display = ('id', 'archivo', 'fecha_carga', 'procesado', 'filas_leidas', 'filas_ok', 'filas_error')
    readonly_fields = ('fecha_carga',)


@admin.register(ErrorCargaVenta)
class ErrorCargaVentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'carga', 'fila_excel', 'mensaje', 'creado_en')
    search_fields = ('mensaje',)