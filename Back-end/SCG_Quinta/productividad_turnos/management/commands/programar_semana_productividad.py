from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from productividad_turnos.models import AreaProductividad, PLANTAS
from productividad_turnos.services import programar


class Command(BaseCommand):
    help = "Genera programación de una semana ISO. Atómico: si un turno ya existe, no cambia ninguno."

    def add_arguments(self, parser):
        parser.add_argument("--usuario-id", type=int, required=True)
        parser.add_argument("--planta", required=True, choices=[x[0] for x in PLANTAS])
        parser.add_argument("--area", default="TORTAS")
        parser.add_argument("--anio", type=int, required=True)
        parser.add_argument("--semana", type=int, required=True)
        parser.add_argument("--dias", type=int, nargs="+", choices=range(1, 8), default=[1, 2, 3, 4, 5])
        parser.add_argument("--turnos", nargs="+", choices=list("ABC"), default=list("ABC"))
        for t in "abc":
            parser.add_argument(f"--meta-{t}", type=int)
        parser.add_argument("--motivo", default="Programación semanal")

    @transaction.atomic
    def handle(self, *args, **opts):
        try:
            monday = date.fromisocalendar(opts["anio"], opts["semana"], 1)
            user = get_user_model().objects.get(pk=opts["usuario_id"])
            area = AreaProductividad.objects.get(codigo=opts["area"])
            for t in opts["turnos"]:
                if opts[f"meta_{t.lower()}"] is None or opts[f"meta_{t.lower()}"] < 0:
                    raise CommandError(f"Indique --meta-{t.lower()} con un valor no negativo.")
            count = 0
            for day in sorted(set(opts["dias"])):
                for turn in sorted(set(opts["turnos"])):
                    programar(user, {"fecha_operativa": monday + timedelta(days=day - 1), "planta": opts["planta"], "area": area, "turno": turn, "meta_pt": opts[f"meta_{turn.lower()}"], "programado": True, "extraordinario": day == 7, "motivo": opts["motivo"]})
                    count += 1
        except (ValueError, ValidationError, PermissionDenied, get_user_model().DoesNotExist, AreaProductividad.DoesNotExist) as exc:
            raise CommandError(str(exc)) from exc
        self.stdout.write(self.style.SUCCESS(f"Creadas {count} programaciones. No se crearon cierres de producción."))