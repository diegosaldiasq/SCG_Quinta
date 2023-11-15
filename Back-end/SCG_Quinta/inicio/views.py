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
        request.session['fechainicio'] = fecha_inicio
        request.session['fechafin'] = fecha_fin
        return JsonResponse({'success': True})
    
@login_required
def no_hay_datos(request):
    return render(request, 'inicio/no_hay_datos.html')

@login_required
def descargar_monitoreo_del_agua(request):
    fecha_inicio_str = request.session.get('fechainicio')
    fecha_fin_str = request.session.get('fechafin')
    
    objeto_filtrado = None
    if fecha_inicio_str == None or fecha_fin_str == None:
        objeto_filtrado = DatosFormularioMonitoreoDelAgua.objects.all()
    else:
        fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio_str, '%Y-%m-%d'))
        fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin_str, '%Y-%m-%d'))
        objeto_filtrado = DatosFormularioMonitoreoDelAgua.objects.filter(fecha_registro__range=[fecha_inicio, fecha_fin])

    if not objeto_filtrado.exists():
        return render(request, 'inicio/no_hay_datos.html')
    else:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="monitoreo_del_agua.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.append(['nombre_tecnologo',
                    'fecha_registro',
                    'turno_mda',
                    'planta_mda',
                    'numero_llave',
                    'punto_muestreo',
                    'sabor_insipido',
                    'olor_inodora',
                    'color_incoloro',
                    'ph_mda',
                    'cloro_libre',
                    'accion_correctiva',
                    'resultado_ac',
                    'verificado',
                    'verificado_por',
                    'fecha_de_verificacion'])
        
        for objeto in objeto_filtrado:
            fecha_de_verificacion = (
                objeto.fecha_de_verificacion.astimezone(pytz.UTC).replace(tzinfo=None)
                if objeto.fecha_de_verificacion else None
            )
            ws.append([objeto.nombre_tecnologo,
                        objeto.fecha_registro.astimezone(pytz.UTC).replace(tzinfo=None),
                        objeto.turno_mda,
                        objeto.planta_mda,
                        objeto.numero_llave,
                        objeto.punto_muestreo,
                        objeto.sabor_insipido,
                        objeto.olor_inodora,
                        objeto.color_incoloro,
                        objeto.ph_mda,
                        objeto.cloro_libre,
                        objeto.accion_correctiva,
                        objeto.resultado_ac,
                        objeto.verificado,
                        objeto.verificado_por,
                        fecha_de_verificacion])
        wb.save(response)
        if fecha_inicio_str != None or fecha_fin_str != None:
            del request.session['fechainicio']
            del request.session['fechafin']
        return response

@login_required
def descargar_higiene_y_conducta_personal(request):
    fecha_inicio_str = request.session.get('fechainicio')
    fecha_fin_str = request.session.get('fechafin')
    
    objeto_filtrado = None
    if fecha_inicio_str == None or fecha_fin_str == None:
        objeto_filtrado = DatosFormularioHigieneConductaPersonal.objects.all()
    else:
        fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio_str, '%Y-%m-%d'))
        fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin_str, '%Y-%m-%d'))
        objeto_filtrado = DatosFormularioHigieneConductaPersonal.objects.filter(fecha_registro__range=[fecha_inicio, fecha_fin])

    if not objeto_filtrado.exists():
        return render(request, 'inicio/no_hay_datos.html')
    else:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="higiene_y_conducta_personal.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.append(['fecha_ingreso',
                        'nombre_personal',
                        'turno',
                        'planta',
                        'area',
                        'cumplimiento',
                        'desviacion',
                        'accion_correctiva',
                        'verificacion_accion_correctiva',
                        'observacion',
                        'nombre_tecnologo',
                        'verificado',
                        'verificado_por',
                        'fecha_de_verificacion'])
        
        for objeto in objeto_filtrado:
            fecha_de_verificacion = (
                objeto.fecha_de_verificacion.astimezone(pytz.UTC).replace(tzinfo=None)
                if objeto.fecha_de_verificacion else None
            )
            ws.append([objeto.fecha_ingreso.astimezone(pytz.UTC).replace(tzinfo=None),
                            objeto.nombre_personal,
                            objeto.turno,
                            objeto.planta,
                            objeto.area,
                            objeto.cumplimiento,
                            objeto.desviacion,
                            objeto.accion_correctiva,
                            objeto.verificacion_accion_correctiva,
                            objeto.observacion,
                            objeto.nombre_tecnologo,
                            objeto.verificado,
                            objeto.verificado_por,
                            fecha_de_verificacion])
        wb.save(response)
        if fecha_inicio_str != None or fecha_fin_str != None:
            del request.session['fechainicio']
            del request.session['fechafin']
        return response

