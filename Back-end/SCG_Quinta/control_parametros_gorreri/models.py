from django.db import models

# Create your models here.

class DatosFormularioControlParametrosGorreri(models.Model):
    nombre_tecnologo = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField()
    cliente = models.CharField(max_length=100)
    codigo_producto = models.CharField(max_length=50)
    producto = models.CharField(max_length=100)
    numero_tm = models.IntegerField()
    velocidad_bomba = models.IntegerField()
    velocidad_turbo = models.IntegerField()
    contrapresion = models.FloatField()
    inyeccion_de_aire = models.IntegerField()
    densidad = models.FloatField()
    t_final = models.FloatField()
    lote = models.CharField()
    turno = models.CharField()
    verificado = models.BooleanField(default=False)
    verificado_por = models.CharField(max_length=50 ,null=True, blank=True)
    fecha_de_verificacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.producto} - {self.numero_tm} - {self.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')}"