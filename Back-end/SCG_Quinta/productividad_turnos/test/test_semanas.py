from datetime import date, datetime
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied, ValidationError
from django.test import Client, TestCase
from django.urls import reverse

from productividad_turnos.models import AreaProductividad, AsignacionProductividad, ProgramacionTurno, RegistroProductividadTurno, RevisionProductividad
from productividad_turnos.selectors import summarize
from productividad_turnos.services import ZoneInfo, guardar_registro, programar
from productividad_turnos.weekly_forms import SemanaScopeForm
from productividad_turnos.weekly_services import PARES, cargar_semana, guardar_semana


class SemanaTests(TestCase):
    def setUp(self):
        clock = patch("django.utils.timezone.now", return_value=datetime(2026, 10, 29, 12, tzinfo=ZoneInfo("America/Santiago")))
        clock.start()
        self.addCleanup(clock.stop)
        self.area = AreaProductividad.objects.get(codigo="TORTAS")
        User = get_user_model()
        if User.USERNAME_FIELD == "nombre_completo":
            self.user = User.objects.create_user(nombre_completo="Planificador semanal", perfil_usuario="Supervisor", rut="12345678-9", password="test")
        else:
            self.user = User.objects.create_user(username="planificador", password="test")
        self.user.is_active = True
        self.user.save()
        self.user.user_permissions.add(*Permission.objects.filter(content_type__app_label="productividad_turnos"))
        AsignacionProductividad.objects.create(usuario=self.user, planta="ENEA", area=self.area)
        self.client.force_login(self.user)
        self.url = reverse("productividad_turnos:programacion_semanal")

    def context_data(self, week=44, year=2026):
        return {"anio": year, "semana": week, "planta": "ENEA", "area": self.area.pk}

    def load(self, week=44, year=2026, origin=None):
        return cargar_semana(self.user, year, week, "ENEA", self.area, origen=origin)[1]

    def configured_rows(self, week=44, year=2026):
        rows = self.load(week, year)
        for index, meta in [(0, 3800), (1, 5700), (3, 4000), (17, 2200)]:
            rows[index].update(programado=True, meta_pt=meta)
        rows[17]["extraordinario"] = True
        return rows

    def save(self, rows, week=44, year=2026, reason="Programación acordada"):
        return guardar_semana(self.user, year, week, "ENEA", self.area, rows, reason)

    def payload(self, rows=None, week=44, year=2026):
        rows = rows if rows is not None else self.configured_rows(week, year)
        result = self.context_data(week, year)
        result.update({"turnos-TOTAL_FORMS": "21", "turnos-INITIAL_FORMS": "21", "turnos-MIN_NUM_FORMS": "21", "turnos-MAX_NUM_FORMS": "21", "semana-motivo": "Programación semanal de prueba"})
        for i, row in enumerate(rows):
            for key in ("dia", "turno", "programacion_id", "version", "registro_version"):
                result["turnos-{0}-{1}".format(i, key)] = str(row[key])
            if row["programado"]:
                result["turnos-{0}-programado".format(i)] = "on"
            if row["extraordinario"]:
                result["turnos-{0}-extraordinario".format(i)] = "on"
            result["turnos-{0}-meta_pt".format(i)] = "" if row["meta_pt"] is None else str(row["meta_pt"])
        return result

    def close(self, plan):
        return guardar_registro(self.user, plan.pk, {"dotacion": 50, "terminadas": 3500, "semielaborados": 2000, "horas_persona": None, "observaciones": "Ejemplo", "confirmar_ceros": False}, 0, cerrar=True)

    def test_get_empty_week_is_read_only_and_has_twenty_one_cells(self):
        response = self.client.get(self.url, self.context_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["formset"].forms), 21)
        self.assertEqual(len(response.context["grid"]), 7)
        self.assertContains(response, "Guardar semana")
        self.assertEqual(ProgramacionTurno.objects.count(), 0)

    def test_full_week_different_targets_and_unprogrammed_slots(self):
        rows = self.configured_rows()
        self.assertEqual(self.save(rows), 21)
        self.assertEqual(ProgramacionTurno.objects.count(), 21)
        self.assertEqual(ProgramacionTurno.objects.filter(programado=True).count(), 4)
        self.assertEqual(ProgramacionTurno.objects.get(fecha_operativa=date(2026, 10, 26), turno="A").meta_pt, 3800)
        self.assertEqual(ProgramacionTurno.objects.get(fecha_operativa=date(2026, 10, 27), turno="A").meta_pt, 4000)
        saturday = ProgramacionTurno.objects.get(fecha_operativa=date(2026, 10, 31), turno="C")
        self.assertTrue(saturday.extraordinario)
        sunday = ProgramacionTurno.objects.get(fecha_operativa=date(2026, 11, 1), turno="C")
        self.assertFalse(sunday.programado)
        self.assertEqual(sunday.meta_pt, 0)
        self.assertEqual(RegistroProductividadTurno.objects.count(), 0)

    def test_week_is_independent_from_other_weeks(self):
        self.save(self.configured_rows(43), week=43)
        self.save(self.configured_rows(44), week=44)
        rows = self.load(44)
        rows[0]["meta_pt"] = 4200
        self.save(rows)
        self.assertEqual(ProgramacionTurno.objects.get(fecha_operativa=date(2026, 10, 19), turno="A").meta_pt, 3800)
        self.assertEqual(ProgramacionTurno.objects.get(fecha_operativa=date(2026, 10, 26), turno="A").meta_pt, 4200)

    def test_copy_is_preview_only_and_shifts_dates(self):
        self.save(self.configured_rows(43), week=43)
        rows = self.load(44, origin=(2026, 43))
        self.assertEqual(ProgramacionTurno.objects.count(), 21)
        self.assertEqual(rows[0]["meta_pt"], 3800)
        self.assertEqual(rows[0]["programacion_id"], 0)
        self.save(rows)
        self.assertEqual(ProgramacionTurno.objects.count(), 42)
        self.assertEqual(ProgramacionTurno.objects.filter(fecha_operativa=date(2026, 10, 26), turno="A").count(), 1)

    def test_closed_destination_keeps_target_during_copy(self):
        self.save(self.configured_rows(43), week=43)
        self.save(self.configured_rows(44), week=44)
        destination = ProgramacionTurno.objects.get(fecha_operativa=date(2026, 10, 26), turno="A")
        record = self.close(destination)
        source = ProgramacionTurno.objects.get(fecha_operativa=date(2026, 10, 19), turno="A")
        source.meta_pt = 9999
        source.save()
        rows = self.load(44, origin=(2026, 43))
        self.assertEqual(rows[0]["meta_pt"], 3800)
        self.assertTrue(rows[0]["_locked"])
        self.save(rows)
        record.refresh_from_db()
        self.assertEqual(record.terminadas, 3500)
        self.assertEqual(record.meta_pt_cierre, 3800)

    def test_copy_never_duplicates_production(self):
        self.save(self.configured_rows(43), week=43)
        self.close(ProgramacionTurno.objects.get(fecha_operativa=date(2026, 10, 19), turno="A"))
        rows = self.load(44, origin=(2026, 43))
        self.save(rows)
        self.assertEqual(RegistroProductividadTurno.objects.count(), 1)
        self.assertFalse(RegistroProductividadTurno.objects.filter(programacion__fecha_operativa__gte=date(2026, 10, 26)).exists())

    def test_closed_change_rejected_and_everything_rolled_back(self):
        self.save(self.configured_rows())
        p = ProgramacionTurno.objects.get(fecha_operativa=date(2026, 10, 26), turno="B")
        self.close(p)
        rows = self.load()
        rows[0]["meta_pt"], rows[1]["meta_pt"] = 1234, 9999
        audits = RevisionProductividad.objects.count()
        with self.assertRaises(ValidationError):
            self.save(rows)
        self.assertEqual(ProgramacionTurno.objects.get(fecha_operativa=date(2026, 10, 26), turno="A").meta_pt, 3800)
        self.assertEqual(RevisionProductividad.objects.count(), audits)

    def test_stale_plan_version_is_rejected(self):
        self.save(self.configured_rows())
        old = self.load()
        new = self.load()
        new[0]["meta_pt"] = 4200
        self.save(new)
        with self.assertRaises(ValidationError):
            self.save(old)

    def test_production_changed_while_editing_is_rejected(self):
        self.save(self.configured_rows())
        old = self.load()
        p = ProgramacionTurno.objects.get(fecha_operativa=date(2026, 10, 26), turno="A")
        self.close(p)
        with self.assertRaises(ValidationError):
            self.save(old)

    def test_concurrent_creation_snapshot_is_rejected(self):
        first = self.configured_rows()
        stale = self.configured_rows()
        self.save(first)
        with self.assertRaises(ValidationError):
            self.save(stale)
        self.assertEqual(ProgramacionTurno.objects.count(), 21)

    def test_repeated_save_does_not_duplicate_or_create_audit_noise(self):
        self.save(self.configured_rows())
        audits = RevisionProductividad.objects.count()
        self.assertEqual(self.save(self.load()), 0)
        self.assertEqual(ProgramacionTurno.objects.count(), 21)
        self.assertEqual(RevisionProductividad.objects.count(), audits)

    def test_negative_or_missing_target_does_not_save(self):
        rows = self.configured_rows()
        rows[-1].update(programado=True, meta_pt=-1)
        with self.assertRaises(ValidationError):
            self.save(rows)
        self.assertEqual(ProgramacionTurno.objects.count(), 0)
        rows[-1]["meta_pt"] = None
        with self.assertRaises(ValidationError):
            self.save(rows)

    def test_nested_service_failure_rolls_back_all_rows(self):
        calls = [0]
        def sometimes_fails(*args, **kwargs):
            calls[0] += 1
            if calls[0] == 3:
                raise ValidationError("Simulación de fallo")
            return programar(*args, **kwargs)
        with patch("productividad_turnos.weekly_services.programar", side_effect=sometimes_fails):
            with self.assertRaises(ValidationError):
                self.save(self.configured_rows())
        self.assertEqual(ProgramacionTurno.objects.count(), 0)
        self.assertEqual(RevisionProductividad.objects.count(), 0)

    def test_iso_boundary_and_invalid_week(self):
        form = SemanaScopeForm(self.context_data(53, 2025), user=self.user)
        self.assertFalse(form.is_valid())
        rows = self.configured_rows(53, 2026)
        self.save(rows, week=53)
        copied = self.load(1, 2027, origin=(2026, 53))
        self.save(copied, week=1, year=2027)
        self.assertEqual(ProgramacionTurno.objects.get(fecha_operativa=date(2027, 1, 4), turno="A").meta_pt, 3800)

    def test_source_missing_or_same_week_is_rejected(self):
        with self.assertRaises(ValidationError):
            self.load(44, origin=(2026, 44))
        with self.assertRaises(ValidationError):
            self.load(44, origin=(2026, 43))

    def test_form_post_saves_and_reloads_matrix(self):
        response = self.client.post(self.url, self.payload())
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Semana guardada")
        self.assertEqual(ProgramacionTurno.objects.count(), 21)
        self.assertEqual(response.context["formset"].initial[3]["meta_pt"], 4000)

    def test_get_copy_does_not_write_and_post_does(self):
        self.save(self.configured_rows(43), week=43)
        query = self.context_data()
        query.update(accion="copiar", copiar_anio=2026, copiar_semana=43)
        response = self.client.get(self.url, query)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Copia en previsualización")
        self.assertEqual(ProgramacionTurno.objects.count(), 21)
        rows = response.context["formset"].initial
        self.assertEqual(self.client.post(self.url, self.payload(rows)).status_code, 302)
        self.assertEqual(ProgramacionTurno.objects.count(), 42)

    def test_missing_management_or_tampered_cell_does_not_crash(self):
        data = self.payload()
        data.pop("turnos-TOTAL_FORMS")
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ProgramacionTurno.objects.count(), 0)
        data = self.payload()
        data["turnos-1-dia"] = "7"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cuadrícula")
        self.assertEqual(ProgramacionTurno.objects.count(), 0)

    def test_active_empty_target_and_missing_reason_have_errors(self):
        data = self.payload()
        data["turnos-0-meta_pt"] = ""
        self.assertContains(self.client.post(self.url, data), "Ingrese la meta")
        data = self.payload()
        data["semana-motivo"] = ""
        self.assertEqual(self.client.post(self.url, data).status_code, 200)
        self.assertEqual(ProgramacionTurno.objects.count(), 0)

    def test_locked_form_ignores_submitted_meta_change(self):
        self.save(self.configured_rows())
        p = ProgramacionTurno.objects.get(fecha_operativa=date(2026, 10, 26), turno="A")
        self.close(p)
        data = self.payload(self.load())
        data["turnos-0-meta_pt"] = "9999"
        self.assertEqual(self.client.post(self.url, data).status_code, 302)
        p.refresh_from_db()
        self.assertEqual(p.meta_pt, 3800)

    def test_permissions_scope_and_pair_are_enforced(self):
        with self.assertRaises(PermissionDenied):
            cargar_semana(self.user, 2026, 44, "PUERTO_VESPUCIO", self.area)
        data = self.context_data()
        data["planta"] = "PUERTO_VESPUCIO"
        response = self.client.get(self.url, data)
        self.assertIsNone(response.context["formset"])
        self.user.user_permissions.clear()
        self.assertEqual(self.client.get(self.url).status_code, 403)

    def test_csrf_and_post_scope_are_required(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        self.assertEqual(client.post(self.url, self.payload()).status_code, 403)
        data = self.payload()
        data.pop("anio")
        self.assertEqual(self.client.post(self.url, data).status_code, 200)
        self.assertEqual(ProgramacionTurno.objects.count(), 0)

    def test_panels_receive_the_same_plans_and_exclude_off_slots(self):
        self.save(self.configured_rows(43), week=43)
        p = ProgramacionTurno.objects.get(fecha_operativa=date(2026, 10, 19), turno="A")
        self.close(p)
        result = summarize(ProgramacionTurno.objects.all(), date(2026, 10, 19), date(2026, 10, 25), "semana")
        self.assertEqual(result["meta_programada"], 15700)
        self.assertEqual(result["vencidos"], 4)
        self.assertEqual(result["recibidos"], 1)
        self.assertEqual(result["total"]["terminadas"], 3500)
        self.assertEqual(result["total"]["meta"], 3800)

    def test_invalid_ids_and_duplicate_pairs_are_rejected(self):
        rows = self.configured_rows()
        rows[0]["programacion_id"] = 9999
        with self.assertRaises(ValidationError):
            self.save(rows)
        rows = self.configured_rows()
        rows[1]["turno"] = "A"
        with self.assertRaises(ValidationError):
            self.save(rows)

    def test_menu_has_weekly_and_existing_individual_page_still_works(self):
        response = self.client.get(reverse("productividad_turnos:programacion"))
        self.assertContains(response, self.url)
        self.assertContains(response, "Programar semana completa")
