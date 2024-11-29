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
    access_token = models.TextField(null=False, blank=False, max_length=255, default=None)
    expires = models.DateTimeField(null=False, blank=False, default=None)
    ultima_fecha_obtencion_token = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    client_id = models.TextField(null=True, blank=True, max_length=255)

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
    project_id = models.TextField(null=False, blank=False, max_length=255, default=None) 
    project_name = models.TextField(null=False, blank=False, max_length=255)
    number = models.TextField(null=False, blank=False, max_length=255)
    customer_name = models.TextField(null=True, blank=True, max_length=255)
    status = models.TextField(null=True, blank=True, max_length=255)
    activo = models.BooleanField(null=False, blank=False, default=True)

    def __str__(self):
        return self.project_name
    
class UsuariosZistemo(models.Model):
    id = models.BigAutoField(primary_key=True)
    zistemo_id = models.TextField(null=False, blank=False, max_length=255, default=None)
    first_name = models.TextField(null=False, blank=False, max_length=255, default=None)
    last_name = models.TextField(null=False, blank=False, max_length=255, default=None)
    email = models.TextField(null=True, blank=True, max_length=255)
    zistemo_activo = models.BooleanField(null=False, blank=False, default=True)
    activo = models.BooleanField(null=False, blank=False, default=True)

    def __str__(self):
        return self.project_name
    
class TimeEntries(models.Model):
    id = models.BigAutoField(primary_key=True)
    csv_key = models.TextField(null=True, blank=True, max_length=255, default=None)
    zistemo_id = models.TextField(null=True, blank=True, max_length=255, default=None)
    user_id = models.TextField(null=True, blank=True, max_length=255, default=None)
    project_id = models.TextField(null=True, blank=True, max_length=255, default="")
    hours = models.TextField(null=False, blank=False, max_length=255, default=None)
    notes = models.TextField(null=True, blank=True, max_length=255, default="")
    billed = models.TextField(null=True, blank=True, max_length=255, default="0")
    hours_rounded = models.TextField(null=False, blank=False, max_length=255, default=None)
    projectName = models.TextField(null=False, blank=False, max_length=255, default=None)
    taskName = models.TextField(null=False, blank=False, max_length=255, default=None)
    userName = models.TextField(null=False, blank=False, max_length=255, default=None)
    customer_name = models.TextField(null=False, blank=False, max_length=255, default=None)
    log_date_formatted = models.TextField(null=False, blank=False, max_length=255, default=None)
    time_entry_file_name = models.TextField(null=True, blank=True, max_length=255, default=None)
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)

    def __str__(self):
        return self.taskName
