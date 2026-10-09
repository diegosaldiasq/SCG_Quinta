from django.core.management.base import BaseCommand
from calculo_oee.models import TurnoOEE
from calculo_oee.services import calcular_oee_automatico


class Command(BaseCommand):
    help = 'Calcula los turnos pendientes válidos y reporta los que requieren revisión.'

    def handle(self, *args, **options):
        calculados = revision = 0
        ids = TurnoOEE.objects.filter(
            produccion_real__isnull=False, resumenes_turno__isnull=True,
        ).values_list('pk', flat=True)
        for lote_id in ids.iterator():
            resumen, motivos = calcular_oee_automatico(lote_id)
            if resumen:
                calculados += 1
            else:
                revision += 1
                self.stdout.write(f'Turno {lote_id}: ' + '; '.join(motivos))
        self.stdout.write(self.style.SUCCESS(
            f'{calculados} calculados; {revision} requieren revisión.'
        ))