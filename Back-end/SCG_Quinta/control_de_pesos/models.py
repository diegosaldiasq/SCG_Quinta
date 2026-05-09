from django.db import models

# Create your models here.

class DatosFormularioControlDePesos(models.Model):
    nombre_tecnologo = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField(unique=True, null=False, blank=False)
    cliente = models.TextField()
    codigo_producto = models.CharField(max_length=20, null=True, blank=True)
    producto = models.TextField()
    peso_receta = models.IntegerField()
    peso_real = models.IntegerField()
    altura = models.IntegerField(null=True, blank=True, help_text="Altura en mm")
    lote = models.TextField(null=False, blank=False)
    turno = models.TextField(null=False, blank=False)
    verificado = models.BooleanField(default=False)
    verificado_por = models.CharField(max_length=50, null=True, blank=True)
    fecha_de_verificacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre_tecnologo} {self.fecha_registro}"
    
class ProductoControlPeso(models.Model):
    AREA_CHOICES = [
        ("TORTAS", "Tortas"),
        ("PRELISTOS", "Prelistos"),
        ("INSUMOS_KUCHEN", "Insumos Kuchen"),
    ]
    CLIENTE_CHOICES = [
        ("Jumbo", "Jumbo"),
        ("SISA", "SISA"),
        ("Walmart", "Walmart"),
        ("Unimarc", "Unimarc"),
        ("Insumo", "Insumo"),
        ("SUB", "SUB"),
        ("Pasteles", "Pasteles"),
        ("Prelisto pasteles", "Prelisto pasteles"),
    ]

    area = models.CharField(max_length=30, choices=AREA_CHOICES, default="TORTAS")
    cliente = models.CharField(max_length=100, choices=CLIENTE_CHOICES)
    codigo = models.CharField(max_length=30)
    producto = models.CharField(max_length=200)
    peso_receta = models.IntegerField()
    porcentaje_perdida = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    altura = models.IntegerField(null=True, blank=True)
    un_pp = models.DecimalField("Unidades por persona", max_digits=10, decimal_places=2, null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["area", "cliente", "producto"]
        unique_together = ("area", "cliente", "codigo", "producto")

    def __str__(self):
        return f"{self.area} - {self.cliente} - {self.codigo} - {self.producto}"
