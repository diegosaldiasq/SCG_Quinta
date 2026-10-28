from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from productividad_turnos.models import AreaProductividad, AsignacionProductividad, PLANTAS


BASE = ["view_registroproductividadturno"]
ROLES = {
    "Consulta": BASE,
    "Supervisor": BASE + ["registrar_turno", "cerrar_turno"],
    "Verificador": BASE + ["registrar_turno", "cerrar_turno", "verificar_turno", "reabrir_turno"],
    "Planificacion": BASE + ["programar_turno"],
}


class Command(BaseCommand):
    help = "Crea grupos de productividad y, opcionalmente, asigna un usuario existente a un grupo y alcance."

    def add_arguments(self, parser):
        parser.add_argument("--usuario-id", type=int)
        parser.add_argument("--grupo", choices=list(ROLES))
        parser.add_argument("--planta", choices=[x[0] for x in PLANTAS])
        parser.add_argument("--area", default="TORTAS")

    @transaction.atomic
    def handle(self, *args, **options):
        for role, codes in ROLES.items():
            group, _ = Group.objects.get_or_create(name=f"Productividad - {role}")
            permissions = Permission.objects.filter(content_type__app_label="productividad_turnos", codename__in=codes)
            if permissions.count() != len(codes):
                raise CommandError("Faltan permisos. Ejecute migrate antes de configurar los grupos.")
            group.permissions.add(*permissions)
        if options["usuario_id"]:
            if not options["grupo"] or not options["planta"]:
                raise CommandError("Con --usuario-id indique también --grupo y --planta.")
            try:
                user = get_user_model().objects.get(pk=options["usuario_id"])
                area = AreaProductividad.objects.get(codigo=options["area"])
            except (get_user_model().DoesNotExist, AreaProductividad.DoesNotExist) as exc:
                raise CommandError("El usuario o el área no existen.") from exc
            user.groups.add(Group.objects.get(name=f'Productividad - {options["grupo"]}'))
            AsignacionProductividad.objects.get_or_create(usuario=user, planta=options["planta"], area=area)
            self.stdout.write(self.style.SUCCESS(f"Asignado usuario {user.pk} a {options['grupo']}, {options['planta']}, {area.codigo}."))
        self.stdout.write(self.style.SUCCESS("Grupos configurados. No se modificaron grupos ajenos ni se crearon usuarios."))