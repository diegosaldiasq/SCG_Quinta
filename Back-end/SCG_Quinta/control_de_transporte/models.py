from django.db import models

# Create your models here.

class DatosFormularioControlDeTransporte(models.Model):
    nombre_tecnologo = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField()
    fecha_recepcion = models.DateTimeField()
    producto_recepcion = models.TextField()
    temperatura_transporte = models.FloatField()
    temperatura_producto = models.FloatField()
    lote = models.TextField()
    fecha_vencimiento = models.DateTimeField()
    accion_correctiva = models.IntegerField()
    verificacion_accion_correctiva = models.TextField()
    verificado = models.BooleanField(default=False)
    verificado_por = models.CharField(max_length=50 ,null=True, blank=True)
    fecha_de_verificacion = models.DateTimeField(null=True, blank=True)

    
    def __str__(self):
        return self.nombre_tecnologo + " " + str(self.fecha_registro)