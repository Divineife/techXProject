# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage
import pathlib
import os
from flask import request
import hashlib


class Backend:
    def __init__(self):

        self.storage_client = storage.Client()

        self.wiki_view = self.storage_client.bucket('wiki_view')
        self.bucket_name = 'wikis_viewer'

        self.wiki_password = self.storage_client.bucket('wiki_passwords')
        self.password_bucket = 'wiki_passwords'
        
    def get_wiki_page(self, name):
        blobs = self.storage_client.list_blobs(self.bucket_name)
        for blob in blobs:
            if blob.name == name:
                return blob.download_as_string().decode('utf-8')

    def get_all_page_names(self):
        blobs = self.storage_client.list_blobs(self.bucket_name)
        blob_names = []
        for blob in blobs:
            blob_names.append(blob)
        return blob_names

    def upload(self, file, name):
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(name)
        blob.upload_from_file(file)

    def sign_up(self, usernameIn, passwordIn):
        # Check if username is already being used
        blobs = self.storage_client.list_blobs(self.password_bucket)
        for blob in blobs:
            if blob.name.lower() == usernameIn.lower():
                return False
        
        # If the username hasn't been taken, encrypt the password and upload it
        encrypted_password = hashlib.blake2b(passwordIn.encode()).hexdigest()
        blob = self.wiki_password.blob(usernameIn)
        blob.upload_from_string(encrypted_password)
        return True

    def sign_in(self, usernameIn, passwordIn):
        blobs = self.storage_client.list_blobs(self.password_bucket)
        passwordIn_encryption = hashlib.blake2b(passwordIn.encode()).hexdigest()
        for blob in blobs:
            if blob.name.lower() == usernameIn.lower(): 
                return blob.download_as_string().decode('utf-8') == passwordIn_encryption

    def get_image(self):
        pass
