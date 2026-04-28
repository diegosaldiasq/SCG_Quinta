from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from openpyxl import Workbook

from .forms import RegistroSalaCremasForm
from .models import RegistroSalaCremas


@login_required
def registro_sala_cremas(request):
    if request.method == "POST":
        form = RegistroSalaCremasForm(request.POST)

        if form.is_valid():
            registro = form.save(commit=False)

            if hasattr(request.user, "nombre_completo"):
                registro.usuario = request.user.nombre_completo
            else:
                registro.usuario = request.user.get_full_name() or request.user.username

            registro.fecha_hora = timezone.now()
            registro.save()

            messages.success(request, "Registro guardado correctamente.")
            return redirect("control_sala_cremas:registro_sala_cremas")
    else:
        form = RegistroSalaCremasForm()

    return render(request, "control_sala_cremas/registro_sala_cremas.html", {
        "form": form,
    })


@login_required
def historial_sala_cremas(request):
    registros = RegistroSalaCremas.objects.all()

    fecha_desde = request.GET.get("fecha_desde")
    fecha_hasta = request.GET.get("fecha_hasta")
    turno = request.GET.get("turno")
    cliente = request.GET.get("cliente")
    producto = request.GET.get("producto")
    lote = request.GET.get("lote")
    batidora = request.GET.get("batidora")

    if fecha_desde:
        registros = registros.filter(fecha_hora__date__gte=fecha_desde)

    if fecha_hasta:
        registros = registros.filter(fecha_hora__date__lte=fecha_hasta)

    if turno:
        registros = registros.filter(turno=turno)

    if cliente:
        registros = registros.filter(cliente__icontains=cliente)

    if producto:
        registros = registros.filter(producto__icontains=producto)

    if lote:
        registros = registros.filter(lote__icontains=lote)

    if batidora:
        registros = registros.filter(numero_batidora__icontains=batidora)

    return render(request, "control_sala_cremas/historial_sala_cremas.html", {
        "registros": registros,
        "filtros": request.GET,
    })


@login_required
def descargar_sala_cremas_excel(request):
    registros = RegistroSalaCremas.objects.all()

    fecha_desde = request.GET.get("fecha_desde")
    fecha_hasta = request.GET.get("fecha_hasta")
    turno = request.GET.get("turno")
    cliente = request.GET.get("cliente")
    producto = request.GET.get("producto")
    lote = request.GET.get("lote")
    batidora = request.GET.get("batidora")

    if fecha_desde:
        registros = registros.filter(fecha_hora__date__gte=fecha_desde)

    if fecha_hasta:
        registros = registros.filter(fecha_hora__date__lte=fecha_hasta)

    if turno:
        registros = registros.filter(turno=turno)

    if cliente:
        registros = registros.filter(cliente__icontains=cliente)

    if producto:
        registros = registros.filter(producto__icontains=producto)

    if lote:
        registros = registros.filter(lote__icontains=lote)

    if batidora:
        registros = registros.filter(numero_batidora__icontains=batidora)

    wb = Workbook()
    ws = wb.active
    ws.title = "Sala Cremas"

    headers = [
        "Usuario",
        "Fecha y hora",
        "Turno",
        "Cliente",
        "Producto",
        "Código",
        "Lote",
        "Densidad",
        "Temperatura",
        "N° Batidora",
        "Observaciones",
    ]

    ws.append(headers)

    for r in registros:
        ws.append([
            r.usuario,
            r.fecha_hora.strftime("%d-%m-%Y %H:%M"),
            r.turno,
            r.cliente,
            r.producto,
            r.codigo,
            r.lote,
            float(r.densidad),
            float(r.temperatura),
            r.numero_batidora,
            r.observaciones or "",
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="registros_sala_cremas.xlsx"'

    wb.save(response)
    return response