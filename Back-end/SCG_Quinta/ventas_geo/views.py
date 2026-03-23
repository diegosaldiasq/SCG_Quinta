from django.shortcuts import render
from .forms import CargaVentasForm

def cargar_ventas(request):
    form = CargaVentasForm()
    return render(request, 'ventas_geo/cargar_ventas.html', {'form': form})