@login_required
def descargar_monitoreo_de_plagas(request):
    fecha_inicio_str = request.session.get('fechainicio')
    fecha_fin_str = request.session.get('fechafin')
    
    objeto_filtrado = None
    if fecha_inicio_str == None or fecha_fin_str == None:
        objeto_filtrado = DatosFormularioMonitoreoDePlagas.objects.all()
    else:
        fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio_str, '%Y-%m-%d'))
        fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin_str, '%Y-%m-%d'))
        objeto_filtrado = DatosFormularioMonitoreoDePlagas.objects.filter(fecha_registro__range=[fecha_inicio, fecha_fin])

    if not objeto_filtrado.exists():
        return render(request, 'inicio/no_hay_datos.html')
    else:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="monitoreo_de_plagas.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.append(['nombre_tecnologo',
                        'fecha_registro',
                        'numero_estacion',
                        'tipo_plaga',
                        'tipo_trampa',
                        'ubicacion',
                        'monitoreo',
                        'accion_correctiva',
                        'verificado',
                        'verificado_por',
                        'fecha_de_verificacion'])
        
        for objeto in objeto_filtrado:
            fecha_de_verificacion = (
                objeto.fecha_de_verificacion.astimezone(pytz.UTC).replace(tzinfo=None)
                if objeto.fecha_de_verificacion else None
            )
            ws.append([objeto.nombre_tecnologo,
                            objeto.fecha_registro.astimezone(pytz.UTC).replace(tzinfo=None),
                            objeto.numero_estacion,
                            objeto.tipo_plaga,
                            objeto.tipo_trampa,
                            objeto.ubicacion,
                            objeto.monitoreo,
                            objeto.accion_correctiva,
                            objeto.verificado,
                            objeto.verificado_por,
                            fecha_de_verificacion])
        wb.save(response)
        if fecha_inicio_str != None or fecha_fin_str != None:
            del request.session['fechainicio']
            del request.session['fechafin']
        return response

@login_required
def descargar_recepcion_mpme(request):
    fecha_inicio_str = request.session.get('fechainicio')
    fecha_fin_str = request.session.get('fechafin')
    
    objeto_filtrado = None
    if fecha_inicio_str == None or fecha_fin_str == None:
        objeto_filtrado = DatosFormularioRecepcionMpMe.objects.all()
    else:
        fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio_str, '%Y-%m-%d'))
        fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin_str, '%Y-%m-%d'))
        objeto_filtrado = DatosFormularioRecepcionMpMe.objects.filter(fecha_registro__range=[fecha_inicio, fecha_fin])

    if not objeto_filtrado.exists():
        return render(request, 'inicio/no_hay_datos.html')
    else:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="recepcion_mpme.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.append(['nombre_tecnologo',
                        'lote_dia',
                        'fecha_registro',
                        'nombre_proveedor',
                        'nombre_producto',
                        'fecha_elaboracion',
                        'fecha_vencimiento',
                        'lote_producto',
                        'numero_factura',
                        'higiene',
                        'rs',
                        'temperatura_transporte',
                        'apariencia',
                        'textura',
                        'ausencia_material_extraño',
                        'temperatura_producto',
                        'condicion_envase',
                        'color',
                        'olor',
                        'sabor',
                        'grados_brix',
                        'verificado',
                        'verificado_por',
                        'fecha_de_verificacion'])
        
        for objeto in objeto_filtrado:
            fecha_de_verificacion = (
                objeto.fecha_de_verificacion.astimezone(pytz.UTC).replace(tzinfo=None)
                if objeto.fecha_de_verificacion else None
            )
            ws.append([objeto.nombre_tecnologo,
                            objeto.lote_dia,
                            objeto.fecha_registro.astimezone(pytz.UTC).replace(tzinfo=None),
                            objeto.nombre_proveedor,
                            objeto.nombre_producto,
                            objeto.fecha_elaboracion.astimezone(pytz.UTC).replace(tzinfo=None),
                            objeto.fecha_vencimiento.astimezone(pytz.UTC).replace(tzinfo=None),
                            objeto.lote_producto,
                            objeto.numero_factura,
                            objeto.higiene,
                            objeto.rs,
                            objeto.temperatura_transporte,
                            objeto.apariencia,
                            objeto.textura,
                            objeto.ausencia_material_extraño,
                            objeto.temperatura_producto,
                            objeto.condicion_envase,
                            objeto.color,
                            objeto.olor,
                            objeto.sabor,
                            objeto.grados_brix,
                            objeto.verificado,
                            objeto.verificado_por,
                            fecha_de_verificacion])
        wb.save(response)
        if fecha_inicio_str != None or fecha_fin_str != None:
            del request.session['fechainicio']
            del request.session['fechafin']
        return response
                     
