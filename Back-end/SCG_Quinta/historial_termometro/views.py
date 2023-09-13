from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioHistorialTermometro
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def historial_termometro(request):
    vista_historial_termometro(request)
    return render(request, 'historial_termometro/r_historial_termometro.html')


def vista_historial_termometro(request):
    if request.method == 'POST' and request.is_ajax():
        nombre_tecnologo = request.POST.get('nombre_tecnologo')
        fecha_registro = request.POST.get('fecha_registro')
        codigo_termometro = request.POST.get('codigo_termometro')
        valor_1 = request.POST.get('valor_1')
        valor_2 = request.POST.get('valor_2')
        valor_3 = request.POST.get('valor_3')
        valor_4 = request.POST.get('valor_4')
        valor_5 = request.POST.get('valor_5')
        promedio_prueba = request.get('promedio_prueba')
        valor_6 = request.POST.get('valor_6')
        valor_7 = request.POST.get('valor_7')
        valor_8 = request.POST.get('valor_8')
        valor_9 = request.POST.get('valor_9')
        valor_10 = request.POST.get('valor_10')
        promedio_patron = request.POST.get('promedio_patron')   
        factor_anual = request.POST.get('factor_anual')
        promedio_termometros = request.POST.get('promedio_termometros')
        nivel_aceptacion = request.POST.get('nivel_aceptacion')
        cumplimiento = request.POST.get('cumplimiento')     
        accion_correctiva = request.POST.get('accion_correctiva')
        verificacion_accion_correctiva = request.POST.get('verificacion_accion_correctiva')


        datos = DatosFormularioHistorialTermometro(
            nombre_tecnologo=nombre_tecnologo, 
            fecha_registro=fecha_registro,
            codigo_termometro=codigo_termometro,
            valor_1=valor_1,
            valor_2=valor_2,
            valor_3=valor_3,
            valor_4=valor_4,
            valor_5=valor_5,
            promedio_prueba=promedio_prueba,
            valor_6=valor_6,
            valor_7=valor_7,
            valor_8=valor_8,
            valor_9=valor_9,
            valor_10=valor_10,
            promedio_patron=promedio_patron,
            factor_anual=factor_anual,
            promedio_termometros=promedio_termometros,
            nivel_aceptacion=nivel_aceptacion,
            cumplimiento=cumplimiento,
            accion_correctiva=accion_correctiva,
            verificacion_accion_correctiva=verificacion_accion_correctiva
            )
        datos.save()

        return JsonResponse({'mensaje': 'Datos guardados exitosamente'})
    
def redireccionar_selecciones(request):
    url_selecciones = reverse('vista_selecciones')
    return HttpResponseRedirect(url_selecciones)



