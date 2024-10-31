import datetime
from django.conf import settings
import os
from django.http import HttpResponse, Http404
from google.cloud import storage
from zistemo_automation_api.data_utils import DataUtils

class GoogleCloudBucketStorage():

    def delete_file(self, file_name, bucket_name=None):
        if not bucket_name:
            if settings.GOOGLE_CLOUD_BUCKET:
                bucket_name = settings.GOOGLE_CLOUD_BUCKET
            else:
                return {}
        
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.delete()

        return True
    
    def save_file(self, file_object, file_name, container_folder=None, prefix_folder=None, bucket_name=None,):

        
        if not bucket_name:
            if settings.GOOGLE_CLOUD_BUCKET:
                bucket_name = settings.GOOGLE_CLOUD_BUCKET
            else:
                return {}


        content_type = DataUtils.get_file_mimetype(file_name)

        if container_folder:
            file_name = container_folder+"/"+file_name

        if prefix_folder:
            file_name = prefix_folder + "/" + file_name

        file_stream = file_object.read()

        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_name)

        blob.upload_from_string(
            file_stream,
            content_type=content_type)

        url = blob.public_url

        return {"public_url": url}

    def save_file_as_string(self, file_string, file_name, container_folder=None, prefix_folder=None, bucket_name=None,):

        
        if not bucket_name:
            if settings.GOOGLE_CLOUD_BUCKET:
                bucket_name = settings.GOOGLE_CLOUD_BUCKET
            else:
                return {}


        content_type = DataUtils.get_file_mimetype(file_name)

        if container_folder:
            file_name = container_folder+"/"+file_name

        if prefix_folder:
            file_name = prefix_folder + "/" + file_name

        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_name)

        blob.upload_from_string(
            file_string,
            content_type=content_type)

        url = blob.public_url

        return {"public_url": url}

    def save_file_from_filename(self, full_file_path, file_name, container_folder, prefix_folder, bucket_name):

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        if container_folder:
            file_name = container_folder+"/"+file_name

        if prefix_folder:
            file_name = prefix_folder + "/" + file_name
            
        blob = bucket.blob(file_name)
        print("Subiendo a google cloud storage, bucket("+str(bucket_name)+"), file_name("+file_name+") :: "+str(full_file_path))
        blob.upload_from_filename(full_file_path)

        url = blob.public_url

        print("PUBLIC URL RCVD: "+str(url))
        return {"public_url": url}