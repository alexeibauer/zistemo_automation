from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from zistemo_automation_api.serializers import *
from zistemo_automation_api.models import *
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from datetime import datetime
from django.conf import settings
from django.template.loader import render_to_string
import string
import random
import json
from datetime import datetime
from datetime import timezone
from datetime import timedelta
from google.cloud import storage
from zistemo_automation_api.puentes.mail import MailsBridge
from zistemo_automation_api.file_storage.factory import FileStorageFactory
from zistemo_automation_api.utils import Utils
from zistemo_automation_api.business_logic.reportes_zistemo_bl import ReportesZistemoBL

class CatalogoProyectosView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):

        proyectos = ReportesZistemoBL().listar_proyectos()
        proyectos_creados = 0
        if "success" in proyectos and proyectos["success"]=="true":
            for proyecto in proyectos["data"]:
                p = Proyectos.objects.filter(project_name=proyecto["project_name"], number=proyecto["number"]).first()

                if not p:
                    p = Proyectos.objects.create(
                                project_name = proyecto["project_name"],
                                number = proyecto["number"],
                                customer_name = proyecto["customer_name"],
                                status = proyecto["status"]
                                )
                    p.save()
                    proyectos_creados = proyectos_creados+1

        return Response({"proyectos_creados": proyectos_creados})