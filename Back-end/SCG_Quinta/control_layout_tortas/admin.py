from django.contrib import admin
from .models import ProductoTorta, LayoutTorta, LayoutCapa, RegistroLayout, RegistroCapa


class LayoutCapaInline(admin.TabularInline):
    model = LayoutCapa
    extra = 0
    ordering = ("orden",)


@admin.register(LayoutTorta)
class LayoutTortaAdmin(admin.ModelAdmin):
    list_display = ("planta", "producto", "version", "activo", "creado_en")
    list_filter = ("planta", "activo", "producto__cliente")
    search_fields = ("producto__nombre", "producto__codigo")
    inlines = [LayoutCapaInline]


@admin.register(ProductoTorta)
class ProductoTortaAdmin(admin.ModelAdmin):
    list_display = ("cliente", "nombre", "codigo")
    search_fields = ("cliente", "nombre", "codigo")


class RegistroCapaInline(admin.TabularInline):
    model = RegistroCapa
    extra = 0
    readonly_fields = ()
    autocomplete_fields = ("capa",)


@admin.register(RegistroLayout)
class RegistroLayoutAdmin(admin.ModelAdmin):
    list_display = ("fecha", "planta", "layout", "turno", "linea", "lote", "operador")
    list_filter = ("planta", "fecha")
    search_fields = ("layout__producto__nombre", "layout__producto__codigo", "lote", "operador")
    inlines = [RegistroCapaInline]
