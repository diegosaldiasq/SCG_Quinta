from django.db import models

# Create your models here.


class DatosFormularioTemperaturaDespachoSisa(models.Model):
    nombre_tecnologo = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField()
    cadena = models.TextField()
    item = models.TextField()
    producto = models.TextField()
    congelado_refrigerado = models.TextField()
    temperatura_producto = models.FloatField()
    revision_etiquetado = models.TextField()
    lote = models.TextField()
    fecha_vencimiento = models.DateTimeField()
    accion_correctiva = models.IntegerField()
    verificacion_accion_correctiva = models.FloatField()
    verificado = models.BooleanField(default=False)
    verificado_por = models.CharField(max_length=50 ,null=True, blank=True)
    fecha_de_verificacion = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.nombre