from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q


PLANTAS = [("ENEA", "ENEA"), ("PUERTO_VESPUCIO", "Puerto Vespucio")]
TURNOS = [(x, f"Turno {x}") for x in "ABC"]


class AreaProductividad(models.Model):
    codigo = models.SlugField(max_length=40, unique=True)
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    mide_semielaborado = models.BooleanField(default=True)
    definicion_dotacion = models.TextField(
        default="Personas presentes del área durante el turno."
    )

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class AsignacionProductividad(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    planta = models.CharField(max_length=30, choices=PLANTAS)
    area = models.ForeignKey(AreaProductividad, on_delete=models.PROTECT)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["usuario", "planta", "area"], name="prod_asignacion_unica"
        )]
        verbose_name_plural = "Asignaciones de productividad"

    def __str__(self):
        return f"{self.usuario} · {self.get_planta_display()} · {self.area}"


class ProgramacionTurno(models.Model):
    fecha_operativa = models.DateField(db_index=True)
    planta = models.CharField(max_length=30, choices=PLANTAS)
    area = models.ForeignKey(AreaProductividad, on_delete=models.PROTECT)
    turno = models.CharField(max_length=1, choices=TURNOS)
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    meta_pt = models.PositiveIntegerField()
    programado = models.BooleanField(default=True)
    extraordinario = models.BooleanField(default=False)
    motivo = models.TextField(blank=True)
    version = models.PositiveIntegerField(default=1)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["fecha_operativa", "planta", "area", "turno"]
        constraints = [
            models.UniqueConstraint(fields=["fecha_operativa", "planta", "area", "turno"], name="prod_programacion_unica"),
            models.CheckConstraint(check=Q(fin__gt=models.F("inicio")), name="prod_horario_valido"),
            models.CheckConstraint(check=Q(meta_pt__gte=0), name="prod_meta_no_negativa"),
        ]
        indexes = [models.Index(fields=["planta", "area", "fecha_operativa"], name="prod_alcance_fecha_idx")]

    def __str__(self):
        return f"{self.fecha_operativa} · {self.get_planta_display()} · {self.area} · {self.turno}"


class RegistroProductividadTurno(models.Model):
    BORRADOR, CERRADO, VERIFICADO = "BORRADOR", "CERRADO", "VERIFICADO"
    ESTADOS = [(BORRADOR, "Borrador"), (CERRADO, "Cerrado"), (VERIFICADO, "Verificado")]
    programacion = models.OneToOneField(ProgramacionTurno, on_delete=models.PROTECT, related_name="registro")
    dotacion = models.PositiveIntegerField(null=True, blank=True)
    semielaborados = models.PositiveIntegerField(null=True, blank=True)
    terminadas = models.PositiveIntegerField(null=True, blank=True)
    horas_persona = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal("0.01"))])
    meta_pt_cierre = models.PositiveIntegerField(null=True, blank=True)
    observaciones = models.TextField(blank=True)
    estado = models.CharField(max_length=12, choices=ESTADOS, default=BORRADOR, db_index=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="productividad_creada")
    cerrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="productividad_cerrada")
    verificado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="productividad_verificada")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    cerrado = models.DateTimeField(null=True, blank=True)
    verificado = models.DateTimeField(null=True, blank=True)
    version = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["-programacion__fecha_operativa", "programacion__turno"]
        permissions = [
            ("registrar_turno", "Ingresar y editar borradores de productividad"),
            ("cerrar_turno", "Cerrar turnos de productividad"),
            ("verificar_turno", "Verificar cierres de productividad"),
            ("reabrir_turno", "Reabrir cierres de productividad"),
            ("programar_turno", "Administrar programación y metas"),
        ]
        constraints = [
            models.CheckConstraint(check=Q(horas_persona__isnull=True) | Q(horas_persona__gt=0), name="prod_hh_positivas"),
            models.CheckConstraint(check=Q(estado="BORRADOR") | (Q(dotacion__gt=0) & Q(dotacion__isnull=False) & Q(terminadas__isnull=False) & Q(meta_pt_cierre__isnull=False) & Q(cerrado__isnull=False)), name="prod_cierre_completo"),
            models.CheckConstraint(check=Q(estado__in=["BORRADOR", "CERRADO", "VERIFICADO"]), name="prod_estado_valido"),
        ]

    def __str__(self):
        return f"{self.programacion} · {self.get_estado_display()}"


class RevisionProductividad(models.Model):
    programacion = models.ForeignKey(ProgramacionTurno, on_delete=models.PROTECT, related_name="revisiones")
    accion = models.CharField(max_length=30)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField(blank=True)
    antes = models.JSONField(default=dict)
    despues = models.JSONField(default=dict)

    class Meta:
        ordering = ["-fecha", "-id"]
        verbose_name_plural = "Historial de cambios de productividad"

    def __str__(self):
        return f"{self.accion} · {self.programacion}"