@login_required
def descargar_pcc2_detector_metales(request):
    fecha_inicio_str = request.session.get('fechainicio')
    fecha_fin_str = request.session.get('fechafin')
    
    objeto_filtrado = None
    if fecha_inicio_str == None or fecha_fin_str == None:
        objeto_filtrado = DatosFormularioPcc2DetectorMetales.objects.all()
    else:
        fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio_str, '%Y-%m-%d'))
        fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin_str, '%Y-%m-%d'))
        objeto_filtrado = DatosFormularioPcc2DetectorMetales.objects.filter(fecha_registro__range=[fecha_inicio, fecha_fin])

    if not objeto_filtrado.exists():
        return render(request, 'inicio/no_hay_datos.html')
    else:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="pcc2_detector_metales.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.append(['nombre_tecnologo',
                        'fecha_registro',
                        'lote',
                        'turno',
                        'tipo_metal',
                        'medicion',
                        'producto',
                        'observaciones',
                        'accion_correctiva',
                        'verificado',
                        'verificado_por',
                        'fecha_de_verificacion'])
        
        for objeto in objeto_filtrado:
            fecha_de_verificacion = (
                objeto.fecha_de_verificacion.astimezone(pytz.UTC).replace(tzinfo=None)
                if objeto.fecha_de_verificacion else None
            )
            ws.append([objeto.nombre_tecnologo,
                            objeto.fecha_registro.astimezone(pytz.UTC).replace(tzinfo=None),
                            objeto.lote,
                            objeto.turno,
                            objeto.tipo_metal,
                            objeto.medicion,
                            objeto.producto,
                            objeto.observaciones,
                            objeto.accion_correctiva,
                            objeto.verificado,
                            objeto.verificado_por,
                            fecha_de_verificacion])
        wb.save(response)
        if fecha_inicio_str != None or fecha_fin_str != None:
            del request.session['fechainicio']
            del request.session['fechafin']
        return response

@login_required
def descargar_control_de_transporte(request):
    fecha_inicio_str = request.session.get('fechainicio')
    fecha_fin_str = request.session.get('fechafin')
    
    objeto_filtrado = None
    if fecha_inicio_str == None or fecha_fin_str == None:
        objeto_filtrado = DatosFormularioControlDeTransporte.objects.all()
    else:
        fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio_str, '%Y-%m-%d'))
        fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin_str, '%Y-%m-%d'))
        objeto_filtrado = DatosFormularioControlDeTransporte.objects.filter(fecha_registro__range=[fecha_inicio, fecha_fin])

    if not objeto_filtrado.exists():
        return render(request, 'inicio/no_hay_datos.html')
    else:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="control_de_transporte.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.append(['nombre_tecnologo',
                        'fecha_registro',
                        'fecha_recepcion',
                        'producto_recepcion',
                        'temperatura_transporte',
                        'temperatura_producto',
                        'lote',
                        'fecha_vencimiento',
                        'accion_correctiva',
                        'verificacion_accion_correctiva',
                        'verificado',
                        'verificado_por',
                        'fecha_de_verificacion'])
        
        for objeto in objeto_filtrado:
            fecha_de_verificacion = (
                objeto.fecha_de_verificacion.astimezone(pytz.UTC).replace(tzinfo=None)
                if objeto.fecha_de_verificacion else None
            )
            ws.append([objeto.nombre_tecnologo,
                            objeto.fecha_registro.astimezone(pytz.UTC).replace(tzinfo=None),
                            objeto.fecha_recepcion.astimezone(pytz.UTC).replace(tzinfo=None),
                            objeto.producto_recepcion,
                            objeto.temperatura_transporte,
                            objeto.temperatura_producto,
                            objeto.lote,
                            objeto.fecha_vencimiento.astimezone(pytz.UTC).replace(tzinfo=None),
                            objeto.accion_correctiva,
                            objeto.verificacion_accion_correctiva,
                            objeto.verificado,
                            objeto.verificado_por,
                            fecha_de_verificacion])
        wb.save(response)
        if fecha_inicio_str != None or fecha_fin_str != None:
            del request.session['fechainicio']
            del request.session['fechafin']
        return response

