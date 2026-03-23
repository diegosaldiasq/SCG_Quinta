from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.nombre


class Local(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=300)
    comuna = models.CharField(max_length=100, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    latitud = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitud = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    direccion_formateada = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Local'
        verbose_name_plural = 'Locales'
        unique_together = ('nombre', 'direccion')

    def __str__(self):
        return f"{self.nombre} - {self.direccion}"


class CargaVentas(models.Model):
    archivo = models.FileField(upload_to='ventas_geo/')
    fecha_carga = models.DateTimeField(auto_now_add=True)
    observacion = models.TextField(blank=True, null=True)
    procesado = models.BooleanField(default=False)
    filas_leidas = models.PositiveIntegerField(default=0)
    filas_ok = models.PositiveIntegerField(default=0)
    filas_error = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-fecha_carga']
        verbose_name = 'Carga de ventas'
        verbose_name_plural = 'Cargas de ventas'

    def __str__(self):
        return f"Carga #{self.id} - {self.fecha_carga:%Y-%m-%d %H:%M}"


class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='ventas')
    local = models.ForeignKey(Local, on_delete=models.CASCADE, related_name='ventas')
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateField()
    carga = models.ForeignKey(CargaVentas, on_delete=models.SET_NULL, blank=True, null=True, related_name='ventas')
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha', 'producto__nombre']
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'

    def __str__(self):
        return f"{self.producto} | {self.local} | {self.cantidad}"
    

class ErrorCargaVenta(models.Model):
    carga = models.ForeignKey(CargaVentas, on_delete=models.CASCADE, related_name='errores')
    fila_excel = models.PositiveIntegerField()
    mensaje = models.TextField()
    datos_fila = models.TextField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['fila_excel']
        verbose_name = 'Error de carga'
        verbose_name_plural = 'Errores de carga'

    def __str__(self):
        return f"Fila {self.fila_excel} - {self.mensaje}"