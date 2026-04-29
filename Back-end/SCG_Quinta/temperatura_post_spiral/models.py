from django.db import models
from django.utils import timezone

from control_sala_cremas.models import ProductoSalaCremas


class RegistroTemperaturaPostSpiral(models.Model):

    TURNO_CHOICES = [
        ('Turno A', 'Turno A'),
        ('Turno B', 'Turno B'),
        ('Turno C', 'Turno C'),
    ]

    producto_sala_cremas = models.ForeignKey(
        ProductoSalaCremas,
        on_delete=models.PROTECT,
        related_name='registros_temperatura_post_spiral',
        verbose_name='Producto'
    )

    usuario = models.CharField(max_length=150)
    fecha_hora = models.DateTimeField(default=timezone.now)

    turno = models.CharField(max_length=20, choices=TURNO_CHOICES)

    cliente = models.CharField(max_length=150, editable=False)
    producto = models.CharField(max_length=200, editable=False)
    codigo = models.CharField(max_length=80, editable=False)

    lote = models.CharField(max_length=100)

    tiempo_permanencia_producto = models.CharField(
        max_length=100,
        verbose_name='Tiempo permanencia producto'
    )

    temperatura = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name='Temperatura °C'
    )

    accion_correctiva = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    acciones_correctivas_requieren_revision = models.BooleanField(default=False)
    acciones_correctivas_verificadas = models.BooleanField(default=False)

    verificado = models.BooleanField(default=False)
    fecha_verificacion = models.DateTimeField(blank=True, null=True)
    nombre_verificador = models.CharField(max_length=150, blank=True, null=True)

    fecha_revision_accion_correctiva = models.DateTimeField(blank=True, null=True)
    nombre_revisor_accion_correctiva = models.CharField(max_length=150, blank=True, null=True)

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_hora']
        verbose_name = 'Registro temperatura post spiral'
        verbose_name_plural = 'Registros temperatura post spiral'

    def save(self, *args, **kwargs):
        if self.producto_sala_cremas:
            self.cliente = getattr(self.producto_sala_cremas, 'cliente', '') or ''
            self.producto = getattr(self.producto_sala_cremas, 'producto', '') or getattr(self.producto_sala_cremas, 'nombre', '') or ''
            self.codigo = getattr(self.producto_sala_cremas, 'codigo', '') or ''

        self.acciones_correctivas_requieren_revision = bool(
            self.accion_correctiva and self.accion_correctiva.strip()
        )

        super().save(*args, **kwargs)

    @property
    def estado_verificacion(self):
        if self.verificado:
            return 'Verificado final'

        if self.acciones_correctivas_requieren_revision and not self.acciones_correctivas_verificadas:
            return 'Pendiente revisión acción correctiva'

        return 'Listo para verificación final'

    @property
    def clase_estado(self):
        if self.verificado:
            return 'estado-ok'

        if self.acciones_correctivas_requieren_revision and not self.acciones_correctivas_verificadas:
            return 'estado-alerta'

        return 'estado-pendiente'

    def __str__(self):
        return f'{self.fecha_hora:%d-%m-%Y %H:%M} | {self.cliente} | {self.producto} | {self.lote}'