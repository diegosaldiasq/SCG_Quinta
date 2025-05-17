from django.db import models

# Create your models here.

class DatosFormularioControlDePesos(models.Model):
    nombre_tecnologo = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField()
    cliente = models.TextField()
    producto = models.TextField()
    peso_receta = models.FloatField()
    peso_real = models.FloatField()
    lote = models.TextField()
    turno = models.TextField()
    verificado = models.BooleanField(default=False)
    verificado_por = models.CharField(max_length=50 ,null=True, blank=True)
    fecha_de_verificacion = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.nombre_tecnologo + " " + str(self.fecha_registro)
