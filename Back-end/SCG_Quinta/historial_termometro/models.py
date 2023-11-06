from django.db import models

# Create your models here.

class DatosFormularioHistorialTermometro(models.Model):
    nombre_tecnologo = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField()
    codigo_termometro = models.TextField()
    valor_1 = models.FloatField()
    valor_2 = models.FloatField()
    valor_3 = models.FloatField()
    valor_4 = models.FloatField()
    valor_5 = models.FloatField()
    promedio_prueba = models.FloatField()
    valor_6 = models.FloatField()
    valor_7 = models.FloatField()
    valor_8 = models.FloatField()
    valor_9 = models.FloatField()
    valor_10 = models.FloatField()
    promedio_patron = models.FloatField()
    factor_anual = models.FloatField()
    promedio_termometros = models.FloatField()
    nivel_aceptacion = models.FloatField()
    cumplimiento = models.TextField()
    accion_correctiva = models.TextField()
    verificacion_accion_correctiva = models.TextField()
    verificado = models.BooleanField(default=False)
    verificado_por = models.CharField(max_length=50 ,null=True, blank=True)
    fecha_de_verificacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre