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
from fpdf import FPDF, HTMLMixin

# creating a class inherited from both FPDF and HTMLMixin
class ZistemoPDF(FPDF, HTMLMixin):

    client_name=""

    def get_current_formatted_date(self):

        return datetime.now().strftime("%d/%m/%Y")

    def set_client_name(self, client_name):
        self.client_name = client_name

    def footer(self):
        # Go to 1.5 cm from bottom
        self.set_y(-15)
        # Select Arial italic 8
        self.set_font('Helvetica', size = 8)

        self.cell(0, 10, self.client_name+" - "+self.get_current_formatted_date(), 0, 0, 'L')
        self.cell(0, 10, 'Page %s' % self.page_no() + ' of {nb}', 0, 0, 'R')

class DescargarReporteView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        

        # instantiating the class
        pdf = ZistemoPDF()
        pdf.set_client_name("Groupe Up")
        pdf.set_font('Helvetica', size=8)
        # adding a page
        pdf.add_page(orientation='L')
        # opening html file 
        file = open("/Users/alexvaldes/Workspaces/Python/zistemo_automation_api/zistemo_automation_api/templates/reporte.html", "r")
        # extracting the data from hte file as a string
        data = file.read()
        # HTMLMixin write_html method
        pdf.write_html(data)


        #saving the file as a pdf
        pdf.output('/Users/alexvaldes/Workspaces/Python/zistemo_automation_api/zistemo_automation_api/templates/reporte.pdf', 'F')
        pdf.alias_nb_pages()

        return Response() 