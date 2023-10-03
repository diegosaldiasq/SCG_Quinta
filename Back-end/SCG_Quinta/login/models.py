from django.db import models

# Create your models here.

class DatosFormularioCrearCuenta(models.Model):
    nombre_completo = models.TextField()
    perfil_usuario = models.TextField()
    rut = models.TextField()
    password = models.TextField()
    new_password = models.TextField()


    def __str__(self):
        return self.nombre
