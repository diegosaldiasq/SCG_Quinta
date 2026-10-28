from decimal import Decimal, ROUND_HALF_UP

from django import template
from django.utils.numberformat import format as number_format

register = template.Library()


@register.filter
def numero(value, decimals=0):
    if value is None or value == "":
        return "—"
    places = int(decimals)
    rounded = Decimal(str(value)).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)
    return number_format(rounded, decimal_sep=",", decimal_pos=places, grouping=3, thousand_sep=".", force_grouping=True)


@register.filter
def porcentaje(value):
    return "Sin datos" if value is None or value == "" else f"{numero(value, 1)} %"


@register.filter
def semaforo(value):
    if value is None or value == "":
        return "info"
    return "good" if value >= 100 else "warn" if value >= 90 else "bad"
