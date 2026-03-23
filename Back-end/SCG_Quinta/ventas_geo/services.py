import json
import pandas as pd
import requests

from decimal import Decimal, InvalidOperation
from django.conf import settings
from django.db import transaction

from .models import (
    Producto,
    Local,
    Venta,
    ErrorCargaVenta,
)


COLUMNAS_ESPERADAS = [
    'producto',
    'local',
    'direccion',
    'comuna',
    'ciudad',
    'cantidad',
    'fecha',
]


def normalizar_texto(valor):
    if pd.isna(valor):
        return ''
    return str(valor).strip()


def construir_direccion_completa(direccion, comuna, ciudad):
    partes = [direccion, comuna, ciudad, 'Chile']
    return ', '.join([p.strip() for p in partes if p and str(p).strip()])


def geocodificar_direccion_google(direccion_completa):
    api_key = settings.GOOGLE_GEOCODING_API_KEY
    if not api_key:
        return {
            'ok': False,
            'error': 'No está configurada la GOOGLE_GEOCODING_API_KEY'
        }

    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'address': direccion_completa,
        'key': api_key,
        'region': 'cl',
        'language': 'es',
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return {
            'ok': False,
            'error': f'Error de conexión con Google Geocoding API: {e}'
        }

    status = data.get('status')

    if status != 'OK':
        return {
            'ok': False,
            'error': f'Google Geocoding API respondió con estado: {status}'
        }

    results = data.get('results', [])
    if not results:
        return {
            'ok': False,
            'error': 'No se encontraron coordenadas para la dirección'
        }

    resultado = results[0]
    location = resultado.get('geometry', {}).get('location', {})

    lat = location.get('lat')
    lng = location.get('lng')
    formatted_address = resultado.get('formatted_address', '')

    if lat is None or lng is None:
        return {
            'ok': False,
            'error': 'La respuesta no contiene latitud/longitud'
        }

    return {
        'ok': True,
        'latitud': lat,
        'longitud': lng,
        'direccion_formateada': formatted_address,
        'respuesta_cruda': data,
    }


def validar_columnas(df):
    columnas_archivo = [str(c).strip().lower() for c in df.columns]
    faltantes = [c for c in COLUMNAS_ESPERADAS if c not in columnas_archivo]
    return faltantes


def obtener_valor_fila(row, nombre_columna):
    for col in row.index:
        if str(col).strip().lower() == nombre_columna.lower():
            return row[col]
    return None


@transaction.atomic
def procesar_carga_ventas(carga):
    ruta_archivo = carga.archivo.path
    df = pd.read_excel(ruta_archivo)

    faltantes = validar_columnas(df)
    if faltantes:
        raise ValueError(f'Faltan columnas obligatorias: {", ".join(faltantes)}')

    carga.filas_leidas = len(df)
    carga.filas_ok = 0
    carga.filas_error = 0
    carga.save()

    for index, row in df.iterrows():
        fila_excel = index + 2

        try:
            producto_nombre = normalizar_texto(obtener_valor_fila(row, 'producto'))
            local_nombre = normalizar_texto(obtener_valor_fila(row, 'local'))
            direccion = normalizar_texto(obtener_valor_fila(row, 'direccion'))
            comuna = normalizar_texto(obtener_valor_fila(row, 'comuna'))
            ciudad = normalizar_texto(obtener_valor_fila(row, 'ciudad'))
            cantidad_valor = obtener_valor_fila(row, 'cantidad')
            fecha_valor = obtener_valor_fila(row, 'fecha')

            if not producto_nombre:
                raise ValueError('Producto vacío')

            if not local_nombre:
                raise ValueError('Local vacío')

            if not direccion:
                raise ValueError('Dirección vacía')

            if pd.isna(cantidad_valor) or str(cantidad_valor).strip() == '':
                raise ValueError('Cantidad vacía')

            try:
                cantidad = Decimal(str(cantidad_valor))
            except (InvalidOperation, ValueError):
                raise ValueError(f'Cantidad inválida: {cantidad_valor}')

            if pd.isna(fecha_valor) or str(fecha_valor).strip() == '':
                raise ValueError('Fecha vacía')

            fecha = pd.to_datetime(fecha_valor).date()

            producto, _ = Producto.objects.get_or_create(
                nombre=producto_nombre
            )

            local = Local.objects.filter(
                nombre=local_nombre,
                direccion=direccion
            ).first()

            if not local:
                direccion_completa = construir_direccion_completa(
                    direccion=direccion,
                    comuna=comuna,
                    ciudad=ciudad
                )

                geo = geocodificar_direccion_google(direccion_completa)

                if not geo['ok']:
                    raise ValueError(f'No se pudo geocodificar la dirección: {geo["error"]}')

                local = Local.objects.create(
                    nombre=local_nombre,
                    direccion=direccion,
                    comuna=comuna or None,
                    ciudad=ciudad or None,
                    latitud=geo['latitud'],
                    longitud=geo['longitud'],
                    direccion_formateada=geo.get('direccion_formateada', '')
                )
            else:
                if (local.latitud is None or local.longitud is None):
                    direccion_completa = construir_direccion_completa(
                        direccion=direccion,
                        comuna=comuna,
                        ciudad=ciudad
                    )

                    geo = geocodificar_direccion_google(direccion_completa)

                    if geo['ok']:
                        local.latitud = geo['latitud']
                        local.longitud = geo['longitud']
                        local.direccion_formateada = geo.get('direccion_formateada', '')
                        local.comuna = comuna or local.comuna
                        local.ciudad = ciudad or local.ciudad
                        local.save()

            Venta.objects.create(
                producto=producto,
                local=local,
                cantidad=cantidad,
                fecha=fecha,
                carga=carga
            )

            carga.filas_ok += 1

        except Exception as e:
            datos_serializados = {}
            try:
                for col in row.index:
                    valor = row[col]
                    if pd.isna(valor):
                        valor = ''
                    datos_serializados[str(col)] = str(valor)
            except Exception:
                datos_serializados = {'error': 'No fue posible serializar la fila'}

            ErrorCargaVenta.objects.create(
                carga=carga,
                fila_excel=fila_excel,
                mensaje=str(e),
                datos_fila=json.dumps(datos_serializados, ensure_ascii=False)
            )
            carga.filas_error += 1

    carga.procesado = True
    carga.save()

    return carga