from django.db import models

# Create your models here.


class DatosFormularioHigieneConductaPersonal(models.Model):
    fecha_ingreso = models.DateTimeField()
    nombre_personal = models.CharField(max_length=100)
    turno = models.TextField()
    planta = models.TextField()
    area = models.TextField()
    cumplimiento = models.TextField()
    desviacion = models.TextField()
    accion_correctiva = models.TextField()
    verificacion_accion_correctiva = models.TextField()
    observacion = models.TextField()
    nombre_tecnologo = models.CharField(max_length=100)
    verificado = models.BooleanField(default=False)
    verificado_por = models.CharField(max_length=50 ,null=True, blank=True)
    fecha_de_verificacion = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.nombre