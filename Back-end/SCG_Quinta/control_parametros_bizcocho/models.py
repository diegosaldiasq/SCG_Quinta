from django.db import models

# Create your models here.


class DatosFormularioControlParametrosBizcocho(models.Model):
    nombre_tecnologo = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField()
    proveedor = models.TextField()
    producto = models.TextField()
    cantidad_agua = models.FloatField()
    cantidad_huevo = models.FloatField()
    velocidad_bomba = models.IntegerField()
    velocidad_turbo = models.IntegerField()
    contrapresion = models.FloatField()
    contrapresion_trasera = models.FloatField()
    inyeccion_de_aire = models.IntegerField()
    densidad = models.FloatField()
    t_final = models.FloatField()
    lote = models.CharField()
    turno = models.CharField()
    verificado = models.BooleanField(default=False)
    verificado_por = models.CharField(max_length=50 ,null=True, blank=True)
    fecha_de_verificacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre_tecnologo + " " + str(self.fecha_registro)
