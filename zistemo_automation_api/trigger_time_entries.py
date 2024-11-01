import requests
import datetime
import urllib
import time

fecha_inicial = "2020-01-01"
fecha_final = "2023-12-31"

url = "http://127.0.0.1:8000/timesheet/"

#Iterar los dias e irle pegando al api con 510 de sleep
date_inicial = datetime.datetime.strptime(fecha_inicial, "%Y-%m-%d")
date_final =  datetime.datetime.strptime(fecha_final, "%Y-%m-%d")
dias = 0
while date_inicial<=date_final:

    print("Enviando fecha:: "+str(date_inicial))
    #Envio al api
    str_date_inicial = date_inicial.strftime("%Y-%m-%d")
    response = requests.post(url, {"fecha_timesheet":str_date_inicial})
    res = response.json()

    print("Recibi respuesta:: "+str(res))
    
    date_inicial = date_inicial + datetime.timedelta(days=1)
    dias = dias + 1
    time.sleep(12.5)

print("Finalizados "+str(dias)+" de procesamiento")