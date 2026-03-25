from django.db import models
from django.utils import timezone


class Cliente(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="productos")
    nombre = models.CharField(max_length=150)
    codigo = models.CharField(max_length=50)

    codigo_registro = models.CharField(max_length=100, blank=True, null=True)
    version = models.CharField(max_length=50, blank=True, null=True)
    fecha_modificacion = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["cliente__nombre", "nombre"]
        unique_together = ("cliente", "nombre")

    def __str__(self):
        return f"{self.cliente.nombre} - {self.nombre}"


class Ingrediente(models.Model):
    nombre = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name = "Ingrediente"
        verbose_name_plural = "Ingredientes"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class ProductoIngrediente(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="producto_ingredientes")
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE, related_name="ingrediente_productos")
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, null=True, blank=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Ingrediente por producto"
        verbose_name_plural = "Ingredientes por producto"
        ordering = ["producto", "orden", "ingrediente__nombre"]
        unique_together = ("producto", "ingrediente")

    def __str__(self):
        return f"{self.producto.nombre} - {self.ingrediente.nombre}"


class RegistroTrazabilidad(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    codigo_producto = models.CharField(max_length=50)

    lote_producto = models.CharField(max_length=100, blank=True, null=True)
    fecha_elaboracion_producto = models.DateField(blank=True, null=True)
    turno = models.CharField(max_length=50, blank=True, null=True)
    linea = models.CharField(max_length=100, blank=True, null=True)

    fecha_registro = models.DateTimeField(default=timezone.now)
    elaborado_por = models.CharField(max_length=150, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Registro de trazabilidad"
        verbose_name_plural = "Registros de trazabilidad"
        ordering = ["-fecha_registro"]

    def __str__(self):
        fecha = self.fecha_registro.strftime("%d-%m-%Y %H:%M")
        return f"{self.producto.nombre} - {fecha}"
    
    verificado = models.BooleanField(default=False, verbose_name="Verificado")
    fecha_verificacion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de verificación"
    )
    nombre_verificador = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name="Nombre verificador"
    )

    def __str__(self):
        return f"{self.producto} - {self.lote_producto}"


class DetalleTrazabilidadIngrediente(models.Model):
    registro = models.ForeignKey(
        RegistroTrazabilidad,
        on_delete=models.CASCADE,
        related_name="detalles"
    )
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.PROTECT)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    lote = models.CharField(max_length=100)
    fecha_elaboracion = models.DateField()
    fecha_vencimiento = models.DateField()
    accion_correctiva = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Detalle trazabilidad ingrediente"
        verbose_name_plural = "Detalles trazabilidad ingredientes"
        ordering = ["ingrediente__nombre"]

    def __str__(self):
        return f"{self.registro} - {self.ingrediente.nombre}"
