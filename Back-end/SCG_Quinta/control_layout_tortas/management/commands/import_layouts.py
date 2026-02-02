import re
from decimal import Decimal, InvalidOperation

import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from control_layout_tortas.models import (
    ProductoTorta,
    LayoutTorta,
    LayoutCapa,
    Planta,
    TipoCapa,
)


# Orden y tipo por columna
COLUMN_MAP = [
    ("Bizcocho", TipoCapa.BIZCOCHO),
    ("Remojo 1", TipoCapa.REMOJO),
    ("Relleno 1", TipoCapa.RELLENO),
    ("Relleno 2", TipoCapa.RELLENO),
    ("Relleno manual 1", TipoCapa.RELLENO_MANUAL),
    ("Remojo 2", TipoCapa.REMOJO),
    ("Relleno 3", TipoCapa.RELLENO),
    ("Relleno 4", TipoCapa.RELLENO),
    ("Relleno manual 2", TipoCapa.RELLENO_MANUAL),
    ("Remojo 3", TipoCapa.REMOJO),
    ("Rebozado", TipoCapa.REBOZADO),
    ("Grana", TipoCapa.GRANA),
    ("Brillo", TipoCapa.BRILLO),
    ("Moños", TipoCapa.MONOS),
    ("Decorado 1", TipoCapa.DECORADO),
    ("Decorado 2", TipoCapa.DECORADO_2),
    ("Chocolatera", TipoCapa.CHOCOLATE),
]


def normalize_planta(value: str) -> str:
    v = (value or "").strip().upper()
    if v in ("PV",):
        return Planta.PV
    if v in ("ENEA", "ENEA."):
        return Planta.ENEA
    if v in ("CURICO", "CURICÓ", "CURICÓ."):
        return Planta.CURICO
    raise ValueError(f"Planta inválida: {value!r}. Usa PV, ENEA o CURICO.")


def parse_decimal(value) -> Decimal | None:
    """
    Convierte celdas típicas: 110, 110.0, "110", "110 g", "110gr", etc.
    Si no se puede, devuelve None.
    """
    if value is None:
        return None
    if isinstance(value, (int, float)):
        try:
            return Decimal(str(value)).quantize(Decimal("0.1"))
        except InvalidOperation:
            return None

    s = str(value).strip()
    if s == "":
        return None

    # Extraer primer número (permite coma o punto)
    m = re.search(r"(-?\d+(?:[.,]\d+)?)", s)
    if not m:
        return None
    num = m.group(1).replace(",", ".")
    try:
        return Decimal(num).quantize(Decimal("0.1"))
    except InvalidOperation:
        return None