@login_required
def descargar_temperatura_despacho_ptjumbo(request):
    fecha_inicio_str = request.session.get('fechainicio')
    fecha_fin_str = request.session.get('fechafin')
    
    objeto_filtrado = None
    if fecha_inicio_str == None or fecha_fin_str == None:
        objeto_filtrado = DatosFormularioTemperaturaDespachoJumbo.objects.all()
    else:
        fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio_str, '%Y-%m-%d'))
        fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin_str, '%Y-%m-%d'))
        objeto_filtrado = DatosFormularioTemperaturaDespachoJumbo.objects.filter(fecha_registro__range=[fecha_inicio, fecha_fin])

    if not objeto_filtrado.exists():
        return render(request, 'inicio/no_hay_datos.html')
    else:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="temperatura_despacho_ptjumbo.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.append(['nombre_tecnologo',
                        'fecha_registro',
                        'cadena',
                        'item',
                        'producto',
                        'temperatura_producto',
                        'revision_etiquetado',
                        'lote',
                        'fecha_vencimiento',
                        'accion_correctiva',
                        'verificacion_accion_correctiva',
                        'verificado',
                        'verificado_por',
                        'fecha_de_verificacion'])
        
        for objeto in objeto_filtrado:
            fecha_de_verificacion = (
                objeto.fecha_de_verificacion.astimezone(pytz.UTC).replace(tzinfo=None)
                if objeto.fecha_de_verificacion else None
            )
            ws.append([objeto.nombre_tecnologo,
                            objeto.fecha_registro.astimezone(pytz.UTC).replace(tzinfo=None),
                            objeto.cadena,
                            objeto.item,
                            objeto.producto,
                            objeto.temperatura_producto,
                            objeto.revision_etiquetado,
                            objeto.lote,
                            objeto.fecha_vencimiento.astimezone(pytz.UTC).replace(tzinfo=None),
                            objeto.accion_correctiva,
                            objeto.verificacion_accion_correctiva,
                            objeto.verificado,
                            objeto.verificado_por,
                            fecha_de_verificacion])
        wb.save(response)
        if fecha_inicio_str != None or fecha_fin_str != None:
            del request.session['fechainicio']
            del request.session['fechafin']
        return response

