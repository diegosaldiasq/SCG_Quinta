from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, nombre_completo, perfil_usuario, rut, pasword=None,):
        if not rut:
            raise ValueError("El campo RUT es obligatorio")
        user = self.model(nombre_completo=nombre_completo, perfil_usuario=perfil_usuario, pasword=pasword)
        user.set_password(pasword)
        user.save(using=self._db)
        return user

    def create_superuser(self, nombre_completo, perfil_usuario, rut, pasword=None):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(nombre_completo, perfil_usuario, rut, pasword)

class DatosFormularioCrearCuenta(AbstractBaseUser, PermissionsMixin):
    nombre_completo = models.TextField()
    perfil_usuario = models.TextField()
    rut = models.TextField(unique=True)
    password = models.TextField()
    new_password = models.TextField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'rut'
    REQUIRED_FIELDS = ['nombre_completo', 'perfil_usuario', 'password']

    objects = CustomUserManager()
