# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage
import pathlib
import os
from io import BytesIO
from flask import request
import hashlib
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
                 Mock_categories_bucket=False):

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

        self.wiki_categories = self.storage_client.bucket('categories')
        self.categories_bucket = 'wiki_categories' if Mock_categories_bucket is False else Mock_categories_bucket

    def get_wiki_page(self, name):
        blobs = self.storage_client.list_blobs(self.bucket_name)
        for blob in blobs:
            if blob.name == name:
                return blob.download_as_string().decode('utf-8')

    def get_all_page_names(self):
        blobs = self.storage_client.list_blobs(self.categories_bucket, delimiter="/", include_trailing_delimiter=True)
        # blob_names = []
        # for blob in blobs:
        #     blob_names.append(blob)
        # return blob_names

        categories = {}
        for blob in blobs:
            category = blob.name[:-1]
            print("CATEGORY:", category)
            blobs_pages = self.storage_client.list_blobs(self.categories_bucket, prefix=category)
            print("BLOBS PAGES:", blobs_pages)
            categories[category] = []
            for page in blobs_pages:
                categories[category].append(page.name)
                print("PAGE NAME", page.name)
            print("CATEGORIES:", categories)

        return categories

    def upload(self, file, name, category):
        bucket = self.storage_client.bucket(self.categories_bucket)
        blob = bucket.blob(category + "/" + name)
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

    def get_categories(self):
        blobs = self.storage_client.list_blobs(self.categories_bucket, delimiter="/", include_trailing_delimiter=True)
        categories = []
        for blob in blobs:
            category = blob.name[:-1]
            categories.append(category)
            print("CATEGORY", category)
        return categories
