from django.contrib import admin
from .models import (
    Cliente,
    Proveedor,
    Producto,
    Ingrediente,
    ProductoIngrediente,
    RegistroTrazabilidad,
    DetalleTrazabilidadIngrediente,
)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    search_fields = ["nombre"]
    list_display = ["nombre"]


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    search_fields = ["nombre"]
    list_display = ["nombre"]


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "cliente", "codigo", "codigo_registro", "version", "fecha_modificacion"]
    list_filter = ["cliente"]
    search_fields = ["nombre", "codigo", "codigo_registro", "version"]


@admin.register(Ingrediente)
class IngredienteAdmin(admin.ModelAdmin):
    search_fields = ["nombre"]
    list_display = ["nombre"]


@admin.register(ProductoIngrediente)
class ProductoIngredienteAdmin(admin.ModelAdmin):
    list_display = ["producto", "ingrediente", "proveedor", "orden"]
    list_filter = ["producto__cliente", "producto", "proveedor"]
    search_fields = ["producto__nombre", "ingrediente__nombre", "proveedor__nombre"]


class DetalleTrazabilidadIngredienteInline(admin.TabularInline):
    model = DetalleTrazabilidadIngrediente
    extra = 0


@admin.register(RegistroTrazabilidad)
class RegistroTrazabilidadAdmin(admin.ModelAdmin):
    list_display = [
        "producto",
        "cliente",
        "codigo_producto",
        "lote_producto",
        "fecha_elaboracion_producto",
        "fecha_registro",
        "elaborado_por",
    ]
    list_filter = ["cliente", "producto", "fecha_registro", "fecha_elaboracion_producto"]
    search_fields = [
        "producto__nombre",
        "codigo_producto",
        "lote_producto",
        "elaborado_por",
        "detalles__lote",
    ]
    inlines = [DetalleTrazabilidadIngredienteInline]
