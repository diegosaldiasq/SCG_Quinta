from django.shortcuts import render
from django.http import HttpResponse
import csv
from openpyxl import Workbook
import pytz
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from historial_termometro.models import DatosFormularioHistorialTermometro
from monitoreo_del_agua.models import DatosFormularioMonitoreoDelAgua
from higiene_y_conducta_personal.models import DatosFormularioHigieneConductaPersonal
from monitoreo_de_plagas.models import DatosFormularioMonitoreoDePlagas
from recepcion_mpme.models import DatosFormularioRecepcionMpMe
from pcc2_detector_metales.models import DatosFormularioPcc2DetectorMetales
from control_de_transporte.models import DatosFormularioControlDeTransporte
from temperatura_despacho_ptjumbo.models import DatosFormularioTemperaturaDespachoJumbo
from temperatura_despacho_ptsisa.models import DatosFormularioTemperaturaDespachoSisa
from reclamo_a_proveedores.models import DatosFormularioReclamoProveedores
from rechazo_mp_in_me.models import DatosFormularioRechazoMpInMe
from informe_de_incidentes.models import DatosFormularioInformeDeIncidentes
from control_material_extraño.models import DatosFormularioControlMaterialExtraño
from login.models import DatosFormularioCrearCuenta
import json
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
from django.db.models.fields import Field
from django.apps import apps


# Create your views here.

@login_required
def index(request):
    #return HttpResponse("Hello World!!")
    return render(request, 'inicio/index.html')

@login_required
def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)

@login_required
def permisos_faltante(request):
    return render(request, 'inicio/falta_permiso.html') 

@login_required
def redireccionar_main(request):
    url_main = reverse('main')
    return HttpResponseRedirect(url_main)

@login_required
def descargas(request):
    return render(request, 'inicio/descargas.html')

@login_required
def set_fechas(request):
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fechainicio')
        fecha_fin = request.POST.get('fechafin')
        if fecha_inicio == '' or fecha_fin == '':
            return JsonResponse({'success': False})
        request.session['fechainicio'] = fecha_inicio
        request.session['fechafin'] = fecha_fin
        return JsonResponse({'success': True})
    
@login_required
def no_hay_datos(request):
    return render(request, 'inicio/no_hay_datos.html')

@login_required
def permisos(request):
    if request.user.is_staff or request.user.is_superuser:
        usuarios = DatosFormularioCrearCuenta.objects.all()
        return render(request, 'inicio/permisos.html', {'usuarios': usuarios})
    else:
        return render(request, 'inicio/falta_permiso.html')

