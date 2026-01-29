from django.urls import path
from .views import RegistroCreateView, RegistroDetalleView

app_name = "control_layout_tortas"

urlpatterns = [
    path("nuevo/", RegistroCreateView.as_view(), name="registro_nuevo"),
    path("<int:pk>/", RegistroDetalleView.as_view(), name="registro_detalle"),
]