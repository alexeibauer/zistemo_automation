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
import os
import io
import csv
from datetime import datetime
from datetime import timezone
from datetime import timedelta
from google.cloud import storage
from zistemo_automation_api.puentes.mail import MailsBridge
from zistemo_automation_api.file_storage.factory import FileStorageFactory
from zistemo_automation_api.utils import Utils
from zistemo_automation_api.data_utils import DataUtils
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
        
        timeEntriesDB = TimeEntries.objects.filter(log_date_formatted=fecha).all()
        if not timeEntriesDB or len(timeEntriesDB)==0:
            return Response({},404)
        
        #Map time entries by day and user
        timeEntriesMap = {}
        for timeEntryRow in timeEntriesDB:

            timeEntryKey = timeEntryRow.log_date_formatted+"-"+timeEntryRow.userName

            if timeEntryKey not in timeEntriesMap:
                timeEntriesMap[timeEntryKey] = []

            timeEntriesMap[timeEntryKey].append(timeEntryRow)
        
        numero_pdfs_creados = 0
        for timeEntryKey in timeEntriesMap.keys():

            timeEntries = timeEntriesMap[timeEntryKey]
            timeEntry = timeEntries[0]
            
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
                #new_row = new_row.replace("{{pr_number}}", project.number)
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
            date_parts = None
            if "/" in timeEntry.log_date_formatted:
                date_parts = timeEntry.log_date_formatted.split("/")
                month = date_parts[1]
                year = date_parts[2]
            elif "." in timeEntry.log_date_formatted:
                date_parts = timeEntry.log_date_formatted.split(".")
                month = date_parts[0]
                year = date_parts[2]
            
            Path("/Users/alexvaldes/Workspaces/Python/zistemo_automation_api/zistemo_automation_api/templates/reportes_pdf/"+year+"/"+month).mkdir(parents=True, exist_ok=True)
            fileName = str(client_id).replace(" ","").lower()+"_"+str(timeEntry.userName).replace(" ","").lower()+"_"+timeEntry.log_date_formatted.replace("/","_")
            #saving the file as a pdf
            pdf.output('/Users/alexvaldes/Workspaces/Python/zistemo_automation_api/zistemo_automation_api/templates/reportes_pdf/'+year+'/'+month+'/'+fileName+'.pdf', 'F')
            pdf.alias_nb_pages()
            numero_pdfs_creados = numero_pdfs_creados + 1

        return Response({"pdf_creado":True, "numero_pdfs_creados": numero_pdfs_creados},201) 
        
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

class LocalTimesheetSaveView(generics.GenericAPIView):

    def post (self, request, *args, **kwargs):

        local_path_with_csv_files = request.GET.get("local_path_with_csv_files")

        time_entries = {}

        for root, dirs, files in os.walk(local_path_with_csv_files):
            for file in files:
                full_csv_file = os.path.join(root, file)
                f = open(full_csv_file, "r")
                f.seek(0)
                single_timesheet_lines = csv.DictReader(io.StringIO(f.read()))

                just_file_name = os.path.basename(full_csv_file).split('/')[-1]
                if just_file_name not in time_entries:
                    time_entries[just_file_name] = []
                time_entries[just_file_name].extend(single_timesheet_lines)

        #Insert into DB
        time_entries_created = 0
        for time_entry_file_name in time_entries.keys():
            print("Processing file: "+time_entry_file_name)
            for time_entry in time_entries[time_entry_file_name]:
                if "Date" not in time_entry or time_entry["Date"]=="":
                    break

                time_entry_key = DataUtils.convert_point_date_to_slash(time_entry["Date"])+"-"+time_entry["Project Name"]+"-"+time_entry["Staff Name"]+"-"+time_entry["Task Name"]
                te = TimeEntries.objects.filter(csv_key=time_entry_key)
                if not te:
                    te = TimeEntries.objects.create(
                        csv_key = time_entry_key,
                        hours = DataUtils.convert_hours_to_float(time_entry["Hours"]),
                        notes = time_entry["Notes"],
                        hours_rounded = DataUtils.convert_hours_to_float(time_entry["Hours"]),
                        projectName = time_entry["Project Name"],
                        taskName = time_entry["Task Name"],
                        userName = time_entry["Staff Name"],
                        customer_name = "-internal-",
                        log_date_formatted = DataUtils.convert_point_date_to_slash(time_entry["Date"]),
                        time_entry_file_name = time_entry_file_name
                    )

                    te.save()
                    time_entries_created = time_entries_created+1


        return Response({"message": "Time entries created:: "+str(time_entries_created)}, 201)