class Command(BaseCommand):
    help = "Importa layouts objetivos (capas) desde Excel/CSV y crea LayoutTorta + LayoutCapa."

    def add_arguments(self, parser):
        parser.add_argument("--file", required=True, help="Ruta del archivo .xlsx / .csv")
        parser.add_argument("--sheet", default="Sheet1", help="Nombre de la hoja (si es Excel)")
        #parser.add_argument("--cliente", default="", help="Cliente (opcional) para ProductoTorta")
        parser.add_argument("--version", type=int, default=1, help="Versión del layout a crear (default 1)")
        parser.add_argument("--inactivar-otros", action="store_true", help="Deja inactivos otros layouts del mismo producto/planta")
        parser.add_argument("--tolerancia", type=float, default=0.0, help="Tolerancia ±g por defecto para todas las capas (ej: 5)")
        parser.add_argument("--dry-run", action="store_true", help="No guarda, solo muestra lo que haría")

    @transaction.atomic
    def handle(self, *args, **opts):
        path = opts["file"]
        sheet = opts["sheet"]
        #cliente = (opts["cliente"] or "").strip()
        version = opts["version"]
        inactivar_otros = opts["inactivar_otros"]
        tol = Decimal(str(opts["tolerancia"])).quantize(Decimal("0.1"))
        dry = opts["dry_run"]

        # Leer archivo
        if path.lower().endswith(".csv"):
            df = pd.read_csv(path)
        elif path.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(path, sheet_name=sheet)
        else:
            raise CommandError("Formato no soportado. Usa .xlsx o .csv")

        required = {"Planta", "Cliente", "Codigo", "Torta"}
        missing = required - set(df.columns)
        if missing:
            raise CommandError(f"Faltan columnas obligatorias: {missing}")

        # Validar columnas de capas (no obligatorio que estén todas, pero advierto)
        cap_cols = [c for c, _ in COLUMN_MAP]
        present_cap_cols = [c for c in cap_cols if c in df.columns]
        if not present_cap_cols:
            raise CommandError("No encuentro ninguna columna de capas (Bizcocho/Remojo/etc.). Revisa encabezados.")

        created_layouts = 0
        created_capas = 0

        for idx, row in df.iterrows():
            planta_raw = row.get("Planta", "")
            torta_nombre = (row.get("Torta", "") or "").strip()
            if not torta_nombre:
                self.stdout.write(self.style.WARNING(f"Fila {idx+2}: Torta vacía, se omite."))
                continue

            try:
                planta = normalize_planta(planta_raw)
            except ValueError as e:
                raise CommandError(f"Fila {idx+2}: {e}")

            # Producto
            cliente_xlsx = (row.get("Cliente", "") or "").strip()
            codigo_xlsx = (row.get("Codigo", "") or "").strip()
            torta_nombre = (row.get("Torta", "") or "").strip()

            if not cliente_xlsx:
                self.stdout.write(self.style.WARNING(f"Fila {idx+2}: Cliente vacío. Se usará ''."))
            if not codigo_xlsx:
                self.stdout.write(self.style.WARNING(f"Fila {idx+2}: Código vacío. Se guardará ''."))
            if not torta_nombre:
                self.stdout.write(self.style.WARNING(f"Fila {idx+2}: Torta vacía, se omite."))
                continue

            # Upsert por (cliente, codigo) cuando hay código; si no, por (cliente, nombre)
            if codigo_xlsx:
                producto, created = ProductoTorta.objects.get_or_create(
                    cliente=cliente_xlsx,
                    codigo=codigo_xlsx,
                    defaults={"nombre": torta_nombre},
                )
                # si ya existe, actualiza nombre si cambió
                if not dry and producto.nombre != torta_nombre:
                    producto.nombre = torta_nombre
                    producto.save(update_fields=["nombre"])
            else:
                producto, created = ProductoTorta.objects.get_or_create(
                    cliente=cliente_xlsx,
                    nombre=torta_nombre,
                    defaults={"codigo": ""},
                )

            if inactivar_otros:
                if not dry:
                    LayoutTorta.objects.filter(planta=planta, producto=producto).update(activo=False)

            # Layout
            if dry:
                layout = None
            else:
                layout, layout_created = LayoutTorta.objects.get_or_create(
                    planta=planta,
                    producto=producto,
                    version=version,
                    defaults={"activo": True},
                )
                if not layout_created:
                    # Si existe, lo dejamos activo por si estaba apagado
                    layout.activo = True
                    layout.save(update_fields=["activo"])

            created_layouts += 1

            # Capas
            orden = 1
            for col, tipo in COLUMN_MAP:
                if col not in df.columns:
                    continue

                val = row.get(col, None)
                peso = parse_decimal(val)
                if peso is None:
                    # Si está vacío/no numérico, no creamos esa capa
                    continue

                nombre_capa = col  # puedes cambiarlo si quieres un nombre más “bonito”
                if dry:
                    created_capas += 1
                else:
                    capa, capa_created = LayoutCapa.objects.update_or_create(
                        layout=layout,
                        orden=orden,
                        defaults={
                            "tipo": tipo,
                            "nombre": nombre_capa,
                            "peso_objetivo_g": peso,
                            "tolerancia_menos_g": tol,
                            "tolerancia_mas_g": tol,
                            "obligatorio": True,
                        },
                    )
                    if capa_created:
                        created_capas += 1
                orden += 1

        if dry:
            raise CommandError(
                f"DRY-RUN: procesé {created_layouts} filas. "
                f"Crearía/actualizaría {created_layouts} layouts y {created_capas} capas."
            )

        self.stdout.write(self.style.SUCCESS(
            f"OK: procesé {created_layouts} filas. Capas creadas/actualizadas: {created_capas}."
        ))