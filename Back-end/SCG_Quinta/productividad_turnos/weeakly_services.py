"""Programación de una semana ISO utilizando los turnos y auditoría existentes."""
from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.db import transaction

from .models import ProgramacionTurno, RegistroProductividadTurno
from .permissions import assert_scope
from .selectors import registro_of
from .services import programar


DIAS = ("Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo")
PARES = tuple((dia, turno) for dia in range(1, 8) for turno in "ABC")


def lunes_iso(anio, semana):
    try:
        return date.fromisocalendar(int(anio), int(semana), 1)
    except (TypeError, ValueError):
        raise ValidationError("La semana no existe en el año ISO indicado.")


def cargar_semana(user, anio, semana, planta, area, origen=None):
    """Solo lectura. Copiar prepara valores en pantalla y no guarda producción."""
    assert_scope(user, planta, area.pk, "programar_turno")
    start = lunes_iso(anio, semana)
    plans = list(ProgramacionTurno.objects.filter(
        planta=planta, area=area, fecha_operativa__range=(start, start + timedelta(days=6))
    ).select_related("registro"))
    existing = {(p.fecha_operativa.isoweekday(), p.turno): p for p in plans}
    sources = {}
    if origen:
        source_start = lunes_iso(*origen)
        if source_start == start:
            raise ValidationError("Seleccione otra semana como origen de la copia.")
        source_plans = list(ProgramacionTurno.objects.filter(
            planta=planta, area=area,
            fecha_operativa__range=(source_start, source_start + timedelta(days=6))
        ))
        if not source_plans:
            raise ValidationError("La semana de origen no tiene programación en esta planta y área.")
        sources = {(p.fecha_operativa.isoweekday(), p.turno): p for p in source_plans}
    result = []
    for dia, turno in PARES:
        target = existing.get((dia, turno))
        record = registro_of(target) if target else None
        locked = bool(record and record.estado in ("CERRADO", "VERIFICADO"))
        # Un cierre de destino nunca se modifica al copiar otra semana.
        value = target if locked or not origen else sources.get((dia, turno))
        result.append({
            "dia": dia, "turno": turno,
            "programacion_id": target.pk if target else 0,
            "version": target.version if target else 0,
            "registro_version": record.version if record else 0,
            "programado": value.programado if value else False,
            "meta_pt": value.meta_pt if value and value.programado else None,
            "extraordinario": value.extraordinario if value and value.programado else False,
            "_locked": locked,
            "_estado": record.get_estado_display() if record else ("Programado" if target and target.programado else "Sin programar"),
        })
    return start, result


@transaction.atomic
def guardar_semana(user, anio, semana, planta, area, filas, motivo):
    """Aplica las 21 celdas en una transacción, sin tocar cantidades de producción."""
    assert_scope(user, planta, area.pk, "programar_turno")
    if not area.activo:
        raise ValidationError("El área está inactiva.")
    if not motivo or not motivo.strip():
        raise ValidationError("Indique el motivo de la programación o del ajuste semanal.")
    if len(filas) != len(PARES) or [(r.get("dia"), r.get("turno")) for r in filas] != list(PARES):
        raise ValidationError("La cuadrícula debe contener los siete días y los tres turnos, sin duplicados.")
    start = lunes_iso(anio, semana)
    # No utilizar select_related sobre la relación nullable registro al bloquear en PostgreSQL.
    plans = list(ProgramacionTurno.objects.select_for_update().filter(
        planta=planta, area=area, fecha_operativa__range=(start, start + timedelta(days=6))
    ).order_by("fecha_operativa", "turno"))
    records = {r.programacion_id: r for r in RegistroProductividadTurno.objects.select_for_update().filter(programacion__in=plans)}
    existing = {(p.fecha_operativa.isoweekday(), p.turno): p for p in plans}
    prepared = []
    for row in filas:
        pair = (row["dia"], row["turno"])
        p = existing.get(pair)
        r = records.get(p.pk) if p else None
        if row.get("programacion_id") != (p.pk if p else 0) or row.get("version") != (p.version if p else 0) or row.get("registro_version") != (r.version if r else 0):
            raise ValidationError("La semana o uno de sus registros cambió mientras editaba. Recargue la semana antes de guardar.")
        active = bool(row["programado"])
        meta = row.get("meta_pt") if active else 0
        extraordinary = bool(row.get("extraordinario")) if active else False
        if meta is None or not isinstance(meta, int) or isinstance(meta, bool) or meta < 0 or meta > 2147483647:
            raise ValidationError("Cada turno programado necesita una meta PT entera no negativa.")
        changed = not p or (p.programado, p.meta_pt, p.extraordinario) != (active, meta, extraordinary)
        if r and r.estado in ("CERRADO", "VERIFICADO") and changed:
            raise ValidationError("No puede modificar turnos cerrados o verificados. Reábralos con autorización antes de cambiar su programación.")
        data = {
            "fecha_operativa": start + timedelta(days=row["dia"] - 1), "planta": planta,
            "area": area, "turno": row["turno"], "meta_pt": meta,
            "programado": active, "extraordinario": extraordinary,
            "motivo": "Semana {0}-W{1:02d}: {2}".format(anio, semana, motivo.strip()),
        }
        prepared.append((p, data, changed))
    count = 0
    for p, data, changed in prepared:
        if changed:
            programar(user, data, pk=p.pk if p else None, version=p.version if p else None)
            count += 1
    return count