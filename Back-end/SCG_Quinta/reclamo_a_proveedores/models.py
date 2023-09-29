from django.db import models

# Create your models here.

class DatosFormularioReclamoProveedores(models.Model):
    nombre_tecnologo = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField()
    nombre_proveedor = models.TextField()
    fecha_reclamo = models.DateTimeField()
    nombre_del_producto = models.TextField()
    fecha_elaboracion = models.DateTimeField()
    lote = models.TextField()
    fecha_vencimiento = models.DateTimeField()
    no_conformidad = models.TextField()
    clasificacion = models.TextField()
    cantidad_involucrada = models.FloatField()
    unidad_de_medida = models.TextField()
    archivo_foto = models.FileField()

    def __str__(self):
        return self.nombre

