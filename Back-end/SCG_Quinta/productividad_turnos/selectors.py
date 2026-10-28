from datetime import date, timedelta
from decimal import Decimal

from django.conf import settings
from django.utils import timezone

from .models import RegistroProductividadTurno
from .permissions import scoped_programs


OFICIALES = ("CERRADO", "VERIFICADO")


def registro_of(plan):
    try:
        return plan.registro
    except RegistroProductividadTurno.DoesNotExist:
        return None


def ratio(numerator, denominator, factor=1):
    return Decimal(numerator) / Decimal(denominator) * factor if denominator else None


def metrics(registros):
    rows = list(registros)
    present = bool(rows)
    pt = sum(r.terminadas for r in rows) if present else None
    meta = sum(r.meta_pt_cierre for r in rows) if present else None
    semi = sum(r.semielaborados for r in rows) if present and all(r.semielaborados is not None for r in rows) else None
    dot = sum(r.dotacion for r in rows) if present and all(r.dotacion and r.dotacion > 0 for r in rows) else None
    hh = sum((r.horas_persona for r in rows), Decimal(0)) if present and all(r.horas_persona and r.horas_persona > 0 for r in rows) else None
    missing_meta = present and any(r.meta_pt_cierre == 0 and r.terminadas > 0 for r in rows)
    compliance = ratio(pt, meta, 100) if present and not missing_meta else None
    return {"cierres": len(rows), "terminadas": pt, "meta": meta, "semielaborados": semi, "personas_turno": dot, "horas_persona": hh, "cumplimiento": compliance, "up": ratio(pt, dot) if present else None, "uph": ratio(pt, hh) if present else None, "brecha": pt - meta if present else None, "metas_incompletas": bool(missing_meta)}


def estado_plan(plan, now=None):
    reg = registro_of(plan)
    if not plan.programado:
        return "No programado"
    if reg and reg.estado in OFICIALES:
        return reg.get_estado_display()
    if reg:
        return "Borrador"
    return "Pendiente" if plan.fin <= (now or timezone.now()) else "Aún no finaliza"


def programs_from_filter(user, data, periodo):
    if periodo == "semana":
        start = date.fromisocalendar(data["anio"], data["semana"], 1)
        end = start + timedelta(days=6)
    else:
        start = end = data["fecha"]
    qs = scoped_programs(user).filter(fecha_operativa__range=(start, end), area=data["area"], turno__in=data["turnos"])
    if data["planta"]:
        qs = qs.filter(planta=data["planta"])
    return qs, start, end


def summarize(plans, start, end, periodo, now=None):
    now = now or timezone.now()
    plans = list(plans)
    regs = [registro_of(p) for p in plans if p.programado and registro_of(p) and registro_of(p).estado in OFICIALES]
    total = metrics(regs)
    due = [p for p in plans if p.programado and p.fin <= now]
    received = [p for p in due if registro_of(p) and registro_of(p).estado in OFICIALES]
    tolerance = timedelta(minutes=getattr(settings, "PRODUCTIVIDAD_TOLERANCIA_MINUTOS", 60))
    timely = [p for p in received if registro_of(p).cerrado <= p.fin + tolerance]
    total_plan = sum(p.meta_pt for p in plans if p.programado)
    groups = []
    if periodo == "semana":
        for offset in range(7):
            day = start + timedelta(days=offset)
            subset = [p for p in plans if p.fecha_operativa == day]
            groups.append((day, subset))
    else:
        groups = [(f"Turno {t}", [p for p in plans if p.turno == t]) for t in "ABC" if any(p.turno == t for p in plans)]
    rows = []
    for label, subset in groups:
        rr = [registro_of(p) for p in subset if p.programado and registro_of(p) and registro_of(p).estado in OFICIALES]
        programmed = [p for p in subset if p.programado]
        statuses = [estado_plan(p, now) for p in subset]
        m = metrics(rr)
        rows.append({"label": label, "metrics": m, "recibidos": len(rr), "programados": len(programmed), "estado": ", ".join(dict.fromkeys(statuses)) or "No programado"})
    by_turn = []
    for turno in "ABC":
        rr = [r for r in regs if r.programacion.turno == turno]
        by_turn.append({"turno": turno, "metrics": metrics(rr)})
    # Escala común para gráficos HTML sin dependencias externas.
    scale = max([1] + [max(r["metrics"]["terminadas"] or 0, r["metrics"]["meta"] or 0) for r in rows])
    for row in rows:
        row["ancho_pt"] = float(Decimal(row["metrics"]["terminadas"] or 0) * 100 / scale)
        row["ancho_meta"] = float(Decimal(row["metrics"]["meta"] or 0) * 100 / scale)
    calendar = [{"plan": p, "registro": registro_of(p), "estado": estado_plan(p, now)} for p in plans]
    return {"total": total, "rows": rows, "por_turno": by_turn, "calendar": calendar, "desde": start, "hasta": end, "periodo": periodo, "vencidos": len(due), "recibidos": len(received), "pendientes": len(due)-len(received), "cobertura": ratio(len(received), len(due), 100), "oportunidad": ratio(len(timely), len(due), 100), "meta_programada": total_plan, "avance_plan": ratio(total["terminadas"], total_plan, 100) if regs else None, "actualizado": now}
