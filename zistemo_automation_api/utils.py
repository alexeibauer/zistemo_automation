import random
import string
import base64
import unicodedata
import re
from datetime import datetime
from datetime import timedelta

from django.db.models import *
from zistemo_automation_api.models import *
from zistemo_automation_api.serializers import *

class Utils:

    @staticmethod
    def toLowerNoAccents(target):

        target = target.lower()
        target = target.replace("á","a")
        target = target.replace("é","e")
        target = target.replace("í","i")
        target = target.replace("ó","o")
        target = target.replace("ú","u")

        return target

    @staticmethod
    def toDateFromString(fecha, utc=-5, format='%Y-%m-%dT%H:%M:%S.%fZ'):
        fecha_target = datetime.strptime(fecha, format) + timedelta(hours=utc)
        return fecha_target

    @staticmethod
    def toStringFormattedFromString(fecha, utc=-5, format="%m/%d/%Y, %H:%M"):
        fecha_target = datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(hours=utc)
        fecha_target = fecha_target.strftime(format)
        return fecha_target

    @staticmethod
    def toStringFormattedFromDatetime(fecha, utc=-5, format="%m/%d/%Y, %H:%M"):
        fecha_target = fecha + timedelta(hours=utc)
        fecha_target = fecha_target.strftime(format)
        return fecha_target

    @staticmethod
    def randomString(stringLength=10):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

    @staticmethod
    def randomNumber(numberLength=10):
        """Generate a random number of fixed length """
        digits = string.digits
        return ''.join(random.choice(digits) for i in range(numberLength))

    @staticmethod
    def requestRawFileToB64(file):
        file_b64 = str(base64.b64encode(file.read()).decode())
        return file_b64

    @staticmethod
    def mimeFromFilename(filename):
        content_type = ""
        if '.mp4' in filename:
            content_type = "video/mp4"
        elif '.m4v' in filename:
            content_type = "video/mp4"
        else:
            content_type = "application/octet-stream"

        return content_type

    @staticmethod
    def requestFileToB64(logo):

        content_type = ""
        if '.jpg' in logo.name or '.jpeg' in logo.name:
            content_type = "data:image/jpeg;base64,"
        elif '.png' in logo.name:
            content_type = "data:image/png;base64,"

        logo_b64 = content_type+str(base64.b64encode(logo.read()).decode())

        return logo_b64

    @staticmethod
    def slugify(value, allow_unicode=False):
        value = str(value)
        if allow_unicode:
            value = unicodedata.normalize('NFKC', value)
        else:
            value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub(r'[^\w\s-]', '', value.lower())
        return re.sub(r'[-\s]+', '_', value).strip('-_')

    @staticmethod
    def uploadFile(url, file, file_storage_bridge, container_folder, carpeta_prefix, filename=None):
        if isinstance(file, str):
            print(f"existing_file: {url}")
            return file
        if url:
            print(f"deleting_file: {url}")
            try:
                file_storage_bridge.delete_file(url)
            except:
                pass
            url = None
        if file:
            print(f"uploading_file: {file.name}")
            if filename:
                response = file_storage_bridge.save_file(file, f"{filename}.{file.name.split('.')[-1]}", container_folder, carpeta_prefix)
            else:
                response = file_storage_bridge.save_file(file, file.name, container_folder, carpeta_prefix)
            url = response["public_url"]
            print(f"url: {url}")
        return url
