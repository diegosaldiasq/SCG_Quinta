from datetime import datetime, timedelta
from decimal import Decimal
from zoneinfo import ZoneInfo

from django.conf import settings
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.forms.models import model_to_dict
from django.utils import timezone

from .models import ProgramacionTurno, RegistroProductividadTurno, RevisionProductividad
from .permissions import assert_scope


def horario(fecha, turno):
    """La fecha operativa corresponde al día de término del turno A."""
    horarios = getattr(settings, "PRODUCTIVIDAD_HORARIOS", {"A": ["23:00", "07:00"], "B": ["07:00", "14:30"], "C": ["14:30", "22:00"]})
    tz = ZoneInfo(getattr(settings, "PRODUCTIVIDAD_TIME_ZONE", "America/Santiago"))
    inicio_h, fin_h = [datetime.strptime(v, "%H:%M").time() for v in horarios[turno]]
    dia_inicio = fecha - timedelta(days=1) if inicio_h >= fin_h else fecha
    inicio = datetime.combine(dia_inicio, inicio_h, tzinfo=tz)
    fin = datetime.combine(fecha, fin_h, tzinfo=tz)
    # Rechazar horas inexistentes o ambiguas durante un cambio de huso.
    for dt in (inicio, fin):
        if dt.astimezone(ZoneInfo("UTC")).astimezone(tz).replace(tzinfo=None) != dt.replace(tzinfo=None) or dt.replace(fold=0).utcoffset() != dt.replace(fold=1).utcoffset():
            raise ValidationError("Horario ambiguo o inexistente por cambio de hora. Ajuste PRODUCTIVIDAD_HORARIOS para esta programación.")
    return inicio, fin


def snapshot(obj):
    if obj is None:
        return {}
    def convert(value):
        if isinstance(value, Decimal):
            return str(value)
        if hasattr(value, "isoformat"):
            return value.isoformat()
        return value
    return {k: convert(v) for k, v in model_to_dict(obj).items()}


def audit(plan, user, action, before, after, reason=""):
    RevisionProductividad.objects.create(programacion=plan, usuario=user, accion=action, antes=before, despues=after, motivo=reason)


@transaction.atomic
def programar(user, data, pk=None, version=None):
    assert_scope(user, data["planta"], data["area"].pk, "programar_turno")
    plan = None
    if pk:
        plan = ProgramacionTurno.objects.select_for_update().get(pk=pk)
        assert_scope(user, plan.planta, plan.area_id, "programar_turno")
        if plan.version != version:
            raise ValidationError("La programación cambió. Recargue antes de editar.")
        if any(getattr(plan, key) != data[key] for key in ("fecha_operativa", "planta", "area", "turno")):
            raise ValidationError("La fecha, planta, área y turno de una programación existente no se pueden cambiar.")
        if RegistroProductividadTurno.objects.filter(programacion=plan).exclude(estado="BORRADOR").exists():
            raise ValidationError("Existe un cierre. Reábralo con motivo antes de modificar esta programación.")
        if not data.get("motivo", "").strip():
            raise ValidationError("Indique el motivo del ajuste de programación.")
    before = snapshot(plan)
    plan = plan or ProgramacionTurno(creado_por=user)
    for name in ("fecha_operativa", "planta", "area", "turno", "meta_pt", "programado", "extraordinario", "motivo"):
        setattr(plan, name, data[name])
    if not plan.area.activo:
        raise ValidationError("El área está inactiva.")
    if plan.meta_pt == 0 and not plan.motivo.strip():
        raise ValidationError("Una meta cero necesita motivo.")
    plan.inicio, plan.fin = horario(plan.fecha_operativa, plan.turno)
    if pk:
        plan.version += 1
    plan.full_clean()
    plan.save()
    audit(plan, user, "PROGRAMACION", before, snapshot(plan), plan.motivo)
    return plan


