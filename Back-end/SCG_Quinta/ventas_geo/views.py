from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CargaVentasForm
from .services import procesar_carga_ventas


def cargar_ventas(request):
    if request.method == 'POST':
        form = CargaVentasForm(request.POST, request.FILES)
        if form.is_valid():
            carga = form.save()
            try:
                procesar_carga_ventas(carga)
                messages.success(request, 'Archivo procesado correctamente.')
                return redirect('ventas_geo:cargar_ventas')
            except Exception as e:
                messages.error(request, f'Error al procesar el archivo: {e}')
                return redirect('ventas_geo:cargar_ventas')
    else:
        form = CargaVentasForm()

    return render(request, 'ventas_geo/cargar_ventas.html', {'form': form})