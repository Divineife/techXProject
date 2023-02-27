# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage

class Backend:
    def __init__(self):

        self.storage_client = storage.Client()

        self.wiki_view = self.storage_client.bucket('wiki_view')
        self.wiki_password = self.storage_client.bucket('wiki_passwords')
        
    def get_wiki_page(self, name):
        pass

    def get_all_page_names(self):
        pass

    def upload(self):
        pass

    def sign_up(self, username, password):
        name = self.wiki_password.blob('Bob.txt')
        print('name', name)
        return True

    def sign_in(self):
        pass

    def get_image(self):
        pass

