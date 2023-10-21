from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, nombre_completo, perfil_usuario, rut, password=None):
        if not rut:
            raise ValueError("El campo RUT es obligatorio")
        user = self.model(nombre_completo=nombre_completo, perfil_usuario=perfil_usuario, rut=rut,new_password=password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nombre_completo, perfil_usuario, rut, password=None):
        user = self.create_user(nombre_completo, perfil_usuario, rut, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class DatosFormularioCrearCuenta(AbstractBaseUser, PermissionsMixin):
    nombre_completo = models.TextField(unique=True)
    perfil_usuario = models.CharField(max_length=20)
    rut = models.CharField(max_length=12)
    password = models.TextField()
    new_password = models.TextField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'nombre_completo'
    REQUIRED_FIELDS = ['rut', 'perfil_usuario']

    objects = CustomUserManager()
