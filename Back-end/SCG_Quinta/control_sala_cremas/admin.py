from django.contrib import admin
from .models import RegistroSalaCremas, ProductoSalaCremas


@admin.register(ProductoSalaCremas)
class ProductoSalaCremasAdmin(admin.ModelAdmin):
    list_display = ("cliente", "producto", "codigo", "activo")
    list_filter = ("cliente", "activo")
    search_fields = ("cliente", "producto", "codigo")


@admin.register(RegistroSalaCremas)
class RegistroSalaCremasAdmin(admin.ModelAdmin):
    list_display = (
        "fecha_hora",
        "usuario",
        "turno",
        "cliente",
        "producto",
        "codigo",
        "lote",
        "densidad",
        "temperatura",
        "numero_batidora",
        "verificado",
        "verificado_por",
        "fecha_verificacion",
    )
    list_filter = ("turno", "cliente", "verificado", "numero_batidora")
    search_fields = ("cliente", "producto", "codigo", "lote", "usuario")