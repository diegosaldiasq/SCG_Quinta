"""Validación y cálculo OEE. un_pp conserva la unidad existente: unidades/persona/turno."""
from math import isfinite

from django.conf import settings
from django.db import transaction

from control_de_pesos.models import ProductoControlPeso
from .configuracion import CONFIGURACION_PLANTAS
from .models import TurnoOEE, ResumenTurnoOee


def obtener_un_pp(planta, supervisor, cliente, producto, codigo):
    configuracion = CONFIGURACION_PLANTAS.get(planta, {})
    area = configuracion.get('area_por_supervisor', {}).get(supervisor)
    clientes = configuracion.get('clientes_por_area', {}).get(area, [])
    if not area or cliente not in clientes:
        return 0
    item = ProductoControlPeso.objects.filter(
        area=area, activo=True, cliente=cliente, producto=producto,
        codigo=codigo,
    ).first()
    return float(item.un_pp) if item and item.un_pp is not None else 0


def evaluar_turno(lote):
    """Devuelve datos del resumen y motivos; nunca guarda ni limita porcentajes."""
    motivos = []
    personas = lote.numero_personas or 0
    tiempo = lote.tiempo_planeado or 0
    real = lote.produccion_real
    productos = list(lote.productos.all())
    detenciones = list(lote.detenciones.all())
    malos = sum(r.cantidad for r in lote.reprocesos.all())
    paro = sum(d.duracion for d in detenciones)
    if real is None:
        motivos.append('Falta ingresar la producción real.')
    if personas <= 0:
        motivos.append('La cantidad de personas debe ser mayor que cero.')
    if tiempo <= 0:
        motivos.append('El tiempo planeado debe ser mayor que cero.')
    if not lote.supervisor:
        motivos.append('Falta el supervisor.')
    if not lote.produccion_planeada or lote.produccion_planeada <= 0:
        motivos.append('Falta una producción planeada mayor que cero.')
    if paro > tiempo:
        motivos.append(f'Detenciones ({paro} min) mayores que el tiempo planeado ({tiempo} min).')
    if malos > (real or 0):
        motivos.append(f'Reprocesos ({malos}) mayores que la producción real ({real or 0}).')
    if real and paro == tiempo:
        motivos.append('Hay producción con tiempo operativo igual a cero.')

    # Posicionar las horas nocturnas después de las 23:00 del día operacional.
    origen = 23 * 60 if str(lote.turno).upper().strip() in ('A', 'TURNO A') else 0
    intervalos = []
    for d in detenciones:
        inicio = (d.hora_inicio.hour * 60 + d.hora_inicio.minute - origen) % 1440
        duracion = ((d.hora_fin.hour * 60 + d.hora_fin.minute)
                    - (d.hora_inicio.hour * 60 + d.hora_inicio.minute)) % 1440
        if duracion != d.duracion:
            motivos.append(f'La duración de la detención {d.id} no coincide con sus horarios.')
        if duracion:
            intervalos.append((inicio, inicio + duracion))
    fin_anterior = -1
    for inicio, fin in sorted(intervalos):
        if inicio < fin_anterior:
            motivos.append('Hay detenciones con horarios superpuestos.')
            break
        fin_anterior = max(fin_anterior, fin)

    filas = productos or [lote]
    plan = sum(p.produccion_planeada or 0 for p in filas)
    if productos:
        if any(p.produccion_real is None for p in productos):
            motivos.append('Falta completar la producción real de uno o más productos.')
        if any(not p.produccion_planeada for p in productos):
            motivos.append('Falta la producción planeada de uno o más productos.')
        if sum(p.produccion_real or 0 for p in productos) != (real or 0):
            motivos.append('La suma de la producción real por producto no coincide con el total del turno.')
        if plan != lote.produccion_planeada:
            motivos.append('La suma de la producción planeada por producto no coincide con el total del turno.')

    tasas = []
    for p in filas:
        tasa = obtener_un_pp(lote.planta, lote.supervisor, p.cliente, p.producto, p.codigo)
        if not isfinite(tasa) or tasa <= 0:
            motivos.append(f'Falta una tasa nominal válida para «{p.producto}» en el área del supervisor.')
        tasas.append(tasa)

    if motivos:
        return None, list(dict.fromkeys(motivos))

    # Media armónica ponderada por unidades reales. Si no hubo producción,
    # utilizar la mezcla planeada permite mantener una capacidad teórica válida.
    pesos = [p.produccion_real or 0 for p in filas] if real else [p.produccion_planeada for p in filas]
    tasa_nominal = sum(pesos) / sum(peso / tasa for peso, tasa in zip(pesos, tasas))
    teorica = tasa_nominal * personas
    disponibilidad = (tiempo - paro) / tiempo * 100
    rendimiento = real / teorica * 100
    calidad = (real - malos) / real * 100 if real else 0
    oee = disponibilidad * rendimiento * calidad / 10000
    limite = float(getattr(settings, 'OEE_RENDIMIENTO_MAXIMO', 100))
    if not isfinite(limite) or limite < 100:
        raise ValueError('OEE_RENDIMIENTO_MAXIMO debe ser finito y mayor o igual a 100.')
    if rendimiento > limite + 1e-9:
        motivos.append(f'Rendimiento {rendimiento:.2f} % superior al límite de {limite:g} %. Revisar tasa nominal, personas y producción.')
    if oee > 100 + 1e-9:
        motivos.append(f'OEE {oee:.2f} % superior al 100 %.')
    if motivos:
        return None, motivos

    def concatenar(campo):
        return ', '.join(dict.fromkeys(getattr(p, campo) for p in filas if getattr(p, campo)))

    datos = dict(
        planta=lote.planta, fecha=lote.fecha, turno=lote.turno,
        supervisor=lote.supervisor, cliente=concatenar('cliente'),
        codigo=concatenar('codigo'), producto=concatenar('producto'), linea=lote.linea,
        tiempo_paro=paro, tiempo_planeado=tiempo, produccion_teorica=round(teorica),
        produccion_planificada=plan, produccion_real=real, productos_malos=malos,
        productos_buenos=real - malos, numero_personas=personas,
        unidades_por_persona=round(real / personas, 2),
        unidades_pp_hora=round(real / (tiempo / 60) / personas, 2),
        eficiencia=round(rendimiento, 2), disponibilidad=round(disponibilidad, 2),
        calidad=round(calidad, 2), oee=round(oee, 2),
    )
    for campo in ('cliente', 'codigo', 'producto'):
        if len(datos[campo]) > ResumenTurnoOee._meta.get_field(campo).max_length:
            motivos.append(f'El texto combinado de {campo} supera el espacio del resumen.')
    return (None, motivos) if motivos else (datos, [])


@transaction.atomic
def calcular_oee_automatico(lote_id):
    # Serializar todos los cálculos de un mismo turno para impedir duplicados.
    lote = TurnoOEE.objects.select_for_update().get(pk=lote_id)
    existente = lote.resumenes_turno.first()
    if existente:
        # Los resúmenes históricos y la verificación humana se conservan.
        return existente, []
    datos, motivos = evaluar_turno(lote)
    if motivos:
        return None, motivos
    return ResumenTurnoOee.objects.create(lote=lote, **datos), []
