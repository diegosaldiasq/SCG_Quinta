from datetime import timedelta
from urllib.parse import urlencode

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .permissions import require_permission
from .views import base_context
from .weekly_forms import MotivoSemanaForm, SemanaFormSet, SemanaScopeForm
from .weekly_services import DIAS, cargar_semana, guardar_semana


@require_permission("programar_turno")
@require_http_methods(["GET", "POST"])
def programacion_semanal(request):
    posted = request.method == "POST"
    parameters = request.POST if posted else request.GET
    scope = SemanaScopeForm(parameters, user=request.user, use_defaults=not posted)
    formset = None
    reason_form = MotivoSemanaForm(request.POST if posted else None, prefix="semana")
    grid = []
    start = end = None
    copying = False
    if scope.is_valid():
        data = scope.cleaned_data
        origin = None
        if not posted and request.GET.get("accion") == "copiar":
            if data.get("copiar_anio") is None or data.get("copiar_semana") is None:
                scope.add_error(None, "Complete el año y la semana de origen para copiar.")
            else:
                origin = (data["copiar_anio"], data["copiar_semana"])
        if not scope.errors:
            try:
                start, initial = cargar_semana(request.user, data["anio"], data["semana"], data["planta"], data["area"], origen=origin)
            except ValidationError as exc:
                scope.add_error(None, " ".join(exc.messages))
            else:
                end = start + timedelta(days=6)
                copying = bool(origin)
                if copying:
                    reason_form = MotivoSemanaForm(prefix="semana", initial={"motivo": "Copia de {0}-W{1:02d} a {2}-W{3:02d}".format(origin[0], origin[1], data["anio"], data["semana"])})
                formset = SemanaFormSet(request.POST if posted else None, initial=initial, prefix="turnos")
                if posted:
                    valid_cells = formset.is_valid()
                    valid_reason = reason_form.is_valid()
                    if valid_cells and valid_reason:
                        try:
                            count = guardar_semana(request.user, data["anio"], data["semana"], data["planta"], data["area"], [f.cleaned_data for f in formset], reason_form.cleaned_data["motivo"])
                        except ValidationError as exc:
                            scope.add_error(None, " ".join(exc.messages))
                        except IntegrityError:
                            scope.add_error(None, "Otro usuario guardó esta semana. Recargue antes de volver a editar.")
                        else:
                            messages.success(request, "Semana guardada. Ya puede ingresar los resultados de los turnos programados al finalizar cada uno." if count else "La semana no tiene cambios. Se conservó la programación existente.")
                            query = urlencode({"anio": data["anio"], "semana": data["semana"], "planta": data["planta"], "area": data["area"].pk})
                            return redirect(reverse("productividad_turnos:programacion_semanal") + "?" + query)
                if len(formset.forms) == 21:
                    for index, name in enumerate(DIAS):
                        cells = []
                        for offset in range(3):
                            pos = index * 3 + offset
                            cells.append({"form": formset.forms[pos], "estado": initial[pos]["_estado"], "turno": initial[pos]["turno"]})
                        grid.append({"dia": name, "fecha": start + timedelta(days=index), "cells": cells})
                else:
                    scope.add_error(None, "Formulario incompleto. Vuelva a cargar la semana. No se guardó ningún cambio.")
    plant_name = dict(scope.fields["planta"].choices).get(scope.data.get("planta"), "")
    return render(request, "productividad_turnos/programacion_semanal.html", base_context(request, scope=scope, formset=formset, motivo_form=reason_form, grid=grid, desde=start, hasta=end, copying=copying, planta_nombre=plant_name))
