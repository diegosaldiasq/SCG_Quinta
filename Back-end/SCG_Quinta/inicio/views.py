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
def redireccionar_main(request):
    url_main = reverse('main')
    return HttpResponseRedirect(url_main)

@login_required
def descargas(request):
    return render(request, 'inicio/descargas.html')

@login_required
def descargar_monitoreo_del_agua(request):
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
                'resultado_ac'])
    
    for objeto in DatosFormularioMonitoreoDelAgua.objects.all():
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
                    objeto.resultado_ac])
    wb.save(response)
    return response

@login_required
def descargar_higiene_y_conducta_personal(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="higiene_y_conducta_personal.csv"'
    writer = csv.writer(response)
    writer.writerow(['fecha_ingreso',
                     'nombre_personal',
                     'turno',
                     'planta',
                     'area',
                     'cumplimiento',
                     'desviacion',
                     'accion_correctiva',
                     'verificacion_accion_correctiva',
                     'observacion',
                     'nombre_tecnologo'])
    
    for objeto in DatosFormularioHigieneConductaPersonal.objects.all():
        writer.writerow([objeto.fecha_ingreso,
                         objeto.nombre_personal,
                         objeto.turno,
                         objeto.planta,
                         objeto.area,
                         objeto.cumplimiento,
                         objeto.desviacion,
                         objeto.accion_correctiva,
                         objeto.verificacion_accion_correctiva,
                         objeto.observacion,
                         objeto.nombre_tecnologo])
    return response

@login_required
def descargar_monitoreo_de_plagas(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="monitoreo_de_plagas.csv"'
    writer = csv.writer(response)
    writer.writerow(['nombre_tecnologo',
                     'fecha_registro',
                     'numero_estacion',
                     'tipo_plaga',
                     'tipo_trampa',
                     'ubicacion',
                     'monitoreo',
                     'accion_correctiva'])
    
    for objeto in DatosFormularioMonitoreoDePlagas.objects.all():
        writer.writerow([objeto.nombre_tecnologo,
                         objeto.fecha_registro,
                         objeto.numero_estacion,
                         objeto.tipo_plaga,
                         objeto.tipo_trampa,
                         objeto.ubicacion,
                         objeto.monitoreo,
                         objeto.accion_correctiva])
    return response

@login_required
def descargar_recepcion_mpme(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="recepcion_mpme.csv"'
    writer = csv.writer(response)
    writer.writerow(['nombre_tecnologo',
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
                     'grados_brix'])
    
    for objeto in DatosFormularioRecepcionMpMe.objects.all():
        writer.writerow([objeto.nombre_tecnologo,
                         objeto.lote_dia,
                         objeto.fecha_registro,
                         objeto.nombre_proveedor,
                         objeto.nombre_producto,
                         objeto.fecha_elaboracion,
                         objeto.fecha_vencimiento,
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
                         objeto.grados_brix])
    return response
                     
@login_required
def descargar_pcc2_detector_metales(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pcc2_detector_metales.csv"'
    writer = csv.writer(response)
    writer.writerow(['nombre_tecnologo',
                     'fecha_registro',
                     'lote',
                     'turno',
                     'tipo_metal',
                     'medicion',
                     'producto',
                     'observaciones',
                     'accion_correctiva'])
    
    for objeto in DatosFormularioPcc2DetectorMetales.objects.all():
        writer.writerow([objeto.nombre_tecnologo,
                         objeto.fecha_registro,
                         objeto.lote,
                         objeto.turno,
                         objeto.tipo_metal,
                         objeto.medicion,
                         objeto.producto,
                         objeto.observaciones,
                         objeto.accion_correctiva])
    return response

@login_required
def descargar_control_de_transporte(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="control_de_transporte.csv"'
    writer = csv.writer(response)
    writer.writerow(['nombre_tecnologo',
                     'fecha_registro',
                     'fecha_recepcion',
                     'producto_recepcion',
                     'temperatura_transporte',
                     'temperatura_producto',
                     'lote',
                     'fecha_vencimiento',
                     'accion_correctiva',
                     'verificacion_accion_correctiva'])
    
    for objeto in DatosFormularioControlDeTransporte.objects.all():
        writer.writerow([objeto.nombre_tecnologo,
                         objeto.fecha_registro,
                         objeto.fecha_recepcion,
                         objeto.producto_recepcion,
                         objeto.temperatura_transporte,
                         objeto.temperatura_producto,
                         objeto.lote,
                         objeto.fecha_vencimiento,
                         objeto.accion_correctiva,
                         objeto.verificacion_accion_correctiva])
    return response

@login_required
def descargar_temperatura_despacho_ptjumbo(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="temperatura_despacho_ptjumbo.csv"'
    writer = csv.writer(response)
    writer.writerow(['nombre_tecnologo',
                     'fecha_registro',
                     'cadena',
                     'item',
                     'producto',
                     'temperatura_producto',
                     'revision_etiquetado',
                     'lote',
                     'fecha_vencimiento',
                     'accion_correctiva',
                     'verificacion_accion_correctiva'])
    
    for objeto in DatosFormularioTemperaturaDespachoJumbo.objects.all():
        writer.writerow([objeto.nombre_tecnologo,
                         objeto.fecha_registro,
                         objeto.cadena,
                         objeto.item,
                         objeto.producto,
                         objeto.temperatura_producto,
                         objeto.revision_etiquetado,
                         objeto.lote,
                         objeto.fecha_vencimiento,
                         objeto.accion_correctiva,
                         objeto.verificacion_accion_correctiva])
    return response

@login_required
def descargar_temperatura_despacho_ptsisa(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="temperatura_despacho_ptsisa.csv"'
    writer = csv.writer(response)
    writer.writerow(['nombre_tecnologo',
                     'fecha_registro',
                     'cadena',
                     'item',
                     'producto',
                     'temperatura_producto',
                     'revision_etiquetado',
                     'lote',
                     'fecha_vencimiento',
                     'accion_correctiva',
                     'verificacion_accion_correctiva'])
    
    for objeto in DatosFormularioTemperaturaDespachoSisa.objects.all():
        writer.writerow([objeto.nombre_tecnologo,
                         objeto.fecha_registro,
                         objeto.cadena,
                         objeto.item,
                         objeto.producto,
                         objeto.temperatura_producto,
                         objeto.revision_etiquetado,
                         objeto.lote,
                         objeto.fecha_vencimiento,
                         objeto.accion_correctiva,
                         objeto.verificacion_accion_correctiva])
    return response

@login_required
def descargar_historial_termometro(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="historial_termometro.csv"'
    writer = csv.writer(response)
    writer.writerow(['nombre_tecnologo',
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
                     'verificacion_accion_correctiva'])
    
    for objeto in DatosFormularioHistorialTermometro.objects.all():
        writer.writerow([objeto.nombre_tecnologo,
                         objeto.fecha_registro,
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
                         objeto.verificacion_accion_correctiva])
    return response

@login_required
def descargar_reclamo_a_proveedores(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reclamo_a_proveedores.csv"'
    writer = csv.writer(response)
    writer.writerow(['nombre_tecnologo',
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
                     'archivo_foto'])
    
    for objeto in DatosFormularioReclamoProveedores.objects.all():
        writer.writerow([objeto.nombre_tecnologo,
                         objeto.fecha_registro,
                         objeto.nombre_proveedor,
                         objeto.fecha_reclamo,
                         objeto.nombre_del_producto,
                         objeto.fecha_elaboracion,
                         objeto.lote,
                         objeto.fecha_vencimiento,
                         objeto.no_conformidad,
                         objeto.clasificacion,
                         objeto.cantidad_involucrada,
                         objeto.unidad_de_medida,
                         objeto.archivo_foto])
    return response

@login_required
def descargar_rechazo_mp_in_me(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rechazo_mp_in_me.csv"'
    writer = csv.writer(response)
    writer.writerow(['nombre_tecnologo',
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
                     'clasificacion'])
    
    for objeto in DatosFormularioRechazoMpInMe.objects.all():
        writer.writerow([objeto.nombre_tecnologo,
                         objeto.fecha_registro,
                         objeto.nombre_proveedor,
                         objeto.numero_factura,
                         objeto.nombre_transportista,
                         objeto.nombre_producto,
                         objeto.fecha_elaboracion,
                         objeto.lote,
                         objeto.fecha_vencimiento,
                         objeto.motivo_rechazo,
                         objeto.cantidad_producto_involucrado,
                         objeto.unidad_de_medida,
                         objeto.clasificacion])
    return response

@login_required
def descargar_informe_de_incidentes(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="informe_de_incidentes.csv"'
    writer = csv.writer(response)
    writer.writerow(['nombre_tecnologo',
                     'fecha_registro',
                     'fuente_material',
                     'cantidad_contaminada',
                     'unidad_de_medida',
                     'lote_producto_contaminado',
                     'observaciones',
                     'analisis_causa',
                     'accion_correctiva'])
    
    for objeto in DatosFormularioInformeDeIncidentes.objects.all():
        writer.writerow([objeto.nombre_tecnologo,
                         objeto.fecha_registro,
                         objeto.fuente_material,
                         objeto.cantidad_contaminada,
                         objeto.unidad_de_medida,
                         objeto.lote_producto_contaminado,
                         objeto.observaciones,
                         objeto.analisis_causa,
                         objeto.accion_correctiva])
    return response

@login_required
def descargar_control_material_extraño(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="control_material_extraño.csv"'
    writer = csv.writer(response)
    writer.writerow(['nombre_tecnologo',
                     'fecha_registro',
                     'turno',
                     'area_material',
                     'tipo_material',
                     'accion_correctiva',
                     'verificacion_accion_correctiva',  
                     'observaciones'])
    
    for objeto in DatosFormularioControlMaterialExtraño.objects.all():
        writer.writerow([objeto.nombre_tecnologo,
                         objeto.fecha_registro,
                         objeto.turno,
                         objeto.area_material,
                         objeto.tipo_material,
                         objeto.accion_correctiva,
                         objeto.verificacion_accion_correctiva,
                         objeto.observaciones])
    return response