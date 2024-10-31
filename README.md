ML-Lighthouse - API
====================

## Requerimientos

* Python 3.9
* Pip 3  

- - -

## Ambientación

1. Install Python 3.5+

2. Install Pip 3

3. Install virtualenv  
Se usa para crear ambientes virtuales y ejecutar la versión de Python requerida

4. Clonar el proyecto  

5. Activar el ambiente virtual  
$ source env/bin/activate

6. Instalar las librerías requeridas por el proyecto  
$ pip3 install -r requirements.txt

NOTA IMPORTANTES SOBRE librería postgresql EN AMBIENTE DE DESARROLLO:
Es posible que al final al correr el api en ambiente de desarrollo sobre todo, se arroje el error siguiente:
"Library not loaded: /usr/local/opt/openssl/lib/libssl.1.0.0.dylib"

Que es una dependencia de la librería "psycopg2", la librería de postgresql para python. Para repararlo, corra el siguiente upgrade de la librería:

$ pip3 install psycopg2 --upgrade


7. Configurar conexión a base de datos (MySQL)  
/zistemo_automation_api/my.cnf

8. Crear la base de datos y aplicar las migraciones  
$ python3 manage.py makemigrations zistemo_automation_api  
$ python3 manage.py migrate  


9. Crear un administrator (IMPORTANTE)  
Para crear un administrador, corra el siguiente comando:
$ python3 manage.py createsuperuser --email admin@admin.com --username admin  
(Console input) PASSWORD: XXXXXX

Después de ello genere su entrada en la tabla "perfil" y asigne el grupo "superadmin" usando la tabla auth_user_groups, esto le dará acceso a las funciones de administración dentro de la app web beserva

11. Correr el servidor  
 python3 manage.py runserver  

12. Incrementar el tamaño del la columna first_name de la tabla 'auth_user' a 200 chars (No se puede hacer desde una migración de Django)

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  -

## API Contract (postman)

https://www.getpostman.com/collections/1c3588836608e021702f

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  -

## Configuraciones adicionales en ambientes [qa, staging, prod]

Aparte de las configuraciones generales del ambiente local, es requerido ejecutar los siguientes comandos, para preparar los ambientes.

1. Crear el folder ** media ** usado para subir archivos  
$ mkdir media  

2. Dar a Apache permisos de escritura para el folder mediafolder (en caso de no usar google cloud)
$ chmod -R 775 media  
$ chown  -R  jenkins:www-data media  

3. Agregar el nuevo dominio al archivo settings.py file (/zistemo_automation_api/settings.py)
Ejemplo: ALLOWED_HOSTS = ['127.0.0.1','api.domain.com']  

4. Crear carpeta para guardar los logs  (en caso de no usar google cloud)
$ mkdir logs
$ chmod -R 775 logs  
$ chown  -R  jenkins:www-data logs  

## Despliegue en producción - Google App Engine

1. Generar los archivos estáticos de django (Solo se requiere en el primer deploy)  
$ python3 manage.py collectstatic

2. Conectarse a la BD de prod mediante un proxy (Previamente instalar sdk de google cloud)    
$ ./cloud_sql_proxy -instances="<instancia-gcloud>"=tcp:3307

3. Configurar en el archivo my.cnf la conexión hacia esta BD  

4. Aplicar las migraciones del proyecto

5. Configurar en el archivo settings.py la conexión a la BD de google cloud (esta comentada)  

6. Ejecutar el comando de publicación  
$ gcloud app deploy -v {ULTIMA_VERSION_DESPLEGADA}  



 Para la parte de Google Cloud, hay que exportar a una variable local para poder comunicarse con el bucket en la nube, ejemplo:

 export GOOGLE_APPLICATION_CREDENTIALS=<ruta>beserva_storage.json (el json se obtiene de gcloud: https://cloud.google.com/iam/docs/creating-managing-service-account-keys?hl=es_419, pero también esta en este proyecto)

URL para obtener token de ML:
https://auth.mercadolibre.com.mx/authorization?response_type=code&client_id=3125500230099140&redirect_uri=https://api-dot-ml-lighthouse.uc.r.appspot.com/

Para cambiar el code por access token
https://api-dot-ml-lighthouse.uc.r.appspot.com/?code=TG-66bbfc93fd190e000187b9ef-157717066
