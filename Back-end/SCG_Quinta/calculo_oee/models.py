from django.db import models

# Create your models here.

class TurnoOEE(models.Model):
    fecha = models.DateField()
    linea = models.CharField(max_length=50)
    turno = models.CharField(max_length=20)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    tiempo_planeado = models.PositiveIntegerField(help_text="En minutos")
    produccion_real = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.fecha} - {self.linea} - {self.turno}"

class Detencion(models.Model):
    turno = models.ForeignKey(TurnoOEE, on_delete=models.CASCADE, related_name='detenciones')
    motivo = models.CharField(max_length=100)
    duracion = models.PositiveIntegerField(help_text="Duración en minutos")

class Reproceso(models.Model):
    turno = models.ForeignKey(TurnoOEE, on_delete=models.CASCADE, related_name='reprocesos')
    motivo = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()