@login_required
def descargar_temperatura_despacho_ptsisa(request):
    fecha_inicio_str = request.session.get('fechainicio')
    fecha_fin_str = request.session.get('fechafin')
    
    objeto_filtrado = None
    if fecha_inicio_str == None or fecha_fin_str == None:
        objeto_filtrado = DatosFormularioTemperaturaDespachoSisa.objects.all()
    else:
        fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio_str, '%Y-%m-%d'))
        fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin_str, '%Y-%m-%d'))
        objeto_filtrado = DatosFormularioTemperaturaDespachoSisa.objects.filter(fecha_registro__range=[fecha_inicio, fecha_fin])

    if not objeto_filtrado.exists():
        return render(request, 'inicio/no_hay_datos.html')
    else:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="temperatura_despacho_ptsisa.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.append(['nombre_tecnologo',
                        'fecha_registro',
                        'cadena',
                        'item',
                        'producto',
                        'temperatura_producto',
                        'revision_etiquetado',
                        'lote',
                        'fecha_vencimiento',
                        'accion_correctiva',
                        'verificacion_accion_correctiva',
                        'verificado',
                        'verificado_por',
                        'fecha_de_verificacion'])
        
        for objeto in objeto_filtrado:
            fecha_de_verificacion = (
                objeto.fecha_de_verificacion.astimezone(pytz.UTC).replace(tzinfo=None)
                if objeto.fecha_de_verificacion else None
            )
            ws.append([objeto.nombre_tecnologo,
                            objeto.fecha_registro.astimezone(pytz.UTC).replace(tzinfo=None),
                            objeto.cadena,
                            objeto.item,
                            objeto.producto,
                            objeto.temperatura_producto,
                            objeto.revision_etiquetado,
                            objeto.lote,
                            objeto.fecha_vencimiento.astimezone(pytz.UTC).replace(tzinfo=None),
                            objeto.accion_correctiva,
                            objeto.verificacion_accion_correctiva,
                            objeto.verificado,
                            objeto.verificado_por,
                            fecha_de_verificacion])
        wb.save(response)
        if fecha_inicio_str != None or fecha_fin_str != None:
            del request.session['fechainicio']
            del request.session['fechafin']
        return response

@login_required
def descargar_historial_termometro(request):
    fecha_inicio_str = request.session.get('fechainicio')
    fecha_fin_str = request.session.get('fechafin')
    
    objeto_filtrado = None
    if fecha_inicio_str == None or fecha_fin_str == None:
        objeto_filtrado = DatosFormularioHistorialTermometro.objects.all()
    else:
        fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio_str, '%Y-%m-%d'))
        fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin_str, '%Y-%m-%d'))
        objeto_filtrado = DatosFormularioHistorialTermometro.objects.filter(fecha_registro__range=[fecha_inicio, fecha_fin])

    if not objeto_filtrado.exists():
        return render(request, 'inicio/no_hay_datos.html')
    else:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="historial_termometro.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.append(['nombre_tecnologo',
                        'fecha_registro',
                        'codigo_termometro',
                        'valor_1',
                        'valor_2',
                        'valor_3',
                        'valor_4',
                        'valor_5',
                        'promedio_prueba',
                        'valor_6',
                        'valor_7',
                        'valor_8',
                        'valor_9',
                        'valor_10',
                        'promedio_patron',
                        'factor_anual',
                        'promedio_termometros',
                        'nivel_aceptacion',
                        'cumplimiento',
                        'accion_correctiva',
                        'verificacion_accion_correctiva',
                        'verificado',
                        'verificado_por',
                        'fecha_de_verificacion'])
        
        for objeto in objeto_filtrado:
            fecha_de_verificacion = (
                objeto.fecha_de_verificacion.astimezone(pytz.UTC).replace(tzinfo=None)
                if objeto.fecha_de_verificacion else None
            )
            ws.append([objeto.nombre_tecnologo,
                            objeto.fecha_registro.astimezone(pytz.UTC).replace(tzinfo=None),
                            objeto.codigo_termometro,
                            objeto.valor_1,
                            objeto.valor_2,
                            objeto.valor_3,
                            objeto.valor_4,
                            objeto.valor_5,
                            objeto.promedio_prueba,
                            objeto.valor_6,
                            objeto.valor_7,
                            objeto.valor_8,
                            objeto.valor_9,
                            objeto.valor_10,
                            objeto.promedio_patron,
                            objeto.factor_anual,
                            objeto.promedio_termometros,
                            objeto.nivel_aceptacion,
                            objeto.cumplimiento,
                            objeto.accion_correctiva,
                            objeto.verificacion_accion_correctiva,
                            objeto.verificado,
                            objeto.verificado_por,
                            fecha_de_verificacion])
        wb.save(response)
        if fecha_inicio_str != None or fecha_fin_str != None:
            del request.session['fechainicio']
            del request.session['fechafin']
        return response

