from pathlib import Path
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

class CrearReporteDiaView(generics.GenericAPIView):

    def formatHours(self, hours):
        td = timedelta(hours=float(hours))
        total_seconds = td.total_seconds()
        hours = total_seconds//3600
        minutes = (td.seconds // 60) % 60
        return str(int(hours))+":"+str(minutes).zfill(2)
        
    def post(self, request, *args, **kwargs):
        
        fecha = request.data["fecha"]
        client_id = request.data["client_id"]

        cuentaZistemo = CuentasZistemo.objects.filter(client_id=client_id).first()
        if not cuentaZistemo:
            return Response({},404)
        
        timeEntries = TimeEntries.objects.filter(log_date_formatted=fecha).all()
        if not timeEntries or len(timeEntries)==0:
            return Response({},404)
        
        timeEntry = timeEntries[0]
        project = Proyectos.objects.filter(project_id=timeEntry.project_id).first()
        if not project:
            return Response({}, 404)

        # instantiating the class
        pdf = ZistemoPDF()
        pdf.set_client_name(client_id)
        pdf.set_font('Helvetica', size=8)
        # adding a page
        pdf.add_page(orientation='L')
        # opening html file 
        file = open("/Users/alexvaldes/Workspaces/Python/zistemo_automation_api/zistemo_automation_api/templates/reporte.html", "r")
        # extracting the data from hte file as a string
        data = file.read()

        # Replace general data

        data = data.replace("{{client_name}}",client_id)
        data = data.replace("{{user_name}}",timeEntry.userName)
        data = data.replace("{{initial_date}}",timeEntry.log_date_formatted)
        data = data.replace("{{end_date}}",timeEntry.log_date_formatted)

        #Iterate entries to replace data
        row_file = open("/Users/alexvaldes/Workspaces/Python/zistemo_automation_api/zistemo_automation_api/templates/time_entry_row.html", "r")
        row_stub = row_file.read()
        total_hours = 0
        rows_data = ""
        for te in timeEntries:
            total_hours = total_hours + float(te.hours)
            new_row = row_stub
            new_row = new_row.replace("{{te_log_date_formatted}}", te.log_date_formatted)
            new_row = new_row.replace("{{te_customer_name}}", te.customer_name)
            new_row = new_row.replace("{{pr_number}}", project.number)
            new_row = new_row.replace("{{te_projectName}}", te.projectName)
            new_row = new_row.replace("{{te_taskName}}", te.taskName)
            new_row = new_row.replace("{{te_notes}}", te.notes)
            new_row = new_row.replace("{{te_hours}}", self.formatHours(te.hours))
            new_row = new_row.replace("{{te_billed}}", "No" if te.billed=="0" else "Yes")

            rows_data = rows_data + new_row

        data = data.replace("{{time_entry_rows}}",rows_data)
        data = data.replace("{{total}}",self.formatHours(total_hours))

        # HTMLMixin write_html method
        pdf.write_html(data)
        date_parts = timeEntry.log_date_formatted.split("/")
        month = date_parts[1]
        year = date_parts[2]
        
        Path("/Users/alexvaldes/Workspaces/Python/zistemo_automation_api/zistemo_automation_api/templates/reportes_pdf/"+year+"/"+month).mkdir(parents=True, exist_ok=True)
        fileName = str(client_id).replace(" ","").lower()+"_"+str(timeEntry.userName).replace(" ","").lower()+"_"+timeEntry.log_date_formatted.replace("/","_")
        #saving the file as a pdf
        pdf.output('/Users/alexvaldes/Workspaces/Python/zistemo_automation_api/zistemo_automation_api/templates/reportes_pdf/'+year+'/'+month+'/'+fileName+'.pdf', 'F')
        pdf.alias_nb_pages()

        return Response({"pdf_creado":True},201) 
        
class TimesheetSaveView(generics.GenericAPIView):

    def post (self, request, *args, **kwargs):

        fecha_timesheet = request.data["fecha_timesheet"]

        #Buscamos entradas por cada usuario
        usuarios = UsuariosZistemo.objects.filter(activo=1).all()
        zistemoBL = ReportesZistemoBL()
        time_entries_created = 0
        for usuario in usuarios:
            user_id = usuario.zistemo_id

            time_entries = zistemoBL.listar_time_entries(fecha_timesheet,user_id)

            for time_entry in time_entries:
                te = TimeEntries.objects.filter(zistemo_id=time_entry["id"])
                if not te:
                    te = TimeEntries.objects.create(
                        zistemo_id = time_entry["id"],
                        user_id = time_entry["user_id"],
                        project_id = time_entry["project_id"],
                        hours = time_entry["hours"],
                        notes = time_entry["notes"],
                        billed = time_entry["billed"],
                        hours_rounded = time_entry["hours_rounded"],
                        projectName = time_entry["projectName"],
                        taskName = time_entry["taskName"],
                        userName = time_entry["userName"],
                        customer_name = time_entry["customer_name"],
                        log_date_formatted = time_entry["log_date_formatted"]
                    )

                    te.save()
                    time_entries_created = time_entries_created+1



        return Response({"time_entries_created":time_entries_created}, 201)
    