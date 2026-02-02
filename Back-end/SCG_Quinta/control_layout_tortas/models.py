from django.db import models
from django.utils import timezone


class Planta(models.TextChoices):
    PV = "PV", "PV"
    ENEA = "ENEA", "ENEA"
    CURICO = "CURICO", "Curicó"


class TipoCapa(models.TextChoices):
    BIZCOCHO = "BIZCOCHO", "Bizcocho"
    REMOJO = "REMOJO", "Remojo"
    RELLENO = "RELLENO", "Relleno"
    RELLENO_MANUAL = "RELLENO_MANUAL", "Relleno manual"
    REBOZADO = "REBOZADO", "Rebozado"
    GRANA = "GRANA", "Grana"
    BRILLO = "BRILLO", "Brillo"
    MONOS = "MONOS", "Moños"
    DECORADO = "DECORADO", "Decorado"
    DECORADO_2 = "DECORADO_2", "Decorado 2"
    CHOCOLATE = "CHOCOLATE", "Chocolate"
    OTRO = "OTRO", "Otro"

class CategoriaIngrediente(models.TextChoices):
    CREMA = "CREMA", "Crema"
    MERMELADA = "MERMELADA", "Mermelada"
    MANJAR = "MANJAR", "Manjar / Dulce"
    REMOJO = "REMOJO", "Remojo / Jarabe"
    BIZCOCHO = "BIZCOCHO", "Bizcocho"
    COBERTURA = "COBERTURA", "Cobertura / Rebozado"
    DECORACION = "DECORACION", "Decoración"
    CHOCOLATE = "CHOCOLATE", "Chocolate"
    OTRO = "OTRO", "Otro"


class Ingrediente(models.Model):
    """
    Catálogo maestro de ingredientes usados en capas.
    """
    nombre = models.CharField(max_length=120)  # Ej: "Crema Blanca", "Mermelada de piña"
    categoria = models.CharField(max_length=20, choices=CategoriaIngrediente.choices, default=CategoriaIngrediente.OTRO)
    activo = models.BooleanField(default=True)

    # Opcionales útiles:
    descripcion = models.CharField(max_length=200, blank=True, default="")
    codigo_interno = models.CharField(max_length=40, blank=True, default="")  # si quieres mapear a ERP/insumo
    proveedor = models.CharField(max_length=80, blank=True, default="")
    creado_en = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["categoria", "nombre"]
        unique_together = [("nombre", "categoria")]

    def __str__(self):
        return f"{self.get_categoria_display()} - {self.nombre}"

class ProductoTorta(models.Model):
    """
    Catálogo de tortas por cliente/código.
    Si ya tienes catálogo en otra app, puedes reemplazar esto por FK a tu modelo actual.
    """
    cliente = models.CharField(max_length=80, blank=True, default="")
    nombre = models.CharField(max_length=160)
    codigo = models.CharField(max_length=30, blank=True, default="")

    class Meta:
        unique_together = [("codigo", "nombre")]
        ordering = ["cliente", "nombre"]

    def __str__(self):
        parts = []

        if self.cliente:
            parts.append(self.cliente)

        if self.codigo:
            parts.append(self.codigo)

        parts.append(self.nombre)

        return " - ".join(parts)


class LayoutTorta(models.Model):
    """
    Layout objetivo (receta de armado) por planta + producto.
    """
    planta = models.CharField(max_length=10, choices=Planta.choices)
    producto = models.ForeignKey(ProductoTorta, on_delete=models.PROTECT)
    version = models.PositiveIntegerField(default=1)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-activo", "planta", "producto__nombre", "-version"]
        unique_together = [("planta", "producto", "version")]

    def __str__(self):
        return f"{self.planta} - {self.producto} v{self.version}"


class LayoutCapa(models.Model):
    layout = models.ForeignKey(LayoutTorta, on_delete=models.CASCADE, related_name="capas")
    orden = models.PositiveIntegerField()
    tipo = models.CharField(max_length=30, choices=TipoCapa.choices)

    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.PROTECT)
    etiqueta = models.CharField(
        max_length=120,
        blank=True,
        default="",
        help_text="Texto libre opcional (ej: 'Relleno 1', 'Mermelada guinda'). Si está vacío se usa el ingrediente."
    )

    peso_objetivo_g = models.DecimalField(max_digits=8, decimal_places=1)
    tolerancia_menos_g = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    tolerancia_mas_g = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    obligatorio = models.BooleanField(default=True)

    class Meta:
        ordering = ["layout", "orden"]
        unique_together = [("layout", "orden")]

    def __str__(self):
        label = self.etiqueta.strip() or self.ingrediente.nombre
        return f"{self.layout} #{self.orden} {label}"


class RegistroLayout(models.Model):
    """
    Control real (cabecera) de un armado/pesaje.
    """
    planta = models.CharField(max_length=10, choices=Planta.choices)
    layout = models.ForeignKey(LayoutTorta, on_delete=models.PROTECT)
    fecha = models.DateField(default=timezone.localdate)
    turno = models.CharField(max_length=20, blank=True, default="")
    linea = models.CharField(max_length=30, blank=True, default="")
    lote = models.CharField(max_length=40, blank=True, default="")
    operador = models.CharField(max_length=120, blank=True, default="")
    observaciones = models.TextField(blank=True, default="")
    creado_en = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-creado_en"]

    def __str__(self):
        return f"{self.fecha} {self.planta} - {self.layout}"


class RegistroCapa(models.Model):
    registro = models.ForeignKey(RegistroLayout, on_delete=models.CASCADE, related_name="detalles")
    capa = models.ForeignKey(LayoutCapa, on_delete=models.PROTECT)

    ingrediente_usado = models.ForeignKey(
        Ingrediente,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text="Si se usó un ingrediente distinto al planificado."
    )

    peso_real_g = models.DecimalField(max_digits=8, decimal_places=1, null=True, blank=True)
    comentario = models.CharField(max_length=200, blank=True, default="")

    class Meta:
        unique_together = [("registro", "capa")]
        ordering = ["capa__orden"]

    @property
    def objetivo(self):
        return self.capa.peso_objetivo_g

    @property
    def desviacion_g(self):
        if self.peso_real_g is None:
            return None
        return self.peso_real_g - self.capa.peso_objetivo_g
    
    @property
    def cumple(self):
        if self.peso_real_g is None:
            return None

        minimo = self.capa.peso_objetivo_g - (self.capa.tolerancia_menos_g or 0)
        maximo = self.capa.peso_objetivo_g + (self.capa.tolerancia_mas_g or 0)
        return minimo <= self.peso_real_g <= maximo
    
    @property
    def ingrediente_final(self):
        return self.ingrediente_usado or self.capa.ingrediente