@login_required
def vista_permisos(request):
    try:
        # ... (tu código existente)
        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            datos = body_data.get('userData')

            for dato in datos:
                nombre = dato['name']
                es_activo = dato['isActive']
                es_jefatura = dato['isStaff']

                usuario = DatosFormularioCrearCuenta.objects.get(nombre_completo=nombre)
                usuario.is_active = es_activo
                usuario.is_staff = es_jefatura
                usuario.save()
            return JsonResponse({'existe': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required    
def intermedio(request):
    return render(request, 'inicio/intermedio.html')

@login_required
def seleccion_verifica(request):
    return render(request, 'inicio/seleccion_verifica.html')

@login_required
def verificar(request):
    config = request.GET['config']
    request.session['config'] = config
    model_mapping = {
        'monitoreo_del_agua': 'DatosFormularioMonitoreoDelAgua',
        'higiene_y_conducta_personal': 'DatosFormularioHigieneConductaPersonal',
        'monitoreo_de_plagas': 'DatosFormularioMonitoreoDePlagas',
        'recepcion_mpme': 'DatosFormularioRecepcionMpMe',
        'pcc2_detector_metales': 'DatosFormularioPcc2DetectorMetales',
        'control_de_transporte': 'DatosFormularioControlDeTransporte',
        'temperatura_despacho_ptjumbo': 'DatosFormularioTemperaturaDespachoJumbo',
        'temperatura_despacho_ptsisa': 'DatosFormularioTemperaturaDespachoSisa',
        'historial_termometro': 'DatosFormularioHistorialTermometro',
        'reclamo_a_proveedores': 'DatosFormularioReclamoProveedores',
        'rechazo_mp_in_me': 'DatosFormularioRechazoMpInMe',
        'informe_de_incidentes': 'DatosFormularioInformeDeIncidentes',
        'control_material_extraño': 'DatosFormularioControlMaterialExtraño'
    }
    # Función de ayuda para obtener nombres de campos
    def get_field_names(model):
        fields = model._meta.get_fields()
        return [
            field.name for field in fields 
            if isinstance(field, Field) and 
            field.name not in ['fecha_de_verificacion', 'verificado_por']
        ]
    # Obtener el modelo correspondiente al parámetro config
    model_name = model_mapping.get(config)
    # Obtener el modelo dinámicamente utilizando apps.get_model
    model = apps.get_model(config , model_name) 
    datos = model.objects.filter(verificado=False)
    nombres_campos = get_field_names(model)
    return render(request, 'inicio/verificar.html', {'datos': datos, 'config': config, 'nombres_campos': nombres_campos})

@login_required
def verificar_registros(request):
    try:
        config = request.session.get('config')
        model_mapping = {
            'monitoreo_del_agua': 'DatosFormularioMonitoreoDelAgua',
            'higiene_y_conducta_personal': 'DatosFormularioHigieneConductaPersonal',
            'monitoreo_de_plagas': 'DatosFormularioMonitoreoDePlagas',
            'recepcion_mpme': 'DatosFormularioRecepcionMpMe',
            'pcc2_detector_metales': 'DatosFormularioPcc2DetectorMetales',
            'control_de_transporte': 'DatosFormularioControlDeTransporte',
            'temperatura_despacho_ptjumbo': 'DatosFormularioTemperaturaDespachoJumbo',
            'temperatura_despacho_ptsisa': 'DatosFormularioTemperaturaDespachoSisa',
            'historial_termometro': 'DatosFormularioHistorialTermometro',
            'reclamo_a_proveedores': 'DatosFormularioReclamoProveedores',
            'rechazo_mp_in_me': 'DatosFormularioRechazoMpInMe',
            'informe_de_incidentes': 'DatosFormularioInformeDeIncidentes',
            'control_material_extraño': 'DatosFormularioControlMaterialExtraño'
        }
        if request.method == 'POST':
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            datos = body_data.get('userData')
            model_name = model_mapping.get(config)
            model = apps.get_model(config , model_name)

            for dato in datos:
                id = dato['id']
                isVerificado = dato['isVerificado']
                 
                if isVerificado:
                    usuario = model.objects.get(id=id, verificado=False)
                    usuario.verificado = True
                    usuario.verificado_por = request.user.nombre_completo
                    usuario.fecha_de_verificacion = timezone.now()
                    usuario.save()
            return JsonResponse({'existe': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Función para descargar los datos de los formularios, reemplaza los anteriormente creados
@login_required
def descargar_registros(request):
    fecha_inicio_str = request.session.get('fechainicio')
    fecha_fin_str = request.session.get('fechafin')
    config = request.GET['config']
    model_mapping = {
            'monitoreo_del_agua': 'DatosFormularioMonitoreoDelAgua',
            'higiene_y_conducta_personal': 'DatosFormularioHigieneConductaPersonal',
            'monitoreo_de_plagas': 'DatosFormularioMonitoreoDePlagas',
            'recepcion_mpme': 'DatosFormularioRecepcionMpMe',
            'pcc2_detector_metales': 'DatosFormularioPcc2DetectorMetales',
            'control_de_transporte': 'DatosFormularioControlDeTransporte',
            'temperatura_despacho_ptjumbo': 'DatosFormularioTemperaturaDespachoJumbo',
            'temperatura_despacho_ptsisa': 'DatosFormularioTemperaturaDespachoSisa',
            'historial_termometro': 'DatosFormularioHistorialTermometro',
            'reclamo_a_proveedores': 'DatosFormularioReclamoProveedores',
            'rechazo_mp_in_me': 'DatosFormularioRechazoMpInMe',
            'informe_de_incidentes': 'DatosFormularioInformeDeIncidentes',
            'control_material_extraño': 'DatosFormularioControlMaterialExtraño'
        }
    model_name = model_mapping.get(config)
    model = apps.get_model(config , model_name)
    
    objeto_filtrado = None
    if fecha_inicio_str == None or fecha_fin_str == None:
        objeto_filtrado = model.objects.all()
    else:
        fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio_str, '%Y-%m-%d'))
        fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin_str, '%Y-%m-%d'))
        objeto_filtrado = model.objects.filter(fecha_registro__range=[fecha_inicio, fecha_fin])

    filename = str(config) + '.xlsx'
    if not objeto_filtrado.exists():
        return render(request, 'inicio/no_hay_datos.html')
    else:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        wb = Workbook()
        ws = wb.active
        def get_field_names(model):
            fields = model._meta.get_fields()
            return [
                field.name for field in fields 
                if isinstance(field, Field)
            ]
        nombres_campos = get_field_names(model)
        ws.append(nombres_campos)
        def convertir_fecha(fecha):
            return fecha.astimezone(pytz.timezone('America/Santiago')).replace(tzinfo=None) if fecha else None
        def obtener_url_archivo(objeto, campo):
            archivo = getattr(objeto, campo, None)
            return archivo.url if archivo else None
        
        for objeto in objeto_filtrado:
            fila = []
            for campo in nombres_campos:
                valor = getattr(objeto, campo)
                if isinstance(valor, datetime):
                    valor = convertir_fecha(valor)
                if campo == 'archivo_foto':
                    valor = obtener_url_archivo(objeto, campo)
                fila.append(valor)
            ws.append(fila)
        wb.save(response)
        if fecha_inicio_str != None or fecha_fin_str != None:
            del request.session['fechainicio']
            del request.session['fechafin']
        return response