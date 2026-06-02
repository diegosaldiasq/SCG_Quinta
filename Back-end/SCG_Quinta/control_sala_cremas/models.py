from django.db import models
from django.utils import timezone
from control_de_pesos.models import ProductoControlPeso


class ProductoSalaCremas(models.Model):
    cliente = models.CharField(max_length=150)
    producto = models.CharField(max_length=150)
    codigo = models.CharField(max_length=80)

    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["cliente", "producto"]
        unique_together = ("cliente", "producto", "codigo")

    def __str__(self):
        return f"{self.cliente} - {self.producto} - {self.codigo}"


class RegistroSalaCremas(models.Model):
    TURNOS = [
        ("Turno A", "Turno A"),
        ("Turno B", "Turno B"),
        ("Turno C", "Turno C"),
    ]
    TIPOS_CREMA = [
        ("Crema batida vegetal", "Crema batida vegetal"),
        ("Crema batida lactea", "Crema batida lactea"),
        ("Crema batida saborisada", "Crema batida saborisada"),
        ("Crema pastelera", "Crema pastelera"),
        ("Merengue", "Merengue"),
        ("Manjar", "Manjar"),
        ("Mousse", "Mousse"),
    ]

    APLICACIONES = [
        ("Pegado", "Pegado"),
        ("Rebosado", "Rebosado"),
        ("Ambas", "Ambas"),
    ]

    producto_control_peso = models.ForeignKey(
        ProductoControlPeso,
        on_delete=models.PROTECT,
        related_name='registros_sala_cremas',
        verbose_name='Producto',
        null=True,
        blank=True
    )

    usuario = models.CharField(max_length=150)
    fecha_hora = models.DateTimeField(default=timezone.now)

    turno = models.CharField(max_length=20, choices=TURNOS)
    cliente = models.CharField(max_length=150)
    producto = models.CharField(max_length=150)
    codigo = models.CharField(max_length=80)
    lote = models.CharField(max_length=100)

    tipo_crema = models.CharField(max_length=50, choices=TIPOS_CREMA)
    aplicacion = models.CharField(max_length=20, choices=APLICACIONES)

    densidad = models.DecimalField(max_digits=8, decimal_places=3)
    temperatura = models.DecimalField(max_digits=8, decimal_places=2)
    numero_batidora = models.CharField(max_length=50)

    observaciones = models.TextField(blank=True, null=True)

    verificado = models.BooleanField(default=False)
    fecha_verificacion = models.DateTimeField(blank=True, null=True)
    verificado_por = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        ordering = ["-fecha_hora"]

    def __str__(self):
        return f"{self.producto} - Lote {self.lote}"
    
    def save(self, *args, **kwargs):

        if self.producto_control_peso:
            self.cliente = self.producto_control_peso.cliente
            self.producto = self.producto_control_peso.producto
            self.codigo = self.producto_control_peso.codigo

        super().save(*args, **kwargs)