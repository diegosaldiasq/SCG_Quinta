from django.contrib import admin
from .models import ProductoTorta, LayoutTorta, LayoutCapa, RegistroLayout, RegistroCapa, Ingrediente


class LayoutCapaInline(admin.TabularInline):
    model = LayoutCapa
    extra = 0
    ordering = ("orden",)
    autocomplete_fields = ("ingrediente",)


@admin.register(LayoutTorta)
class LayoutTortaAdmin(admin.ModelAdmin):
    list_display = ("planta", "producto", "version", "activo", "creado_en")
    list_filter = ("planta", "activo", "producto__cliente")
    search_fields = ("producto__nombre", "producto__codigo")
    inlines = [LayoutCapaInline]
    autocomplete_fields = ("producto",)


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

@admin.register(Ingrediente)
class IngredienteAdmin(admin.ModelAdmin):
    list_display = ("categoria", "nombre", "activo", "codigo_interno", "proveedor")
    list_filter = ("categoria", "activo")
    search_fields = ("nombre", "codigo_interno", "proveedor")

@admin.register(LayoutCapa)
class LayoutCapaAdmin(admin.ModelAdmin):
    list_display = ("layout", "orden", "tipo", "peso_objetivo_g")
    list_filter = ("tipo", "layout__planta", "layout__activo")
    search_fields = ("layout__producto__nombre", "layout__producto__codigo")
    ordering = ("layout", "orden")
