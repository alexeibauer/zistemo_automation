from datetime import datetime
import time
import pytz
from datetime import timedelta
from zistemo_automation_api.comms.rest_api_comms import RestApiComms
from django.conf import settings
from zistemo_automation_api.models import *

class ReportesZistemoBL():

    rest = RestApiComms()
    access_token = ""
    api_dev_key = ""

    def __init__(self):
        
        self.api_dev_key = settings.ZISTEMO_API_DEV_KEY
        cuenta = CuentasZistemo.objects.filter(api_dev_key=self.api_dev_key).first()
        if cuenta:
            print("Cuenta zistemo encontrada")
            refresh_token = self.refrescar_token(cuenta.access_token, cuenta.ultima_fecha_obtencion_token, cuenta.expires)
            cuenta.access_token = refresh_token["access_token"]
            if refresh_token["se_actualizo"]:
                print("Token refrescado")
                cuenta.ultima_fecha_obtencion_token = datetime.now()
                cuenta.expires = refresh_token["expires"]
            cuenta.save()
        else:
            print("Cuenta zistemo no encontrada")
            auth_json = self.auth_zistemo()
            cuenta = CuentasZistemo.objects.create(
                api_dev_key = self.api_dev_key,
                access_token = auth_json["data"]["access_token"],
                ultima_fecha_obtencion_token = datetime.now(),
                expires = auth_json["data"]["expires"]
            )
            cuenta.save()

        self.access_token = cuenta.access_token
        print("Initialized Zistemo with access token:: "+self.access_token)
    
    def auth_zistemo(self):
        url = settings.ZISTEMO_API_URL+"/sivale/login"
        auth_data = {"email": settings.ZISTEMO_USER_EMAIL, "password": settings.ZISTEMO_USER_PASSWORD}
        return self.rest.post(url=url+"?api_dev_key="+self.api_dev_key,data=auth_data)
    
    def refrescar_token(self, access_token, fecha_creacion, expire_date):

        current_datetime_utc = datetime.now(pytz.utc)
        token_datetime_utc = expire_date
        if current_datetime_utc>token_datetime_utc:
            print("Intentando refrescar el token")
            auth_json = self.auth_zistemo()
            return {"access_token":auth_json["data"]["access_token"], "se_actualizo": True, "expires": auth_json["data"]["expires"]}
        else:
            print("Access token valido")
            return {"access_token":access_token, "se_actualizo": False}
        
    def recuperar_reporte_dia(self, fecha):

        return
    
    def listar_proyectos(self):
        url = settings.ZISTEMO_API_URL+"/sivale/projects"
        res = self.rest.get(url=url, query_params_map=None, bearer_token=self.access_token, api_dev_key=self.api_dev_key)
        if "success" in res and res["success"]:
            return res["data"]
        return []
    
    def listar_usuarios(self):
        url = settings.ZISTEMO_API_URL+"/sivale/timesheet/users"
        res = self.rest.get(url=url, query_params_map=None, bearer_token=self.access_token, api_dev_key=self.api_dev_key)
        if "success" in res and res["success"]:
            return res["data"]
        return []
    
    def listar_time_entries(self, fecha_objetivo, usuario_id):
        url = settings.ZISTEMO_API_URL+"/sivale/timesheet/list"

        params = {"date_from": fecha_objetivo, "date_to":fecha_objetivo, "user_id": usuario_id}
        res = self.rest.get(url=url, query_params_map=params, bearer_token=self.access_token, api_dev_key=self.api_dev_key)
        if "success" in res and res["success"]:
            return res["data"]
        return []