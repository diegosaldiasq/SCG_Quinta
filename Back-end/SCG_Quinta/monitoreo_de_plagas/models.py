from django.db import models

# Create your models here.

class DatosFormularioMonitoreoDePlagas(models.Model):
    nombre_tecnologo = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField()
    numero_estacion = models.IntegerField()
    tipo_plaga = models.TextField()
    tipo_trampa = models.TextField()
    ubicacion = models.TextField()
    monitoreo = models.TextField()
    accion_correctiva = models.IntegerField()

    def __str__(self):
        return self.nombre