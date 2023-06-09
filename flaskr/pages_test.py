from flaskr import create_app
from flask import session
from flaskr.pages import make_endpoints
import unittest
from unittest.mock import MagicMock
import pytest
from unittest.mock import patch
from flaskr.backend import Backend


# See https://flask.palletsprojects.com/en/2.2.x/testing/
# for more info on testing
#TODO(Project 1): Write tests for other routes.
#@pytest.mark.usefixtures("client")
class Test_pages:
    'This includes test to make sure all of the routes in page.py will take us to the correct location depending on the login state'

    @pytest.fixture(scope="class", autouse=True)
    def app(self):
        app = create_app({
            'TESTING': True,
        })
        return app

    @pytest.fixture(scope="class", autouse=True)
    def client(self, app):
        return app.test_client()

    def test_home_page(self, client):
        with client:
            server_response = client.get('/')
            assert server_response.status_code == 200
        assert b'Welcome to the Wiki!' in server_response.data

    @patch.object(
        Backend,
        'get_all_page_names',
        return_value=['hello', 'iterate', 'through', 'this', 'mock_object'])
    def test_pages_page(self, mock_get_all_page_names, client):
        with client.get('/pages/') as server_response:
            assert server_response.status_code == 200
        assert b'Pages contained in this Wiki' in server_response.data

    @patch.object(
        Backend,
        'get_wiki_page',
        return_value=['hello', 'iterate', 'through', 'this', 'mock_object'])
    @patch.object(Backend, 'get_author', return_value='usrid')
    @patch.object(Backend, 'check_user', return_value=True)
    @patch.object(Backend, 'get_page_category', return_value="TechExchange")
    @patch.object(
        Backend,
        'get_commentbucket',
        return_value={'ADS_test': {
            'user_test': ['Comment for testing']
        }})
    def test_page_in_pages(self, mock_get_wiki_page, mock_get_author,
                           mock_checkUser, mock_get_page_category,
                           mock_get_commentbucket, client):
        with client.get('/pages/5') as server_response:
            assert server_response.status_code == 200
        assert b'Welcome to' in server_response.data

    def test_about_page(self, client):
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
    def test_login_page_put_correct(self, mock_signin, client):
        server_response = client.post('/login',
                                      data={
                                          "username": "flask",
                                          'password': 'test'
                                      })
        assert server_response.status_code == 302
        assert b'"/"' in server_response.data

    @patch.object(Backend, 'sign_in', return_value=False)
    def test_login_page_put_incorrect(self, mock_signin, client):
        server_response = client.post('/login',
                                      data={
                                          "username": "flask",
                                          'password': 'test'
                                      })
        assert server_response.status_code == 302
        assert b'"login"' in server_response.data

    @patch.object(Backend, 'sign_up', return_value=True)
    def test_signup_page_put_correct(self, mock_signin, client):
        server_response = client.post('/signup',
                                      data={
                                          "username": "flask",
                                          'password': 'test'
                                      })
        assert server_response.status_code == 302
        assert b'"/login"' in server_response.data

    @patch.object(Backend, 'sign_up', return_value=False)
    def test_signup_page_put_incorrect(self, mock_signin, client):
        server_response = client.post('/signup',
                                      data={
                                          "username": "flask",
                                          'password': 'test'
                                      })
        assert server_response.status_code == 302
        assert b'"/signup"' in server_response.data

    def test_logout_page_get_not_loggedin(self, client):
        server_response = client.get('/logout')
        assert server_response.status_code == 302
        assert b'"/login"' in server_response.data

    def test_upload_page_not_loggedin(self, client):
        server_response = client.get('/upload')
        assert server_response.status_code == 302
        assert b'"login"' in server_response.data

    def test_upload_page(self, client):
        with client.session_transaction() as fake_session:
            fake_session["user"] = 'danny'
        server_response = client.get('/upload', data={"username": "flask"})
        assert server_response.status_code == 200
        assert b"Upload" in server_response.data

    def test_login_page_get_loggedin(self, client):
        server_response = client.get('/login')
        assert server_response.status_code == 302
        assert b'"/"' in server_response.data

    def test_signup_page_get_loggedin(self, client):
        server_response = client.get('/signup')
        assert server_response.status_code == 302
        assert b'"/"' in server_response.data

    def test_logout_page_get_loggedin(self, client):
        server_response = client.get('/logout')
        assert server_response.status_code == 302
        assert b'"/login"' in server_response.data

    @patch.object(
        Backend,
        'get_commentbucket',
        return_value={'ADS_test': {
            'user_test': ['Comment for testing']
        }})
    @patch.object(
        Backend,
        'add_comment',
        return_value={'ADS_test': {
            'user_test': ['Comment for testing']
        }})
    @patch.object(
        Backend,
        'get_wiki_page',
        return_value=['hello', 'iterate', 'through', 'this', 'mock_object'])
    def test_page_inPages_POST(self, mock_get_commentbucket, mock_add_comment,
                               mock_get_wiki_page, client):
        with client.session_transaction() as fake_session:
            fake_session["user"] = 'danny'
        server_response = client.post('/pages/ADS')
        assert server_response.status_code == 302
        assert b'ADS' in server_response.data

    @patch.object(Backend, 'delete', return_value=True)
    def test_delete(self, mock_delete, client):
        server_response = client.post("/delete/page")
        assert server_response.status_code == 302