@login_required
def descargar_reclamo_a_proveedores(request):
    fecha_inicio_str = request.session.get('fechainicio')
    fecha_fin_str = request.session.get('fechafin')
    
    objeto_filtrado = None
    if fecha_inicio_str == None or fecha_fin_str == None:
        objeto_filtrado = DatosFormularioReclamoProveedores.objects.all()
    else:
        fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio_str, '%Y-%m-%d'))
        fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin_str, '%Y-%m-%d'))
        objeto_filtrado = DatosFormularioReclamoProveedores.objects.filter(fecha_registro__range=[fecha_inicio, fecha_fin])

    if not objeto_filtrado.exists():
        return render(request, 'inicio/no_hay_datos.html')
    else:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="reclamo_a_proveedores.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.append(['nombre_tecnologo',
                        'fecha_registro',
                        'nombre_proveedor',
                        'fecha_reclamo',
                        'nombre_del_producto',
                        'fecha_elaboracion',
                        'lote',
                        'fecha_vencimiento',
                        'no_conformidad',
                        'clasificacion',
                        'cantidad_involucrada',
                        'unidad_de_medida',
                        'archivo_foto',
                        'verificado',
                        'verificado_por',
                        'fecha_de_verificacion'])
        
        for objeto in objeto_filtrado:
            fecha_de_verificacion = (
                objeto.fecha_de_verificacion.astimezone(pytz.UTC).replace(tzinfo=None)
                if objeto.fecha_de_verificacion else None
            )
            ws.append([objeto.nombre_tecnologo,
                            objeto.fecha_registro.astimezone(pytz.UTC).replace(tzinfo=None),
                            objeto.nombre_proveedor,
                            objeto.fecha_reclamo.astimezone(pytz.UTC).replace(tzinfo=None),
                            objeto.nombre_del_producto,
                            objeto.fecha_elaboracion.astimezone(pytz.UTC).replace(tzinfo=None),
                            objeto.lote,
                            objeto.fecha_vencimiento.astimezone(pytz.UTC).replace(tzinfo=None),
                            objeto.no_conformidad,
                            objeto.clasificacion,
                            objeto.cantidad_involucrada,
                            objeto.unidad_de_medida,
                            objeto.archivo_foto.url,
                            objeto.verificado,
                            objeto.verificado_por,
                            fecha_de_verificacion])
        wb.save(response)
        if fecha_inicio_str != None or fecha_fin_str != None:
            del request.session['fechainicio']
            del request.session['fechafin']
        return response

@login_required
def descargar_rechazo_mp_in_me(request):
    fecha_inicio_str = request.session.get('fechainicio')
    fecha_fin_str = request.session.get('fechafin')
    
    objeto_filtrado = None
    if fecha_inicio_str == None or fecha_fin_str == None:
        objeto_filtrado = DatosFormularioRechazoMpInMe.objects.all()
    else:
        fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio_str, '%Y-%m-%d'))
        fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin_str, '%Y-%m-%d'))
        objeto_filtrado = DatosFormularioRechazoMpInMe.objects.filter(fecha_registro__range=[fecha_inicio, fecha_fin])

    if not objeto_filtrado.exists():
        return render(request, 'inicio/no_hay_datos.html')
    else:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="rechazo_mp_in_me.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.append(['nombre_tecnologo',
                        'fecha_registro',
                        'nombre_proveedor',
                        'numero_factura',
                        'nombre_transportista',
                        'nombre_producto',
                        'fecha_elaboracion',
                        'lote',
                        'fecha_vencimiento',
                        'motivo_rechazo',
                        'cantidad_producto_involucrado',
                        'unidad_de_medida',
                        'clasificacion',
                        'verificado',
                        'verificado_por',
                        'fecha_de_verificacion'])
        
        for objeto in objeto_filtrado:
            fecha_de_verificacion = (
                objeto.fecha_de_verificacion.astimezone(pytz.UTC).replace(tzinfo=None)
                if objeto.fecha_de_verificacion else None
            )
            ws.append([objeto.nombre_tecnologo,
                            objeto.fecha_registro.astimezone(pytz.UTC).replace(tzinfo=None),
                            objeto.nombre_proveedor,
                            objeto.numero_factura,
                            objeto.nombre_transportista,
                            objeto.nombre_producto,
                            objeto.fecha_elaboracion.astimezone(pytz.UTC).replace(tzinfo=None),
                            objeto.lote,
                            objeto.fecha_vencimiento.astimezone(pytz.UTC).replace(tzinfo=None),
                            objeto.motivo_rechazo,
                            objeto.cantidad_producto_involucrado,
                            objeto.unidad_de_medida,
                            objeto.clasificacion,
                            objeto.verificado,
                            objeto.verificado_por,
                            fecha_de_verificacion])
        wb.save(response)
        if fecha_inicio_str != None or fecha_fin_str != None:
            del request.session['fechainicio']
            del request.session['fechafin']
        return response

