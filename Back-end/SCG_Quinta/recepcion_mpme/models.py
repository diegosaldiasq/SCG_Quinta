from django.db import models

# Create your models here.

class DatosFormularioRecepcionMpMe(models.Model):
    nombre_tecnologo = models.CharField(max_length=100)
    lote_dia = models.TextField()
    fecha_registro = models.DateTimeField()
    nombre_proveedor = models.TextField()
    nombre_producto = models.TextField()
    fecha_elaboracion = models.DateTimeField()
    fecha_vencimiento = models.DateTimeField()
    lote_producto = models.TextField()
    numero_factura = models.TextField()
    higiene = models.TextField()
    rs = models.TextField()
    temperatura_transporte = models.TextField()
    apariencia = models.TextField()
    textura = models.TextField()
    ausencia_material_extraño = models.TextField()
    temperatura_producto = models.TextField()
    condicion_envase = models.TextField()
    color = models.TextField()
    olor = models.TextField()
    sabor = models.TextField()
    grados_brix = models.TextField()

    def __str__(self):
        return self.nombre