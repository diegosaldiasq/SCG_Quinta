from django.shortcuts import render
from django.http import JsonResponse
from .models import DatosFormularioControlDeTransporte
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
import json

# Create your views here.

@login_required
def control_de_pesos(request):
    return render(request, 'control_de_pesps/r_control_de_pesos.html')


