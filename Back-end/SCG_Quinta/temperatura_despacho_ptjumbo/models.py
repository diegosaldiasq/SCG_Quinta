from django.db import models

# Create your models here.


class DatosFormularioTemperaturaDespachoJumbo(models.Model):
    nombre_tecnologo = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField()
    cadena = models.TextField()
    item = models.TextField()
    producto = models.TextField()
    temperatura_producto = models.FloatField()
    revision_etiquetado = models.TextField()
    lote = models.TextField()
    fecha_vencimiento = models.DateTimeField()
    accion_correctiva = models.IntegerField()
    verificacion_accion_correctiva = models.FloatField()
    
    def __str__(self):
        return self.nombre