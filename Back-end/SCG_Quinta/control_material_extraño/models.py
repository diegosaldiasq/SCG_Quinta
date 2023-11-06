from django.db import models

# Create your models here.

class DatosFormularioControlMaterialExtraño(models.Model):
    nombre_tecnologo = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField()
    turno = models.TextField()
    area_material = models.TextField()
    tipo_material = models.TextField()
    accion_correctiva = models.IntegerField()
    verificacion_accion_correctiva = models.TextField()
    observaciones = models.TextField()
    verificado = models.BooleanField(default=False)
    verificado_por = models.CharField(max_length=50 ,null=True, blank=True)
    fecha_de_verificacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre