import requests
import datetime
import urllib
import time

fecha_inicial = "2020-01-01"
fecha_final = "2023-12-31"

url = "http://127.0.0.1:8000/reporte/"

#Iterar los dias e irle pegando al api
date_inicial = datetime.datetime.strptime(fecha_inicial, "%Y-%m-%d")
date_final =  datetime.datetime.strptime(fecha_final, "%Y-%m-%d")
dias = 0
numero_pdfs_creados = 0
while date_inicial<=date_final:

    print("Enviando fecha para PDF:: "+str(date_inicial))
    #Envio al api local
    str_date_inicial = date_inicial.strftime("%d/%m/%Y")
    response = requests.post(url, {"fecha":str_date_inicial, "client_id": "Groupe Up"})
    res = response.json()

    print("Recibi respuesta:: "+str(res))
    
    date_inicial = date_inicial + datetime.timedelta(days=1)
    dias = dias + 1

    if 'numero_pdfs_creados' in res:
        numero_pdfs_creados = numero_pdfs_creados + res['numero_pdfs_creados']
        print("PDFs creados hasta ahora:: "+str(numero_pdfs_creados))

print("Finalizados "+str(dias)+" de procesamiento PDF, se crearon un total de "+str(numero_pdfs_creados)+" PDFs")