# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage
import pathlib
import os
from io import BytesIO
from flask import request
import hashlib
import json
"""The backend to connect to the Google Cloud to upload and read information

The pages.py will call functions inside this Backend class to be able to verify or get information that the user prompted. The Backend talks to our google bucket that will read or upload from certain files that we specified. It will also check to verify user inputs are valid when given.

Typical usage example:

  valid = sign_in(username, password) #return True if credentials is Valid else False
  upload(file, name)
  content = get_wiki_page(page_nam)
  valid = sign_up(username, password) #return True if credentials is Valid else False(in this case the username has been taking)
  page_names = get_all_page_names()
"""


class Backend:

    def __init__(self,
                 Mock_storage_client=False,
                 Mock_bucket_name=False,
                 Mock_authors_images=False,
                 Mock_BytesIO=False,
                 Mock_passwords_bucket=False,
                 Mock_hashlib=False,
                 Mock_comment_bucket= False):

        self.storage_client = storage.Client(
        ) if Mock_storage_client is False else Mock_storage_client

        self.wiki_view = self.storage_client.bucket('wiki_view')
        self.bucket_name = 'wikis_viewer' if Mock_bucket_name is False else Mock_bucket_name

        self.wiki_password = self.storage_client.bucket('wiki_passwords')
        self.password_bucket = 'wiki_passwords' if Mock_passwords_bucket is False else Mock_passwords_bucket
        self.hashlib = hashlib if Mock_hashlib is False else Mock_hashlib

        self.authors_images = self.storage_client.bucket(
            'authors-images'
        ) if Mock_authors_images is False else Mock_authors_images
        self.image_bucket = 'authors-images'
        self.BytesIO = BytesIO if Mock_BytesIO is False else Mock_BytesIO

        self.wiki_users_comments = self.storage_client.bucket('wiki_users_comments')
        self.comment_bucket = 'wiki_users_comments' if Mock_comment_bucket is False else Mock_comment_bucket
        self.json_comments = 'Comments'
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
        usernameIn = usernameIn.strip()
        for blob in blobs:
            if blob.name.lower() == usernameIn.lower():
                return False

        # If the username hasn't been taken, encrypt the password and upload it
        encrypted_password = self.hashlib.blake2b(
            passwordIn.encode()).hexdigest()
        blob = self.wiki_password.blob(usernameIn)
        blob.upload_from_string(encrypted_password)
        return True

    def sign_in(self, usernameIn, passwordIn):
        blobs = self.storage_client.list_blobs(self.password_bucket)
        passwordIn_encryption = self.hashlib.blake2b(
            passwordIn.encode()).hexdigest()
        for blob in blobs:
            if blob.name.lower() == usernameIn.lower():
                print(blob.name.lower())
                return blob.download_as_string().decode(
                    'utf-8') == passwordIn_encryption

    def get_image(self, name):
        blob = self.authors_images.blob(name.lower())
        with blob.open('rb') as f:
            output = f.read()
            return self.BytesIO(output)
        #map_author_2_image[blob.name.lower()] = blob.public_url
        #return map_author_2_image

    
    def checkPage_in_commentbucket(self):
        blobs = self.storage_client.list_blobs(self.comment_bucket)
        for blob in blobs:
            if blob.name == self.json_comments:
                return blob.download_as_string()
        return False


    def add_comment(self, page_comments, page_name,user_name):
        blob = self.wiki_users_comments.blob(self.json_comments)
        #with blob.open("w") as write_file:
        wiki_pages = json.loads(blob.download_as_string())

        page = wiki_pages[page_name]
        page[user_name].append(page_comments)
        blob.upload_from_string(page_comments, content_type='application/json')

    def get_comment(self, post):
        pass
        