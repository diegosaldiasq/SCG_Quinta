"""
URL configuration for SCG_Quinta project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("login.urls")),
    path("inicio/", include("inicio.urls")),
    path("monitoreo_del_agua/", include("monitoreo_del_agua.urls")),
    path("monitoreo_de_plagas/", include("monitoreo_de_plagas.urls")),
    path("pcc2_detector_metales/", include("pcc2_detector_metales.urls")),
    path("recepcion_mpme/", include("recepcion_mpme.urls")),
    path("higiene_y_conducta_personal/", include("higiene_y_conducta_personal.urls")),
    path("control_de_transporte/", include("control_de_transporte.urls")),
    path("temperatura_despacho_ptjumbo/", include("temperatura_despacho_ptjumbo.urls")),
    path("temperatura_despacho_ptsisa/", include("temperatura_despacho_ptsisa.urls")),
    path("informe_de_incidentes/", include("informe_de_incidentes.urls")),
    path("historial_termometro/", include("historial_termometro.urls")),
    path("control_material_extraño/", include("control_material_extraño.urls")),
    path("rechazo_mp_in_me/", include("rechazo_mp_in_me.urls")),
    path("reclamo_a_proveedores/", include("reclamo_a_proveedores.urls")),
    path("selecciones/", include("selecciones.urls")),
    path("login/", include("login.urls")),
    path("control_de_pesos/", include("control_de_pesos.urls")),
    path("control_parametros_gorreri/", include("control_parametros_gorreri.urls")),
    path("control_de_pesos_prelistos/", include("control_de_pesos_prelistos.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

