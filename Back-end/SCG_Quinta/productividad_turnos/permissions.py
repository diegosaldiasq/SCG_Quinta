from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from .models import AsignacionProductividad, ProgramacionTurno


def require_permission(codename):
    def decorate(view):
        @login_required
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            if not request.user.is_active or not request.user.has_perm(f"productividad_turnos.{codename}"):
                raise PermissionDenied("No tiene permiso para esta operación.")
            return view(request, *args, **kwargs)
        return wrapped
    return decorate


def scoped_programs(user):
    qs = ProgramacionTurno.objects.select_related("area", "registro", "registro__creado_por", "registro__cerrado_por")
    if user.is_active and user.is_superuser:
        return qs
    assignments = AsignacionProductividad.objects.filter(usuario=user).values_list("planta", "area_id")
    condition = Q(pk__in=[])
    for planta, area_id in assignments:
        condition |= Q(planta=planta, area_id=area_id)
    return qs.filter(condition)


def assert_scope(user, planta, area_id, permission):
    if not user.is_active or not user.has_perm(f"productividad_turnos.{permission}"):
        raise PermissionDenied("Operación no autorizada.")
    if not user.is_superuser and not AsignacionProductividad.objects.filter(usuario=user, planta=planta, area_id=area_id).exists():
        raise PermissionDenied("No tiene acceso a esta planta y área.")


def user_label(user):
    return getattr(user, "nombre_completo", "") or user.get_full_name() or user.get_username()
