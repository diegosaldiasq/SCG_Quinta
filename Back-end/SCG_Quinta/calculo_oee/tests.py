from datetime import time
from decimal import Decimal
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from control_de_pesos.models import ProductoControlPeso
from .models import TurnoOEE, Producto, Detencion, Reproceso, ResumenTurnoOee
from .services import calcular_oee_automatico, evaluar_turno


class CalculoAutomaticoTests(TestCase):
    def setUp(self):
        self.tasa = ProductoControlPeso.objects.create(
            area='TORTAS', cliente='Jumbo', codigo='1', producto='Torta prueba',
            peso_receta=1000, un_pp=Decimal('100'),
        )
        self.lote = TurnoOEE.objects.create(
            fecha=timezone.now(), planta='ENEA', supervisor='Felipe Campos',
            turno='Turno A', linea='Línea 1', lote='123', cliente='Jumbo',
            codigo='1', producto='Torta prueba', numero_personas=2,
            tiempo_planeado=450, produccion_planeada=200, produccion_real=150,
        )
        self.producto = Producto.objects.create(
            lote=self.lote, cliente='Jumbo', codigo='1', producto='Torta prueba',
            produccion_planeada=200, produccion_real=150,
        )
        self.user = get_user_model().objects.create(
            **{get_user_model().USERNAME_FIELD: 'revisor'}, password='test', is_staff=True, is_active=True,
        )
        self.client.force_login(self.user)

    def test_calculo_valido_y_repeticion_sin_duplicados(self):
        Detencion.objects.create(lote=self.lote, motivo='Falla', hora_inicio=time(0), hora_fin=time(1, 30), duracion=90)
        Reproceso.objects.create(lote=self.lote, motivo='Merma', cantidad=15)
        resumen, motivos = calcular_oee_automatico(self.lote.id)
        self.assertEqual(motivos, [])
        self.assertEqual(resumen.disponibilidad, 80)
        self.assertEqual(resumen.eficiencia, 75)
        self.assertEqual(resumen.calidad, 90)
        self.assertEqual(resumen.oee, 54)
        resumen.verificado = True
        resumen.save()
        segundo, _ = calcular_oee_automatico(self.lote.id)
        self.assertEqual(segundo.id, resumen.id)
        self.assertTrue(segundo.verificado)
        self.assertEqual(ResumenTurnoOee.objects.count(), 1)

    def test_datos_inconsistentes_no_crean_resumen(self):
        casos = [
            ('personas', lambda: TurnoOEE.objects.filter(pk=self.lote.pk).update(numero_personas=0)),
            ('tasa', lambda: ProductoControlPeso.objects.filter(pk=self.tasa.pk).update(un_pp=None)),
            ('parcial', lambda: Producto.objects.filter(pk=self.producto.pk).update(produccion_real=None)),
            ('total', lambda: Producto.objects.filter(pk=self.producto.pk).update(produccion_real=149)),
            ('rendimiento', lambda: ProductoControlPeso.objects.filter(pk=self.tasa.pk).update(un_pp=50)),
            ('mermas', lambda: Reproceso.objects.create(lote=self.lote, motivo='Error', cantidad=151)),
            ('detenciones', lambda: Detencion.objects.create(lote=self.lote, motivo='Falla', hora_inicio=time(0), hora_fin=time(8), duracion=480)),
        ]
        for nombre, cambiar in casos:
            with self.subTest(nombre=nombre):
                with self.captureOnCommitCallbacks():
                    # Cada caso se revierte para mantener el escenario base.
                    from django.db import transaction
                    with transaction.atomic():
                        cambiar()
                        resumen, motivos = calcular_oee_automatico(self.lote.pk)
                        self.assertIsNone(resumen)
                        self.assertTrue(motivos)
                        self.assertFalse(ResumenTurnoOee.objects.exists())
                        transaction.set_rollback(True)

    def test_detenciones_superpuestas_y_cruce_medianoche(self):
        Detencion.objects.create(lote=self.lote, motivo='Falla', hora_inicio=time(23, 30), hora_fin=time(0, 30), duracion=60)
        datos, motivos = evaluar_turno(self.lote)
        self.assertEqual(motivos, [])
        self.assertEqual(datos['tiempo_paro'], 60)
        Detencion.objects.create(lote=self.lote, motivo='Duplicada', hora_inicio=time(0), hora_fin=time(1), duracion=60)
        _, motivos = evaluar_turno(self.lote)
        self.assertTrue(any('superpuestos' in m for m in motivos))

    def test_oee_bajo_y_cero_son_validos(self):
        for real in (1, 0):
            self.lote.produccion_real = real
            self.lote.save()
            self.producto.produccion_real = real
            self.producto.save()
            datos, motivos = evaluar_turno(self.lote)
            self.assertEqual(motivos, [])
            self.assertLessEqual(datos['oee'], 1)

    def test_mezcla_de_productos_ponderada(self):
        self.producto.produccion_real = 50
        self.producto.produccion_planeada = 100
        self.producto.save()
        ProductoControlPeso.objects.create(area='TORTAS', cliente='Jumbo', producto='Lenta', codigo='2', peso_receta=1000, un_pp=50)
        Producto.objects.create(lote=self.lote, cliente='Jumbo', producto='Lenta', codigo='2', produccion_planeada=100, produccion_real=50)
        self.lote.produccion_real = 100
        self.lote.save()
        datos, motivos = evaluar_turno(self.lote)
        self.assertEqual(motivos, [])
        self.assertEqual(datos['eficiencia'], 75)
        self.assertEqual(datos['produccion_teorica'], 133)

    @override_settings(OEE_RENDIMIENTO_MAXIMO=120)
    def test_tolerancia_no_permite_oee_mayor_100(self):
        self.tasa.un_pp = 70
        self.tasa.save()
        datos, motivos = evaluar_turno(self.lote)
        self.assertIsNone(datos)
        self.assertTrue(any('OEE' in m for m in motivos))

    def test_cierre_calcula_y_actualiza_producto_unico(self):
        respuesta = self.client.post(reverse('cerrar_turno', args=[self.lote.pk]), {'produccion_real': 160})
        self.assertRedirects(respuesta, reverse('resumen_turno', args=[self.lote.pk]))
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.produccion_real, 160)
        self.assertEqual(ResumenTurnoOee.objects.get().produccion_real, 160)

    def test_cierre_varios_productos_incompletos_va_a_revision(self):
        Producto.objects.create(lote=self.lote, cliente='Jumbo', producto='Torta prueba', codigo='1', produccion_planeada=1)
        respuesta = self.client.post(reverse('cerrar_turno', args=[self.lote.pk]), {'produccion_real': 160})
        self.assertRedirects(respuesta, reverse('revisar_turno_oee', args=[self.lote.pk]))
        self.assertFalse(ResumenTurnoOee.objects.exists())

    def test_procesar_pendientes_post_y_permisos(self):
        url = reverse('procesar_oee_pendientes')
        self.assertEqual(self.client.get(url).status_code, 405)
        self.user.is_staff = False
        self.user.save()
        self.assertEqual(self.client.post(url).status_code, 403)
        self.assertFalse(ResumenTurnoOee.objects.exists())
        self.user.is_staff = True
        self.user.save()
        self.assertEqual(self.client.post(url).status_code, 302)
        self.assertEqual(ResumenTurnoOee.objects.count(), 1)

    def test_comando_y_filtro_compatible(self):
        respuesta = self.client.get(reverse('lista_turnos'), {'estado': 'calcular_oee'})
        self.assertContains(respuesta, 'Pendiente de cálculo automático')
        self.assertFalse(ResumenTurnoOee.objects.exists())
        call_command('procesar_oee_pendientes', stdout=StringIO())
        respuesta = self.client.get(reverse('lista_turnos'), {'estado': 'revision_oee'})
        self.assertEqual(len(respuesta.context['turnos']), 0)

    def test_pantalla_revision_y_guardado(self):
        url = reverse('revisar_turno_oee', args=[self.lote.pk])
        self.assertContains(self.client.get(url), 'Guardar correcciones')
        datos = {
            'supervisor': 'Felipe Campos', 'numero_personas': 2, 'tiempo_planeado': 450,
            'produccion_planeada': 200, 'produccion_real': 150, 'cliente': 'Jumbo',
            'producto': 'Torta prueba', 'codigo': '1',
            'productos-TOTAL_FORMS': 1, 'productos-INITIAL_FORMS': 1,
            'productos-0-id': self.producto.id, 'productos-0-lote': self.lote.id,
            'productos-0-cliente': 'Jumbo', 'productos-0-producto': 'Torta prueba',
            'productos-0-codigo': '1', 'productos-0-produccion_planeada': 200,
            'productos-0-produccion_real': 150,
            'detenciones-TOTAL_FORMS': 1, 'detenciones-INITIAL_FORMS': 0,
            'reprocesos-TOTAL_FORMS': 1, 'reprocesos-INITIAL_FORMS': 0,
            'next': 'https://example.com',
        }
        self.assertRedirects(self.client.post(url, datos), reverse('lista_turnos'))
        self.assertEqual(ResumenTurnoOee.objects.count(), 1)

    def test_crear_turno_calcula_despues_de_detenciones(self):
        datos = {
            'fecha': '2026-10-09', 'linea': 'Línea 1', 'turno': 'Turno A',
            'numero_personas': 2, 'lote': 'nuevo', 'supervisor': 'Felipe Campos',
            'tiempo_planeado': 450,
            'cliente_producto[]': ['Jumbo'], 'producto[]': ['Torta prueba'],
            'codigo[]': ['1'], 'produccion_planeada[]': ['200'],
            'produccion_real[]': ['150'], 'comentarios_producto[]': [''],
            'motivo_det[]': ['Falla'], 'hora_inicio_det[]': ['00:00'],
            'hora_fin_det[]': ['01:30'], 'comentarios_det[]': [''],
        }
        respuesta = self.client.post(reverse('crear_turno'), datos)
        self.assertEqual(respuesta.status_code, 302)
        resumen = ResumenTurnoOee.objects.get(lote__lote='nuevo')
        self.assertEqual(resumen.oee, 60)
        self.assertEqual(resumen.tiempo_paro, 90)

    def test_crear_incompleto_no_guarda_y_cierre_historico_no_modifica(self):
        datos = {
            'fecha': '2026-10-09', 'linea': 'Línea 1', 'turno': 'Turno A',
            'numero_personas': 2, 'lote': 'nuevo', 'supervisor': 'Felipe Campos',
            'tiempo_planeado': 450, 'producto[]': ['Torta prueba'],
        }
        respuesta = self.client.post(reverse('crear_turno'), datos)
        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(TurnoOEE.objects.filter(lote='nuevo').exists())
        calcular_oee_automatico(self.lote.id)
        self.client.post(reverse('cerrar_turno', args=[self.lote.pk]), {'produccion_real': 999})
        self.lote.refresh_from_db()
        self.assertEqual(self.lote.produccion_real, 150)

    def test_revision_sin_permisos_y_csrf(self):
        from django.test import Client
        cliente = Client(enforce_csrf_checks=True)
        cliente.force_login(self.user)
        self.assertEqual(cliente.post(reverse('procesar_oee_pendientes')).status_code, 403)
        self.assertFalse(ResumenTurnoOee.objects.exists())
        self.user.is_staff = False
        self.user.save()
        url = reverse('revisar_turno_oee', args=[self.lote.pk])
        self.assertContains(self.client.get(url), 'Solicita a administración')
        self.assertEqual(self.client.post(url, {}).status_code, 403)
