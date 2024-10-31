from datetime import datetime
import time
import pytz
from datetime import timedelta
from zistemo_automation_api.comms.rest_api_comms import RestApiComms
from django.conf import settings

class ReportesZistemoBL():

    rest = RestApiComms()
    access_token = ""
    api_dev_key = ""

    def __init__(self):
        self.api_dev_key = settings.ZISTEMO_API_DEV_KEY
        url = settings.ZISTEMO_API_URL+"/sivale/login"
        auth_data = {"email": settings.ZISTEMO_USER_EMAIL, "password": settings.ZISTEMO_USER_PASSWORD}

        auth_json = self.rest.post(url=url+"?api_dev_key="+self.api_dev_key,data=auth_data)
        self.access_token = auth_json["data"]["access_token"]

        print("Initialized Zistemo with access token:: "+self.access_token)
    
    def recuperar_reporte_dia(self, fecha):

        return
    
    def listar_proyectos(self):

        rest = RestApiComms()
        url = settings.ZISTEMO_API_URL+"/sivale/projects"

        return self.rest.get(url=url, query_params_map=None, bearer_token=self.access_token, api_dev_key=self.api_dev_key)