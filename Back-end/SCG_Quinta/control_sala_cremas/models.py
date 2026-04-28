from django.db import models
from django.utils import timezone


class RegistroSalaCremas(models.Model):
    TURNOS = [
        ("Turno A", "Turno A"),
        ("Turno B", "Turno B"),
        ("Turno C", "Turno C"),
    ]

    usuario = models.CharField(max_length=150)
    fecha_hora = models.DateTimeField(default=timezone.now)

    turno = models.CharField(max_length=20, choices=TURNOS)
    cliente = models.CharField(max_length=150)
    producto = models.CharField(max_length=150)
    codigo = models.CharField(max_length=80)
    lote = models.CharField(max_length=100)

    densidad = models.DecimalField(max_digits=8, decimal_places=3)
    temperatura = models.DecimalField(max_digits=8, decimal_places=2)
    numero_batidora = models.CharField(max_length=50)

    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-fecha_hora"]
        verbose_name = "Registro sala de cremas"
        verbose_name_plural = "Registros sala de cremas"

    def __str__(self):
        return f"{self.producto} - Lote {self.lote} - {self.fecha_hora:%d-%m-%Y %H:%M}"