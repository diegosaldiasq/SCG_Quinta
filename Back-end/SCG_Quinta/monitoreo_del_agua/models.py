from django.db import models

# Create your models here.

class DatosFormularioMonitoreoDelAgua(models.Model):
    nombre_tecnologo = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField()
    turno_ = models.TextField()
    planta_ = models.TextField()
    numero_llave = models.IntegerField()
    punto_muestreo = models.TextField()
    sabor_insipido = models.TextField()
    olor_inodora = models.TextField()
    color_incoloro = models.TextField()
    ph_ = models.FloatField()
    cloro_libre = models.FloatField()
    accion_correctiva = models.TextField()
    resultado_ac = models.IntegerField()

    def __str__(self):
        return self.nombre