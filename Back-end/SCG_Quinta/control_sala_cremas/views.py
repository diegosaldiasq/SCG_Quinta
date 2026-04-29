from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import JsonResponse
from django.utils.timezone import localtime
from django.urls import reverse


from openpyxl import Workbook

from .forms import RegistroSalaCremasForm
from .models import RegistroSalaCremas, ProductoSalaCremas


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
        "Tipo crema",
        "Aplicación",
        "Densidad",
        "Temperatura",
        "N° Batidora",
        "Observaciones",
        "Verificado",
        "Fecha de verificación",
        "Verificado por",   
    ]

    ws.append(headers)

    for r in registros:
        ws.append([
            r.usuario,
            localtime(r.fecha_hora).strftime("%d-%m-%Y %H:%M"),
            r.turno,
            r.cliente,
            r.producto,
            r.codigo,
            r.lote,
            r.tipo_crema,
            r.aplicacion,
            float(r.densidad),
            float(r.temperatura),
            r.numero_batidora,
            r.observaciones or "",
            r.verificado,
            localtime(r.fecha_verificacion).strftime("%d-%m-%Y %H:%M") if r.fecha_verificacion else "",
            r.verificado_por or "",
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="registros_sala_cremas.xlsx"'

    wb.save(response)
    return response

@login_required
def api_clientes_sala_cremas(request):
    clientes = (
        ProductoSalaCremas.objects
        .filter(activo=True)
        .values_list("cliente", flat=True)
        .distinct()
        .order_by("cliente")
    )
    return JsonResponse({"clientes": list(clientes)})


@login_required
def api_productos_por_cliente_sala_cremas(request):
    cliente = request.GET.get("cliente", "")

    productos = (
        ProductoSalaCremas.objects
        .filter(cliente=cliente, activo=True)
        .values("producto", "codigo")
        .order_by("producto")
    )

    return JsonResponse({"productos": list(productos)})


@login_required
def verificar_registro_sala_cremas(request, pk):
    if request.method != "POST":
        return redirect("control_sala_cremas:historial_sala_cremas")

    registro = get_object_or_404(RegistroSalaCremas, pk=pk)

    if hasattr(request.user, "nombre_completo"):
        verificador = request.user.nombre_completo
    else:
        verificador = request.user.get_full_name() or request.user.username

    registro.verificado = True
    registro.fecha_verificacion = timezone.now()
    registro.verificado_por = verificador
    registro.save(update_fields=["verificado", "fecha_verificacion", "verificado_por"])

    messages.success(request, "Registro verificado correctamente.")
    return redirect(request.POST.get("next") or "control_sala_cremas:historial_sala_cremas")

@login_required
def redireccionar_selecciones_2(request):
    url_selecciones = reverse('vista_selecciones_2')
    return HttpResponseRedirect(url_selecciones)

@login_required
def redireccionar_seleccion_verifica_2(request):
    url_seleccion_verifica = reverse('seleccion_verifica_2')
    return HttpResponseRedirect(url_seleccion_verifica)