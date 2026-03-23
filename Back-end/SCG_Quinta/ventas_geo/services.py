import pandas as pd


COLUMNAS_ESPERADAS = [
    'producto',
    'local',
    'direccion',
    'comuna',
    'ciudad',
    'cantidad',
    'fecha',
]


def procesar_carga_ventas(carga):
    ruta_archivo = carga.archivo.path
    df = pd.read_excel(ruta_archivo)

    columnas_archivo = [str(c).strip().lower() for c in df.columns]
    faltantes = [c for c in COLUMNAS_ESPERADAS if c not in columnas_archivo]

    if faltantes:
        raise ValueError(f'Faltan columnas obligatorias: {", ".join(faltantes)}')

    carga.filas_leidas = len(df)
    carga.filas_ok = len(df)
    carga.filas_error = 0
    carga.procesado = True
    carga.save()

    return carga