from django.http import HttpResponse

def cargar_ventas(request):
    return HttpResponse("ventas_geo funcionando")

def resultado_carga(request, carga_id):
    return HttpResponse(f"resultado carga {carga_id}")

def dashboard_ventas_geo(request):
    return HttpResponse("dashboard ventas geo")