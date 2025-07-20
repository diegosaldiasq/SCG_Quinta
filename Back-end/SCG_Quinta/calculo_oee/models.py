from django.db import models

# Create your models here.

class TurnoOEE(models.Model):
    fecha = models.DateTimeField(null=False, blank=False)
    cliente = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, null=True, blank=True) 
    producto = models.CharField(max_length=100)
    linea = models.CharField(max_length=50)
    turno = models.CharField(max_length=20)
    numero_personas = models.PositiveIntegerField(help_text="Número de personas que trabajan en el turno", null=True, blank=True)
    lote = models.CharField(max_length=20, null=True, blank=True)
    supervisor = models.CharField(max_length=50, null=True, blank=True)
    tiempo_planeado = models.PositiveIntegerField(help_text="En minutos")
    produccion_planeada = models.PositiveIntegerField(help_text="Producción planeada en unidades")
    produccion_real = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        # opción A: unique_together (deprecated pero sencillo)
        unique_together = ('fecha', 'linea', 'producto', 'lote', 'turno')

    def __str__(self):
        return f"{self.fecha} - {self.linea} - {self.turno}"

class Detencion(models.Model):
    lote = models.ForeignKey(TurnoOEE, on_delete=models.CASCADE, related_name='detenciones')
    motivo = models.CharField(max_length=100)
    hora_inicio = models.TimeField(null=True, blank=True)  # Puede ser null si aún está en curso
    hora_fin = models.TimeField(null=True, blank=True)  # Puede ser null si aún está en curso
    duracion = models.PositiveIntegerField(help_text="Duración en minutos")

class Reproceso(models.Model):
    lote = models.ForeignKey(TurnoOEE, on_delete=models.CASCADE, related_name='reprocesos')
    motivo = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()

class ResumenTurnoOee(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, null=True, blank=True)
    producto = models.CharField(max_length=100)
    linea   = models.CharField(max_length=50)
    lote = models.ForeignKey(TurnoOEE, on_delete=models.CASCADE, related_name='resumenes_turno')
    turno = models.CharField(max_length=20)
    supervisor = models.CharField(max_length=50, null=True, blank=True)
    tiempo_paro = models.PositiveIntegerField(help_text="Tiempo de paro en minutos")
    tiempo_planeado = models.PositiveIntegerField(help_text="Tiempo planeado en minutos")
    produccion_teorica = models.PositiveIntegerField(help_text="Producción teórica en unidades")
    produccion_planificada = models.PositiveIntegerField(help_text="Producción planificada en unidades", null=True, blank=True)
    produccion_real = models.PositiveIntegerField(help_text="Producción real en unidades")
    productos_malos = models.PositiveIntegerField(help_text="Cantidad de productos malos")
    productos_buenos = models.PositiveIntegerField(help_text="Cantidad de productos buenos")
    numero_personas = models.PositiveIntegerField(help_text="Número de personas que trabajaron en el turno", null=True, blank=True)
    unidades_por_persona = models.FloatField(help_text="Unidades producidas por persona", null=True, blank=True)
    unidades_pp_hora = models.FloatField(help_text="Unidades producidas por persona por hora", null=True, blank=True)
    eficiencia = models.FloatField(help_text="Eficiencia del turno en porcentaje")
    disponibilidad = models.FloatField(help_text="Disponibilidad del turno en porcentaje")
    calidad = models.FloatField(help_text="Calidad del turno en porcentaje")
    oee = models.FloatField(help_text="OEE del turno en porcentaje")
    verificado = models.BooleanField(default=False)
    verificado_por = models.CharField(max_length=50 ,null=True, blank=True)
    fecha_de_verificacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Resumen OEE - {self.turno} - Eficiencia: {self.eficiencia}%"