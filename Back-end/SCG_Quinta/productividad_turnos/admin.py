from django.contrib import admin

from .models import AreaProductividad, AsignacionProductividad, ProgramacionTurno, RegistroProductividadTurno, RevisionProductividad


class SuperuserAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_active and request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_add_permission(self, request):
        return self.has_module_permission(request)

    def has_change_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_delete_permission(self, request, obj=None):
        return self.has_module_permission(request)


@admin.register(AreaProductividad)
class AreaAdmin(SuperuserAdmin):
    list_display = ("codigo", "nombre", "activo", "mide_semielaborado")
    search_fields = ("codigo", "nombre")

    def get_readonly_fields(self, request, obj=None):
        # No cambiar la población de un indicador histórico desde el catálogo.
        return ("codigo", "mide_semielaborado", "definicion_dotacion") if obj and obj.programacionturno_set.exists() else ()


@admin.register(AsignacionProductividad)
class AsignacionAdmin(SuperuserAdmin):
    list_display = ("usuario", "planta", "area")
    list_filter = ("planta", "area")
    raw_id_fields = ("usuario",)


class ReadOnlyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        # El admin técnico completo queda reservado al superusuario.
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.none()


@admin.register(ProgramacionTurno)
class ProgramacionAdmin(ReadOnlyAdmin):
    list_display = ("fecha_operativa", "planta", "area", "turno", "meta_pt", "programado")
    list_filter = ("planta", "area", "turno")


@admin.register(RegistroProductividadTurno)
class RegistroAdmin(ReadOnlyAdmin):
    list_display = ("programacion", "estado", "terminadas", "dotacion", "cerrado")
    list_filter = ("estado",)


@admin.register(RevisionProductividad)
class RevisionAdmin(ReadOnlyAdmin):
    list_display = ("programacion", "accion", "usuario", "fecha")
