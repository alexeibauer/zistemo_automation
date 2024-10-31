from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

class BearerTokenAuthentication(TokenAuthentication):
    keyword = u"Bearer"


class CuentasZistemo(models.Model):
    id = models.BigAutoField(primary_key=True)
    api_dev_key = models.TextField(null=False, blank=False, max_length=255, default=None)
    user = models.TextField(null=False, blank=False, max_length=255)
    password = models.TextField(null=False, blank=False, max_length=255, default=None)
    access_token = models.TextField(null=False, blank=False, max_length=255, default=None)
    expires_in = models.IntegerField(null=False, blank=False, default=None)
    refresh_token = models.TextField(null=False, blank=False,  default=None)
    ultima_fecha_obtencion_token = models.DateTimeField(null=False, blank=False, auto_now_add=True)

    def __str__(self):
        return self.usuario
    
class Configuraciones(models.Model):
    id = models.BigAutoField(primary_key=True)
    cuenta_zistemo= models.ForeignKey(CuentasZistemo, on_delete=models.CASCADE, null=True, blank=True, default=None)
    llave = models.TextField(null=False, blank=False, max_length=255)
    valor = models.TextField(null=False, blank=False, max_length=255)

    def __str__(self):
        return self.llave

class Proyectos(models.Model):
    id = models.BigAutoField(primary_key=True)
    project_name = models.TextField(null=False, blank=False, max_length=255)
    number = models.TextField(null=False, blank=False, max_length=255)
    customer_name = models.TextField(null=True, blank=True, max_length=255)
    status = models.TextField(null=True, blank=True, max_length=255)
    activo = models.BooleanField(null=False, blank=False, default=True)

    def __str__(self):
        return self.project_name