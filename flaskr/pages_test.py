from flaskr import create_app
import unittest 
import pytest
from unittest.mock import patch
from flaskr.backend import Backend

# See https://flask.palletsprojects.com/en/2.2.x/testing/ 
# for more info on testing
'''
@pytest.fixture(scope="class", autouse=True)
def app():
    app = create_app({
        'TESTING': True,
    })
    return app


@pytest.fixture(scope="class",  autouse=True)
def client(app):
    return app.test_client()
'''
'''
# TODO(Checkpoint (groups of 4 only) Requirement 4): Change test to
# match the changes made in the other Checkpoint Requirements.
'''
'''
def test_home_page(client):
    with client:
        resp = client.get("/")
        assert resp.status_code == 200
    assert b"Welcome to the Wiki!" in resp.data
'''
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
            assert server_response.status_code == 200
    
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
    
    def test_login_page_get(self, client):
        server_response = client.get('/login')
        assert server_response.status_code == 200
        assert b'Login' in server_response.data

    def test_signup_page_get(self, client):
        server_response = client.get('/signup')
        assert server_response.status_code == 200
        assert b'Sign Up' in server_response.data

    @patch.object(Backend, 'sign_in', return_value=True)
    def test_login_page_put_correct(mock_sign_in, client):
        server_response= client.post('/login', data={"username": "flask", 'password':'test'})
        assert server_response.status_code == 200
        assert b'Incorrect Password or Username' in server_response.data