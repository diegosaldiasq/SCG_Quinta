from django.db import models

# Create your models here.

class TurnoOEE(models.Model):
    fecha = models.DateTimeField(unique=True, null=False, blank=False)
    cliente = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, null=True, blank=True) 
    producto = models.CharField(max_length=100)
    linea = models.CharField(max_length=50)
    turno = models.CharField(max_length=20)
    lote = models.CharField(max_length=50, null=False, blank=False)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    tiempo_planeado = models.PositiveIntegerField(help_text="En minutos")
    produccion_planeada = models.PositiveIntegerField(help_text="Producción planeada en unidades")
    produccion_real = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.fecha} - {self.linea} - {self.turno}"

class Detencion(models.Model):
    lote = models.ForeignKey(TurnoOEE, on_delete=models.CASCADE, related_name='detenciones')
    linea = models.ForeignKey(TurnoOEE, on_delete=models.CASCADE, related_name='detenciones_linea')
    motivo = models.CharField(max_length=100)
    duracion = models.PositiveIntegerField(help_text="Duración en minutos")

class Reproceso(models.Model):
    lote = models.ForeignKey(TurnoOEE, on_delete=models.CASCADE, related_name='reprocesos')
    linea = models.ForeignKey(TurnoOEE, on_delete=models.CASCADE, related_name='reprocesos_linea')
    motivo = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()