# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage
import pathlib
import os
from io import BytesIO
from flask import request, session
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
                 Mock_comment_bucket= False,
                 Mock_session=False):

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
        self.session = session if Mock_session is False else Mock_session

        self.wiki_users_comments = self.storage_client.bucket(
            'wiki_users_comments')
        self.comment_bucket = 'wiki_users_comments' if Mock_comment_bucket is False else Mock_comment_bucket
        self.json_comments = 'Comments'

    def get_wiki_page(self, name):
        blobs = self.storage_client.list_blobs(self.bucket_name)
        for blob in blobs:
            if blob.name == name:
                print('BLOB', blob)
                return blob.download_as_string().decode('utf-8')

    def get_all_page_names(self):
        # This method will return a dictionary with the category as the keys and the name of the pages as the values. Any page with no category inside their metadata will be put in the "Other" category.
        categories = self.get_categories()
        categories_w_pages = {}
        for category in categories:
            categories_w_pages[category] = []

        blobs_pages = self.storage_client.list_blobs(self.bucket_name)
        for blob in blobs_pages:
            page_name = blob.name
            page_category = blob.metadata.get("category")
            if page_category is None:
                page_category = "Other"
            categories_w_pages[page_category].append(page_name)

        return categories_w_pages

    def upload(self, file, name, category):
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(name)
        blob.metadata = {
            'user_id': self.session.get('user'),
            'category': category
        }
        blob.upload_from_file(file)

    def get_author(self, name):
        """
        THis method returns the username of the author of a page
        """
        bucket = self.storage_client.bucket(self.bucket_name)
        cur_blob = bucket.get_blob(name)
        if cur_blob:
            return cur_blob.metadata.get('user_id')

    def check_user(self, name, page_username):
        """
        THis method returns a boolean that indicates whether or not a user posted a page
        """
        #checks if user is the author of a page
        username = self.session.get('user')
        if username == page_username:
            return True
        return False

    def delete(self, name):
        """
        THis method deletes the wikipage.
        """
        blobs = self.storage_client.list_blobs(self.bucket_name)
        for blob in blobs:
            if blob.name == name:
                cur_page = blob
                user_id = self.session.get('user')

                if user_id and cur_page.metadata.get('user_id') == user_id:
                    cur_page.delete()
                    return True
                else:
                    return False
        return False

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
                return blob.download_as_string().decode(
                    'utf-8') == passwordIn_encryption

    def get_image(self, name):
        blob = self.authors_images.blob(name.lower())
        with blob.open('rb') as f:
            output = f.read()
            return self.BytesIO(output)
    
    def checkPage_in_commentbucket(self):
        blobs = self.storage_client.list_blobs(self.comment_bucket)
        for blob in blobs:
            if blob.name == self.json_comments:
                return blob.download_as_string()
        return False

    def add_comment(self, page_comments, page_name, user_name):
        blob = self.wiki_users_comments.blob(self.json_comments)
        #with blob.open("w") as write_file:
        wiki_pages = json.loads(blob.download_as_string())
        page = wiki_pages[page_name]
        page[user_name].append(page_comments)
        blob.upload_from_string(page_comments, content_type='application/json')

    def get_comment(self, post):
        pass

    def get_categories(self):
        # Returns a list of all the categories that have been pre-determined
        categories = ["TechExchange", "Internships", "Clubs", "Events", "Other"]
        return categories

    def get_page_category(self, name):
        # Receives the name of a page then checks the pages metadata and returns the category assigned inside the metadata or "Other" if metadata is missing.
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.get_blob(name)
        if blob is not None:
            cur_page_category = blob.metadata.get("category")
            if cur_page_category == None:
                return "Other"
            else:
                return cur_page_category
