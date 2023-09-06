from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioMonitoreoDePlagas

# Create your views here.


def historial_termometro(request):
    if request.method == 'POST' and request.is_ajax():
        nombre_tecnologo = request.POST.get('nombre_tecnologo')
        fecha_registro = request.POST.get('fecha_registro')
        codigo_termometro = request.POST.get('codigo_termometro')
        valor_1 = request.POST.get('valor_1')
        valor_2 = request.POST.get('valor_2')
        
        accion_correctiva = request.POST.get('accion_correctiva')

        nombre_tecnologo: nombreTecnologo,
        fecha_registro: fechaRegistro,
        codigo_termometro: codigoTermometro,
        valor_1: valor1,
        valor_2: valor2,
        valor_3: valor3,
        valor_4: valor4,
        valor_5: valor5,
        promedio_prueba: output1,
        valor_6: valor6,
        valor_7: valor7,
        valor_8: valor8,
        valor_9: valor9,
        valor_10: valor10,
        promedio_patron: output2,
        factor_anual: factan,
        promedio_termometros: informacionFunction.promedioCantidad,
        nivel_aceptacion: informacionFunction.x1,
        cumplimiento: informacionFunction.regla,
        accion_correctiva: accionCorrectiva,
        verificacion_accion_correctiva: verificacionAccionCorrectiva


        datos = DatosFormularioMonitoreoDePlagas(
            nombre_tecnologo=nombre_tecnologo, 
            fecha_registro=fecha_registro,
            numero_estacion=numero_estacion,
            tipo_plaga=tipo_plaga,
            tipo_trampa=tipo_trampa,
            ubicacion=ubicacion,
            monitoreo=monitoreo,
            accion_correctiva=accion_correctiva
            )
        datos.save()

        return JsonResponse({'mensaje': 'Datos guardados exitosamente'})
