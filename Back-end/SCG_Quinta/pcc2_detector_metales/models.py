from django.db import models

# Create your models here.

class DatosFormularioPcc2DetectorMetales(models.Model):
    nombre_tecnologo = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField()
    lote = models.IntegerField()
    turno = models.TextField()
    tipo_metal = models.TextField()
    medicion = models.TextField()
    producto = models.TextField()
    observaciones = models.TextField()
    accion_correctiva = models.IntegerField()

    def __str__(self):
        return self.nombre
