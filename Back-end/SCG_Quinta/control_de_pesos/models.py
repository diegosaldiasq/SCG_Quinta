from django.db import models

# Create your models here.

class DatosFormularioControlDePesos(models.Model):
    nombre_tecnologo = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField()
    cliente = models.TextField()
    codigo_producto = models.CharField(max_length=20, null=True, blank=True)
    producto = models.TextField()
    peso_receta = models.IntegerField()
    peso_real = models.IntegerField()
    lote = models.TextField(null=False, blank=False)
    turno = models.TextField(null=False, blank=False)
    verificado = models.BooleanField(default=False)
    verificado_por = models.CharField(max_length=50 ,null=True, blank=True)
    fecha_de_verificacion = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.nombre_tecnologo + " " + str(self.fecha_registro)
