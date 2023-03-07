from flaskr import create_app
import unittest 
import pytest

# See https://flask.palletsprojects.com/en/2.2.x/testing/ 
# for more info on testing
#TODO(Project 1): Write tests for other routes.
#@pytest.mark.usefixtures("client")
class Test_pages: 
    'This includes test to make sure all of the methods for our pages are up and running'

    @pytest.fixture(scope="class", autouse=True)
    def app(self):
        app = create_app({
            'TESTING': True,
        })
        return app
    
    @pytest.fixture(scope="class",  autouse=True)
    def client(self,app):
        return app.test_client()

    def test_home_page(self,client):  
        with client:
            server_response = client.get('/')
            assert server_response.status_code == 200
        assert b'Welcome to the Wiki!' in server_response.data
    
    def test_upload_page(self,client):
        with client.get('/upload') as server_response:
            assert server_response.status_code == 302
    
    def test_pages_page(self,client):
        with client.get('/pages/') as server_response:
            assert server_response.status_code == 200

    def test_page_in_pages(self,client):
        with client.get('/pages/5') as server_response:
        #server_response = client.get('/pages/1')
            assert server_response.status_code == 200

    def test_about_page(self,client):
        with client.get('/about') as server_response:
            assert server_response.status_code == 200
        assert b'Daniel Oluwarotimi' in server_response.data
        