# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage
import pathlib, os
from flask import request

class Backend:
    def __init__(self):

        self.storage_client = storage.Client()

        self.wiki_view = self.storage_client.bucket('wiki_view')
        self.wiki_password = self.storage_client.bucket('wiki_password')
        
    def get_wiki_page(self, name):
        pass

    def get_all_page_names(self):
        pass

    def upload(self, file, name):  
            
        bucket_name = 'wikis_viewer'
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(name)
        blob.upload_from_file(file)

    def sign_up(self):
        pass

    def sign_in(self):
        pass

    def get_image(self):
        pass

