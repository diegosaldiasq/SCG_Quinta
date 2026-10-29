from datetime import timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseFormSet, formset_factory
from django.utils import timezone

from .forms import allowed_areas, allowed_plants
from .models import AsignacionProductividad
from .weekly_services import PARES, lunes_iso


class SemanaScopeForm(forms.Form):
    anio = forms.IntegerField(label="Año ISO", min_value=2000, max_value=2100)
    semana = forms.IntegerField(label="Semana ISO", min_value=1, max_value=53)
    planta = forms.ChoiceField(label="Planta")
    area = forms.ModelChoiceField(label="Área", queryset=None)
    copiar_anio = forms.IntegerField(label="Año de origen", min_value=1999, max_value=2100, required=False)
    copiar_semana = forms.IntegerField(label="Semana de origen", min_value=1, max_value=53, required=False)

    def __init__(self, data=None, *, user, use_defaults=True, **kwargs):
        self.user = user
        areas = allowed_areas(user)
        default_area = areas.filter(codigo="TORTAS").first() or areas.first()
        plants = allowed_plants(user)
        default_plant = plants[0][0] if plants else ""
        if default_area and not user.is_superuser:
            assignment = AsignacionProductividad.objects.filter(usuario=user, area=default_area).first()
            if assignment:
                default_plant = assignment.planta
        year, week, _ = timezone.localdate().isocalendar()
        defaults = {"anio": year, "semana": week, "planta": default_plant, "area": default_area.pk if default_area else ""}
        if use_defaults:
            values = dict(defaults)
            if data:
                values.update({k: data.get(k) for k in self.base_fields if k in data and not (data.get("accion") == "cargar" and k.startswith("copiar_"))})
            try:
                previous = lunes_iso(values["anio"], values["semana"]) - timedelta(days=7)
                old_year, old_week, _ = previous.isocalendar()
                values.setdefault("copiar_anio", old_year)
                values.setdefault("copiar_semana", old_week)
            except ValidationError:
                pass
            data = values
        super().__init__(data=data, **kwargs)
        self.fields["area"].queryset = areas
        self.fields["planta"].choices = plants

    def clean(self):
        data = super().clean()
        if "anio" in data and "semana" in data:
            data["lunes"] = lunes_iso(data["anio"], data["semana"])
        if "area" in data and "planta" in data and not self.user.is_superuser:
            if not AsignacionProductividad.objects.filter(usuario=self.user, planta=data["planta"], area=data["area"]).exists():
                raise ValidationError("No tiene asignación para esta combinación de planta y área.")
        return data


class CeldaSemanaForm(forms.Form):
    dia = forms.IntegerField(min_value=1, max_value=7, widget=forms.HiddenInput)
    turno = forms.ChoiceField(choices=[(t, t) for t in "ABC"], widget=forms.HiddenInput)
    programacion_id = forms.IntegerField(min_value=0, widget=forms.HiddenInput)
    version = forms.IntegerField(min_value=0, widget=forms.HiddenInput)
    registro_version = forms.IntegerField(min_value=0, widget=forms.HiddenInput)
    programado = forms.BooleanField(label="Programado", required=False)
    meta_pt = forms.IntegerField(label="Meta PT", min_value=0, max_value=2147483647, required=False, widget=forms.NumberInput(attrs={"placeholder": "Meta PT", "inputmode": "numeric"}))
    extraordinario = forms.BooleanField(label="Extraordinario", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.locked = bool(self.initial.get("_locked"))
        if self.locked:
            for name in ("programado", "meta_pt", "extraordinario"):
                self.fields[name].disabled = True

    def clean(self):
        data = super().clean()
        if data.get("programado") and data.get("meta_pt") is None:
            self.add_error("meta_pt", "Ingrese la meta del turno programado.")
        return data


class SemanaBaseFormSet(BaseFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        pairs = [(form.cleaned_data.get("dia"), form.cleaned_data.get("turno")) for form in self.forms]
        if pairs != list(PARES):
            raise ValidationError("La cuadrícula fue modificada o está incompleta. Recargue la semana.")


SemanaFormSet = formset_factory(CeldaSemanaForm, formset=SemanaBaseFormSet, extra=0, min_num=21, max_num=21, validate_min=True, validate_max=True, absolute_max=21)


class MotivoSemanaForm(forms.Form):
    motivo = forms.CharField(label="Motivo / observación de la programación semanal", max_length=2500, widget=forms.Textarea(attrs={"rows": 2, "placeholder": "Ej.: Programación semana 45; sábado solo A y B."}))
