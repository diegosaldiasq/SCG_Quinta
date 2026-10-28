from datetime import date
from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import AreaProductividad, AsignacionProductividad, PLANTAS, TURNOS


def allowed_areas(user, active_only=True):
    qs = AreaProductividad.objects.all()
    if active_only:
        qs = qs.filter(activo=True)
    if not user.is_superuser:
        qs = qs.filter(pk__in=AsignacionProductividad.objects.filter(usuario=user).values("area_id"))
    return qs


def allowed_plants(user):
    assigned = set(AsignacionProductividad.objects.filter(usuario=user).values_list("planta", flat=True))
    return PLANTAS if user.is_superuser else [p for p in PLANTAS if p[0] in assigned]


class RegistroForm(forms.Form):
    version = forms.IntegerField(min_value=0, widget=forms.HiddenInput)
    dotacion = forms.IntegerField(label="Dotación presente", min_value=1, required=False)
    semielaborados = forms.IntegerField(label="Semielaborados", min_value=0, required=False)
    terminadas = forms.IntegerField(label="Tortas terminadas", min_value=0, required=False)
    horas_persona = forms.DecimalField(label="Horas-persona (opcional)", min_value=Decimal("0.01"), max_digits=12, decimal_places=2, required=False)
    observaciones = forms.CharField(label="Observaciones", required=False, max_length=5000, widget=forms.Textarea(attrs={"rows": 3}))
    confirmar_ceros = forms.BooleanField(label="Confirmo que los valores cero corresponden a producción cero real.", required=False)

    def __init__(self, *args, area, **kwargs):
        super().__init__(*args, **kwargs)
        if not area.mide_semielaborado:
            self.fields.pop("semielaborados")


class ProgramacionForm(forms.Form):
    version = forms.IntegerField(min_value=0, initial=0, widget=forms.HiddenInput)
    fecha_operativa = forms.DateField(label="Fecha operativa", widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"))
    planta = forms.ChoiceField(choices=PLANTAS)
    area = forms.ModelChoiceField(queryset=AreaProductividad.objects.none(), label="Área")
    turno = forms.ChoiceField(choices=TURNOS)
    meta_pt = forms.IntegerField(label="Meta PT", min_value=0)
    programado = forms.BooleanField(label="Turno programado", required=False, initial=True)
    extraordinario = forms.BooleanField(label="Turno extraordinario", required=False)
    motivo = forms.CharField(label="Motivo / observación de programación", required=False, max_length=3000, widget=forms.Textarea(attrs={"rows": 2}))

    def __init__(self, *args, user, editing=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["area"].queryset = allowed_areas(user)
        self.fields["planta"].choices = allowed_plants(user)
        if editing:
            for name in ("fecha_operativa", "planta", "area", "turno"):
                self.fields[name].disabled = True


class FiltroForm(forms.Form):
    fecha = forms.DateField(label="Fecha operativa", widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"))
    anio = forms.IntegerField(label="Año ISO", min_value=2000, max_value=2100)
    semana = forms.IntegerField(label="Semana ISO", min_value=1, max_value=53)
    planta = forms.ChoiceField(required=False)
    area = forms.ModelChoiceField(queryset=AreaProductividad.objects.none(), label="Área")
    turnos = forms.MultipleChoiceField(choices=TURNOS, widget=forms.CheckboxSelectMultiple, required=True)

    def __init__(self, data, *, user, periodo="dia", **kwargs):
        self.periodo = periodo
        areas = allowed_areas(user, active_only=False)
        default_area = areas.filter(codigo="TORTAS").first() or areas.first()
        today = timezone.localdate()
        iso_year, iso_week, _ = today.isocalendar()

        defaults = {
            "fecha": today.isoformat(),
            "anio": iso_year,
            "semana": iso_week,
            "area": default_area.pk if default_area else "",
            "planta": "",
            "turnos": ["A", "B", "C"],
        }
        # QueryDict mantiene selecciones múltiples y distingue una selección vacía.
        from django.http import QueryDict
        bound = QueryDict(mutable=True)
        for k, value in defaults.items():
            bound.setlist(k, value if isinstance(value, list) else [str(value)])
        if data:
            for k in data:
                bound.setlist(k, data.getlist(k) if hasattr(data, "getlist") else ([data[k]] if not isinstance(data[k], list) else data[k]))
            if "filtrar" in data and "turnos" not in data:
                bound.setlist("turnos", [])
        super().__init__(bound, **kwargs)
        self.fields["area"].queryset = areas
        self.fields["planta"].choices = [("", "Todas las plantas autorizadas")] + allowed_plants(user)

    def clean(self):
        data = super().clean()
        if self.periodo == "semana" and "anio" in data and "semana" in data:
            try:
                date.fromisocalendar(data["anio"], data["semana"], 1)
            except ValueError:
                raise ValidationError("Esa semana no existe en el año ISO seleccionado.")
        return data


class AccionForm(forms.Form):
    version = forms.IntegerField(min_value=1, widget=forms.HiddenInput)
    motivo = forms.CharField(required=False, max_length=3000, widget=forms.Textarea(attrs={"rows": 2}))
