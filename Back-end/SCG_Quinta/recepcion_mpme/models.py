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
    numero_factura = models.IntegerField()
    higiene = models.TextField()
    rs = models.TextField()
    temperatura_transporte = models.FloatField(blank=True)
    apariencia = models.TextField()
    textura = models.TextField()
    ausencia_material_extraño = models.TextField()
    temperatura_producto = models.FloatField(blank=True)
    condicion_envase = models.TextField()
    color = models.TextField()
    olor = models.TextField()
    sabor = models.TextField()
    grados_brix = models.FloatField(blank=True)
    verificado = models.BooleanField(default=False)
    verificado_por = models.CharField(max_length=50 ,null=True, blank=True)
    fecha_de_verificacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nombre