@login_required
def descargar_informe_de_incidentes(request):
    fecha_inicio_str = request.session.get('fechainicio')
    fecha_fin_str = request.session.get('fechafin')
    
    objeto_filtrado = None
    if fecha_inicio_str == None or fecha_fin_str == None:
        objeto_filtrado = DatosFormularioInformeDeIncidentes.objects.all()
    else:
        fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio_str, '%Y-%m-%d'))
        fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin_str, '%Y-%m-%d'))
        objeto_filtrado = DatosFormularioInformeDeIncidentes.objects.filter(fecha_registro__range=[fecha_inicio, fecha_fin])

    if not objeto_filtrado.exists():
        return render(request, 'inicio/no_hay_datos.html')
    else:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="informe_de_incidentes.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.append(['nombre_tecnologo',
                        'fecha_registro',
                        'fuente_material',
                        'cantidad_contaminada',
                        'unidad_de_medida',
                        'lote_producto_contaminado',
                        'observaciones',
                        'analisis_causa',
                        'accion_correctiva',
                        'verificado',
                        'verificado_por',
                        'fecha_de_verificacion'])
        
        for objeto in objeto_filtrado:
            fecha_de_verificacion = (
                objeto.fecha_de_verificacion.astimezone(pytz.UTC).replace(tzinfo=None)
                if objeto.fecha_de_verificacion else None
            )
            ws.append([objeto.nombre_tecnologo,
                            objeto.fecha_registro.astimezone(pytz.UTC).replace(tzinfo=None),
                            objeto.fuente_material,
                            objeto.cantidad_contaminada,
                            objeto.unidad_de_medida,
                            objeto.lote_producto_contaminado,
                            objeto.observaciones,
                            objeto.analisis_causa,
                            objeto.accion_correctiva,
                            objeto.verificado,
                            objeto.verificado_por,
                            fecha_de_verificacion])
        wb.save(response)
        if fecha_inicio_str != None or fecha_fin_str != None:
            del request.session['fechainicio']
            del request.session['fechafin']
        return response

@login_required
def descargar_control_material_extraño(request):
    fecha_inicio_str = request.session.get('fechainicio')
    fecha_fin_str = request.session.get('fechafin')
    
    objeto_filtrado = None
    if fecha_inicio_str == None or fecha_fin_str == None:
        objeto_filtrado = DatosFormularioControlMaterialExtraño.objects.all()
    else:
        fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio_str, '%Y-%m-%d'))
        fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin_str, '%Y-%m-%d'))
        objeto_filtrado = DatosFormularioControlMaterialExtraño.objects.filter(fecha_registro__range=[fecha_inicio, fecha_fin])

    if not objeto_filtrado.exists():
        return render(request, 'inicio/no_hay_datos.html')
    else:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="control_material_extraño.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.append(['nombre_tecnologo',
                        'fecha_registro',
                        'turno',
                        'area_material',
                        'tipo_material',
                        'accion_correctiva',
                        'verificacion_accion_correctiva',  
                        'observaciones',
                        'verificado',
                        'verificado_por',
                        'fecha_de_verificacion'])
        
        for objeto in objeto_filtrado:
            fecha_de_verificacion = (
                objeto.fecha_de_verificacion.astimezone(pytz.UTC).replace(tzinfo=None)
                if objeto.fecha_de_verificacion else None
            )
            ws.append([objeto.nombre_tecnologo,
                            objeto.fecha_registro.astimezone(pytz.UTC).replace(tzinfo=None),
                            objeto.turno,
                            objeto.area_material,
                            objeto.tipo_material,
                            objeto.accion_correctiva,
                            objeto.verificacion_accion_correctiva,
                            objeto.observaciones,
                            objeto.verificado,
                            objeto.verificado_por,
                            fecha_de_verificacion])
        wb.save(response)
        if fecha_inicio_str != None or fecha_fin_str != None:
            del request.session['fechainicio']
            del request.session['fechafin']
        return response

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