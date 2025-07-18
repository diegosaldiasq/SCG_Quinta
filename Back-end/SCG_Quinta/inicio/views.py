from django.shortcuts import render
from django.http import HttpResponse
import csv
from openpyxl import Workbook
import pytz
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from login.models import DatosFormularioCrearCuenta
import json
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
from django.db.models.fields import Field
from django.apps import apps
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt


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
def redireccionar_selecciones_2(request):
    url_selecciones = reverse('vista_selecciones_2')
    return HttpResponseRedirect(url_selecciones)

@login_required
def redireccionar_selecciones_3(request):
    url_selecciones = reverse('vista_selecciones_3')
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
def descargas_2(request):
    return render(request, 'inicio/descargas_2.html')

@login_required
def descargas_3(request):
    return render(request, 'inicio/descargas_3.html')

@csrf_exempt
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

@csrf_exempt
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
def intermedio_2(request):  
    return render(request, 'inicio/intermedio_2.html')

@login_required
def intermedio_3(request):  
    return render(request, 'inicio/intermedio_3.html')

@login_required
def seleccion_verifica(request):
    return render(request, 'inicio/seleccion_verifica.html')

@login_required
def seleccion_verifica_2(request):
    return render(request, 'inicio/seleccion_verifica_2.html')

# Diccionario para mapear el nombre de la configuración con el nombre del modelo
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
        'control_material_extraño': 'DatosFormularioControlMaterialExtraño',
        'control_de_pesos': 'DatosFormularioControlDePesos',
        'control_parametros_gorreri': 'DatosFormularioControlParametrosGorreri',
        'control_de_pesos_prelistos': 'DatosFormularioControlDePesosPrelistos',
        'control_de_pesos_insumos_kuchen': 'DatosFormularioControlDePesosInsumosKuchen',
        'calculo_oee': 'calculo_oee.ResumenTurnoOee',
    }

@csrf_exempt
@login_required
def verificar(request):
    if request.user.is_staff or request.user.is_superuser:
        config = request.GET.get('config')
        request.session['config'] = config
        pagina_numero = request.GET.get('page', 1)
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
        datos_sf = model.objects.filter(verificado=False)
        paginator = Paginator(datos_sf, 10)
        datos = paginator.get_page(pagina_numero)
        nombres_campos = get_field_names(model)
        return render(request, 'inicio/verificar.html', {'datos': datos, 'config': config, 'nombres_campos': nombres_campos})
    else:
        return render(request, 'inicio/falta_permiso.html')

@csrf_exempt
@login_required
def verificar_2(request):
    if request.user.is_staff or request.user.is_superuser:
        config = request.GET.get('config')
        request.session['config'] = config
        pagina_numero = request.GET.get('page', 1)
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
        datos_sf = model.objects.filter(verificado=False)
        paginator = Paginator(datos_sf, 10)
        datos = paginator.get_page(pagina_numero)
        nombres_campos = get_field_names(model)
        return render(request, 'inicio/verificar_2.html', {'datos': datos, 'config': config, 'nombres_campos': nombres_campos})
    else:
        return render(request, 'inicio/falta_permiso.html')

@csrf_exempt
@login_required
def verificar_registros(request):
    try:
        config = request.session.get('config')
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
@csrf_exempt
@login_required
def descargar_registros(request):
    fecha_inicio_str = request.session.get('fechainicio')
    fecha_fin_str = request.session.get('fechafin')
    config = request.GET['config']
    if not config:
        return render(request, 'inicio/no_hay_datos.html')
    model_name = model_mapping.get(config)
    #if not model_name:
    #    return render(request, 'inicio/no_hay_datos.html')
    model = apps.get_model(config , model_name)
    #if not model:
    #    return render(request, 'inicio/no_hay_datos.html')
    
    objeto_filtrado = None
    if fecha_inicio_str == None or fecha_fin_str == None:
        objeto_filtrado = model.objects.all()
    else:
        fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio_str, '%Y-%m-%d'))
        fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin_str, '%Y-%m-%d'))
        if model_name == 'ResumenTurnoOee':
            # Para ResumenTurnoOee, se filtra por fecha
            objeto_filtrado = model.objects.filter(fecha__range=[fecha_inicio, fecha_fin])  
        else:
            # Para otros modelos, se filtra por fecha_registro
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
    
@login_required
def en_desarrollo(request):
    config = request.GET.get('config')
    return render(request, 'inicio/sitio_en_construccion.html', {'config': config})

@login_required
def ver_foto(request):
    id = request.GET.get('id')
    config = request.GET.get('config')
    model_name = model_mapping.get(config)
    model = apps.get_model(config , model_name)
    objeto = model.objects.get(id=id)
    foto_archivo = objeto.archivo_foto
    return render(request, 'inicio/ver_foto.html', {'config': config, 'foto_archivo': foto_archivo})
