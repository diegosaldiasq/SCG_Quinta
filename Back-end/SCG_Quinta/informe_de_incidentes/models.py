from django.db import models

# Create your models here.

class DatosFormularioInformeDeIncidentes(models.Model):
    nombre_tecnologo = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField()
    fuente_material = models.TextField()
    cantidad_contaminada = models.TextField()
    unidad_de_medida = models.TextField()
    lote_producto_contaminado = models.TextField()
    observaciones = models.TextField()
    analisis_causa = models.TextField()
    accion_correctiva = models.TextField()

    def __str__(self):
        return self.nombre