@transaction.atomic
def guardar_registro(user, plan_id, data, version, cerrar=False):
    plan = ProgramacionTurno.objects.select_for_update().select_related("area").get(pk=plan_id)
    assert_scope(user, plan.planta, plan.area_id, "registrar_turno")
    if cerrar:
        assert_scope(user, plan.planta, plan.area_id, "cerrar_turno")
    if not plan.programado or not plan.area.activo:
        raise ValidationError("El turno no está programado o su área está inactiva.")
    reg = RegistroProductividadTurno.objects.select_for_update().filter(programacion=plan).first()
    if (reg.version if reg else 0) != version:
        raise ValidationError("El registro cambió. Recargue la página para evitar sobrescribir otra edición.")
    if reg and reg.estado != "BORRADOR":
        raise ValidationError("El registro está cerrado. Debe reabrirse con autorización.")
    if reg and reg.creado_por_id != user.pk and not user.has_perm("productividad_turnos.reabrir_turno"):
        raise PermissionDenied("Solo el autor o un revisor autorizado puede editar este borrador.")
    before = snapshot(reg)
    reg = reg or RegistroProductividadTurno(programacion=plan, creado_por=user)
    for field in ("dotacion", "semielaborados", "terminadas", "horas_persona", "observaciones"):
        setattr(reg, field, data.get(field))
    reg.observaciones = reg.observaciones or ""
    if not plan.area.mide_semielaborado:
        reg.semielaborados = None
    if cerrar:
        if plan.fin > timezone.now():
            raise ValidationError("El turno aún no finaliza. Puede guardar un borrador.")
        if not reg.dotacion or reg.terminadas is None or (plan.area.mide_semielaborado and reg.semielaborados is None):
            raise ValidationError("Complete dotación mayor que cero y todas las cantidades aplicables.")
        if (reg.terminadas == 0 or (plan.area.mide_semielaborado and reg.semielaborados == 0)) and not data.get("confirmar_ceros"):
            raise ValidationError("Confirme que los valores cero son producción cero real.")
        if reg.terminadas == 0 and not reg.observaciones.strip():
            raise ValidationError("Explique la producción cero en observaciones.")
        reg.meta_pt_cierre = plan.meta_pt
        reg.cerrado, reg.cerrado_por, reg.estado = timezone.now(), user, "CERRADO"
    reg.version = (reg.version + 1) if reg.pk else 1
    reg.full_clean()
    reg.save()
    audit(plan, user, "CIERRE" if cerrar else "BORRADOR", before, snapshot(reg), reg.observaciones)
    return reg


@transaction.atomic
def cambiar_estado(user, plan_id, accion, version, motivo=""):
    plan = ProgramacionTurno.objects.select_for_update().get(pk=plan_id)
    permission = "verificar_turno" if accion == "verificar" else "reabrir_turno"
    assert_scope(user, plan.planta, plan.area_id, permission)
    reg = RegistroProductividadTurno.objects.select_for_update().get(programacion=plan)
    if reg.version != version:
        raise ValidationError("Otro usuario modificó el registro. Recargue la página.")
    before = snapshot(reg)
    if accion == "verificar":
        if reg.estado != "CERRADO":
            raise ValidationError("Solo puede verificar un turno cerrado.")
        reg.estado, reg.verificado_por, reg.verificado = "VERIFICADO", user, timezone.now()
    elif accion == "reabrir":
        if reg.estado not in ("CERRADO", "VERIFICADO") or not motivo.strip():
            raise ValidationError("Para reabrir un cierre debe indicar un motivo.")
        reg.estado = "BORRADOR"
        reg.cerrado = reg.verificado = None
        reg.cerrado_por = reg.verificado_por = None
    else:
        raise ValidationError("Acción desconocida.")
    reg.version += 1
    reg.full_clean()
    reg.save()
    audit(plan, user, accion.upper(), before, snapshot(reg), motivo)
    return reg
