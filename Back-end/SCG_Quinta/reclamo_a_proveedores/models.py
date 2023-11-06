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
    archivo_foto = models.FileField(upload_to='fotos_reclamos/') # Define la ruta donde se guardarán las fotos
    verificado = models.BooleanField(default=False)
    verificado_por = models.CharField(max_length=50 ,null=True, blank=True)
    fecha_de_verificacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre

