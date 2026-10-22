import json
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase, override_settings

from .models import DatosFormularioHigieneConductaPersonal
from .views import higiene_y_conducta_personal, vista_higiene_y_conducta_personal


@override_settings(ROOT_URLCONF='higiene_y_conducta_personal.urls')
class RegistroHigieneTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.usuario = SimpleNamespace(is_authenticated=True, nombre_completo='Tecnólogo de prueba')
        self.dato = {
            'nombre_personal': 'Colaborador Uno',
            'turno': 'Turno A',
            'planta': 'enea',
            'area': 'Cremas',
            'cumplimiento': 'No cumple',
            'desviacion': 'Uniforme sucio',
            'accion_correctiva': 'Limpar lavar uniforme',
            'verificacion_accion_correctiva': 'Cumple',
            'observacion': 'Se cambió el uniforme',
        }

    def enviar(self, contenido):
        request = self.factory.post('/registro/', json.dumps(contenido), content_type='application/json')
        request.user = self.usuario
        return vista_higiene_y_conducta_personal(request)

    def test_guarda_todas_las_variables_de_cada_fila(self):
        segundo = {
            'nombre_personal': 'Colaborador Dos', 'turno': 'Turno C', 'planta': 'pv',
            'area': 'Masas', 'cumplimiento': 'Cumple', 'desviacion': 'blanco',
            'accion_correctiva': 'blanco', 'verificacion_accion_correctiva': 'No aplica',
            'observacion': 'Sin desviaciones',
        }
        response = self.enviar({'datos': [self.dato, segundo]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'existe': True, 'guardados': 2})
        registros = list(DatosFormularioHigieneConductaPersonal.objects.order_by('pk'))
        for registro, esperado in zip(registros, [self.dato, segundo]):
            for campo, valor in esperado.items():
                self.assertEqual(getattr(registro, campo), valor)
            self.assertEqual(registro.nombre_tecnologo, self.usuario.nombre_completo)
            self.assertFalse(registro.verificado)
        self.assertEqual(registros[0].fecha_ingreso, registros[1].fecha_ingreso)

    def test_fila_invalida_no_guarda_parcialmente(self):
        for campo in ('nombre_personal', 'turno', 'planta', 'area', 'cumplimiento'):
            with self.subTest(campo=campo):
                segundo = dict(self.dato, **{campo: ' '})
                response = self.enviar({'datos': [self.dato, segundo]})
                self.assertEqual(response.status_code, 400)
                self.assertIn('Fila 2', json.loads(response.content)['error'])
                self.assertFalse(DatosFormularioHigieneConductaPersonal.objects.exists())

    def test_valida_estructura_tipos_y_largo(self):
        for contenido in (
            [], {}, {'datos': []}, {'datos': {}}, {'datos': [None]},
            {'datos': [dict(self.dato, observacion=[])]},
            {'datos': [dict(self.dato, nombre_personal='x' * 101)]},
            {'datos': [dict(self.dato, planta='blanco')]},
        ):
            with self.subTest(contenido=contenido):
                self.assertEqual(self.enviar(contenido).status_code, 400)
        self.assertFalse(DatosFormularioHigieneConductaPersonal.objects.exists())

    def test_permite_campos_opcionales_vacios(self):
        dato = {campo: valor for campo, valor in self.dato.items() if campo in (
            'nombre_personal', 'turno', 'planta', 'area', 'cumplimiento',
        )}
        self.assertEqual(self.enviar({'datos': [dato]}).status_code, 200)
        self.assertEqual(DatosFormularioHigieneConductaPersonal.objects.get().observacion, '')

    def test_acepta_el_envio_individual_anterior(self):
        response = self.enviar({'dato': self.dato})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DatosFormularioHigieneConductaPersonal.objects.count(), 1)

    def test_revierte_el_lote_si_falla_la_segunda_escritura(self):
        crear = DatosFormularioHigieneConductaPersonal.objects.create
        llamadas = 0

        def crear_con_fallo(**kwargs):
            nonlocal llamadas
            llamadas += 1
            if llamadas == 2:
                raise RuntimeError('fallo simulado')
            return crear(**kwargs)

        with patch.object(DatosFormularioHigieneConductaPersonal.objects, 'create', side_effect=crear_con_fallo):
            with self.assertRaises(RuntimeError):
                self.enviar({'datos': [self.dato, self.dato]})
        self.assertFalse(DatosFormularioHigieneConductaPersonal.objects.exists())

    def test_rechaza_json_invalido_y_get(self):
        for body in ('{', b'\xff'):
            request = self.factory.post('/registro/', body, content_type='application/json')
            request.user = self.usuario
            self.assertEqual(vista_higiene_y_conducta_personal(request).status_code, 400)
        request = self.factory.get('/registro/')
        request.user = self.usuario
        self.assertEqual(vista_higiene_y_conducta_personal(request).status_code, 405)

    def test_requiere_autenticacion(self):
        request = self.factory.post('/registro/', '{}', content_type='application/json')
        request.user = AnonymousUser()
        self.assertEqual(vista_higiene_y_conducta_personal(request).status_code, 302)
        self.assertFalse(DatosFormularioHigieneConductaPersonal.objects.exists())

    def test_renderiza_formulario_horizontal(self):
        request = self.factory.get('/')
        request.user = self.usuario
        response = higiene_y_conducta_personal(request)
        self.assertContains(response, 'tbody-registros')
        self.assertContains(response, '+ Agregar registro')
        self.assertContains(response, 'data-campo=', count=9)