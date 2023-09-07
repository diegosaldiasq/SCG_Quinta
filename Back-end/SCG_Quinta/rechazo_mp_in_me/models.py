from django.db import models

# Create your models here.

class DatosFormularioRechazoMpInMe(models.Model):
    nombre_tecnologo = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField()
    nombre_proveedor = models.TextField()
    numero_factura = models.IntegerField()
    nombre_transportista = models.TextField()
    nombre_producto = models.TextField()
    fecha_elaboracion = models.DateTimeField()
    lote = models.TextField()
    fecha_vencimiento = models.DateTimeField()
    motivo_rechazo = models.TextField()
    cantidad_producto_involucrado = models.FloatField()
    unidad_de_medida = models.TextField()
    clasificacion = models.TextField()


    def __str__(self):
        return self.nombre
