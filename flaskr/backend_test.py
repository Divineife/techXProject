from flaskr.backend import Backend
import pytest
from unittest.mock import MagicMock, patch
# TODO(Project 1): Write tests for Backend methods.


class Testback_end:
    'This includes test to make sure all of the methods inside of our backend are given the correct outputs without using and dependencies'

    @pytest.fixture(scope="class", autouse=True)
    def list_blobs(self):
        list_blobs = MagicMock()
        return list_blobs

    @pytest.fixture(scope="class", autouse=True)
    def bucket(self):
        blob = MagicMock()
        return blob

    @pytest.fixture(scope="class", autouse=True)
    def storage_client(self, list_blobs, bucket):
        storage_client = MagicMock()
        storage_client.list_blobs.return_value = list_blobs
        storage_client.bucket = bucket
        return storage_client
    
    @pytest.fixture(scope="class", autouse=True)
    def get_blob(self):
        get_blob = MagicMock()
        return get_blob

    @pytest.fixture(scope="class", autouse=True)
    def wiki_users_comments(self,get_blob):
        wiki_users_comments = MagicMock()
        wiki_users_comments.get_blob.return_value = get_blob
        return wiki_users_comments
    
    
    @pytest.fixture(scope="class", autouse=True)
    def json(self,get_blob):
        json = MagicMock()
        return json
        
    @pytest.fixture(scope="class", autouse=True)
    def passwordIn(self):
        passwordIn = MagicMock()
        passwordIn.encode.return_value = "Hello123"
        return passwordIn

    @pytest.fixture(scope="class", autouse=True)
    def blake2b(self, passwordIn):
        blake2b = MagicMock()
        return blake2b

    @pytest.fixture(scope="class", autouse=True)
    def hexdigest(self):
        hexdigest = MagicMock()
        return hexdigest

    @pytest.fixture(scope="class", autouse=True)
    def hashlib(self, hexdigest, blake2b):
        hashlib = MagicMock()
        hashlib.blake2b.return_value = blake2b
        hashlib.blake2b.return_value.hexdigest.return_value = hexdigest
        return hashlib

    @pytest.fixture(scope="class", autouse=True)
    def lower(self):
        lower = MagicMock()
        return lower

    @pytest.fixture(scope="class", autouse=True)
    def read(self):
        read = MagicMock()
        return read

    @pytest.fixture(scope="class", autouse=True)
    def f(self, read):
        f = MagicMock()
        return f

    @pytest.fixture(scope="class", autouse=True)
    def blob(self, f):
        blob = MagicMock()
        blob.open.return_value.__enter__.return_value = f
        return blob

    @pytest.fixture(scope="class", autouse=True)
    def authors_images(self, blob):
        authors_images = MagicMock()
        authors_images.blob.return_value = blob
        return authors_images

    @pytest.fixture(scope="class", autouse=True)
    def decode(self):
        decode = MagicMock()
        return decode

    def download_as_string(self, decode):
        download_as_string = MagicMock()
        download_as_string.decode.return_value = decode
        return download_as_string

    @pytest.fixture(scope="class", autouse=True)
    def get(self):
        get = MagicMock()
        get.return_value = "TechExchange"
        return get

    @pytest.fixture(scope='class', autouse=True)
    def metadata(self, get):
        metadata = MagicMock()
        metadata.get.return_value = "TechExchange"
        return metadata

    def BytesIO(self, contain_script_bytes):
        BytesIO = MagicMock()
        BytesIO.return_value = contain_script_bytes
        return contain_script_bytes

    @pytest.fixture(scope="class", autouse=True)
    def blobs_list(self):
        return []

    @pytest.fixture(scope="class", autouse=True)
    def session(self):
        session = MagicMock()
        return session

    
    def blob1(self, object_name, contained_script, file, blob, blobs_list, read,
              hashlib, metadata, metadata_data, content_type=False):
        if type(blob.download_as_string()) != str:
            blob.download_as_string.return_value.decode.return_value = contained_script
        blob.name = object_name
        if content_type is not False: blob.content_type = content_type
        blob.contains = (object_name, contained_script)
        blobs_list.append(blob.contains)
        blob.upload_from_file = file
        blob.delete.return_value = contained_script.replace(contained_script, "")        
        blob.upload_from_string.return_value = contained_script
        blob.read.return_value = contained_script
        hashlib.blake2b.return_value.hexdigest.return_value = contained_script
        blob.metadata = metadata
        blob.metadata.get.return_value = metadata_data
        return blob

    def backend(self, storage_client, wiki_name, authors_images, password_name,
                hashlib, session ,comment_bucket = True, json_comments = True,json=False):
        return Backend(storage_client, wiki_name, authors_images, self.BytesIO,
                       password_name, hashlib, session,comment_bucket, json_comments,json)


    def test_get_wiki_page_fail(self, blob, storage_client, list_blobs,
                                blobs_list, bucket, read, hashlib, metadata):
        """
        This method tests if a wiki_page_fails to load.
        """
        storage_client.list_blobs.return_value = [
            self.blob1('ads_file', 'Hello Ads', '/file/ads', blob, blobs_list,
                       read, hashlib, metadata, {'user': 'dfaleye'})
        ]
        ans = self.backend(storage_client, 'Ads', False, False, False,
                           self.session).get_wiki_page('ads_file_not_found')

        storage_client.list_blobs.assert_called_with('Ads')
        assert blob.name == 'ads_file'
        assert ans == None
        assert blob.assert_called_once

    def test_get_all_page(self, blob, storage_client, list_blobs, blobs_list,
                          bucket, read, hashlib, metadata):
        """
        This method tests if the page that renders all pages loads up properly
        """
        blobs_list.clear()
        storage_client.list_blobs.return_value = [
            self.blob1('Hello Sds', 'Hello Sds', '/file/sds', blob, blobs_list,
                       read, hashlib, metadata, "TechExchange"),
            self.blob1('Hello Sds', 'Hello Sds section f', '/file/sds', blob,
                       blobs_list, read, hashlib, metadata, "TechExchange")
        ]
        pages_list = self.backend(storage_client, 'Sds', False, False, False,
                                  self.session).get_all_page_names()

        storage_client.list_blobs.assert_called_with('Sds')
        assert pages_list == {
            "TechExchange": ['Hello Sds', 'Hello Sds'],
            'Internships': [],
            'Clubs': [],
            'Events': [],
            'Other': []
        }
        assert blob.assert_called_once

    def test_upload(self, blob, storage_client, list_blobs, blobs_list, bucket,
                    read, hashlib, metadata, session):
        blobs_list.clear()
        storage_client.list_blobs.return_value = self.blob1(
            'Sds_file', 'Hello Sds', '/file/sds', blob, blobs_list, read,
            hashlib, metadata, {'user': 'dfaleye'})

        session.get.return_value = 'dfaleye'
        bucket.blob.return_value = ['Sds_file']

        self.backend(storage_client, 'Sds', False, False, False,
                     session).upload('/file/sds', 'Sds_file', "other")

        session.get.assert_called_with('user')
        assert blob.upload_from_file == '/file/sds'
        assert blob.name == 'Sds_file'
        assert blob.assert_called_once

    def test_get_image(self, blob, storage_client, list_blobs, blobs_list,
                       bucket, f, read, authors_images, hashlib, metadata):
        blobs_list.clear()
        authors_images.blob.return_value = self.blob1('Sds_file', 'Image',
                                                      '/file/sds', blob,
                                                      blobs_list, read, hashlib,
                                                      metadata,
                                                      {'user': 'dfaleye'})
        f.read.return_value = 'Hello Sds'
        self.backend(storage_client, 'Pds', authors_images, False, False,
                     self.session).get_image('Sds_file')

        authors_images.blob.assert_called_with('sds_file')
        blob.open.assert_called_with('rb')
        assert f.read() == 'Hello Sds'
        assert blob.upload_from_file == '/file/sds'
        assert blob.name == 'Sds_file'
        assert blob.assert_called_once

    def test_sign_in(self, blob, storage_client, list_blobs, blobs_list, bucket,
                     read, hashlib, metadata):
        storage_client.list_blobs.return_value = [
            self.blob1('fake_username', 'Hello123', '/file/passwords', blob,
                       blobs_list, read, hashlib, metadata, "TechExchange")
        ]
        ans = self.backend(storage_client, False, False, 'Passwords', hashlib,
                           self.session).sign_in('fake_username', 'Hello123')

        storage_client.list_blobs.assert_called_with('Passwords')
        blob.download_as_string().decode.assert_called_with('utf-8')
        assert blob.name.lower() == 'fake_username'
        assert ans == True

    def test_sign_up(self, blob, storage_client, list_blobs, blobs_list, bucket,
                     read, hashlib, metadata):
        blobs_list.clear()
        storage_client.list_blobs.return_value = self.blob1(
            'username_file', 'password', '/file/password', blob, blobs_list,
            read, hashlib, metadata, {'user': 'dfaleye'})
        bucket.blob.return_value = ['username_file']
        self.backend(storage_client, 'password', False, 'Passwords', hashlib,
                     self.session).sign_up('/file/password', 'file/password')
        storage_client.list_blobs.assert_called_with('Passwords')
        assert blob.upload_from_file == '/file/password'
        assert blob.name == 'username_file'
        assert blob.assert_called_once


    def test_delete(self, blob, storage_client, list_blobs, blobs_list, bucket,
                    read, hashlib, metadata, session):
        storage_client.list_blobs.return_value = [
            self.blob1('Sds_file', 'Hello Sds', '/file/sds', blob, blobs_list,
                       read, hashlib, metadata, {'user': 'dfaleye'})
        ]

        session.get.return_value = 'dfaleye'
        self.backend(storage_client, 'password', False, 'Passwords', hashlib,
                     session).delete('Sds_file')

        assert blob.delete() == ""
        session.get.assert_called_with('user')
        blob.metadata.get.assert_called_with('user_id')

    def test_check_user(self, blob, storage_client, list_blobs, blobs_list,
                        bucket, read, hashlib, metadata, session):
        """
        This is the test for the check_user method in backend.py
        """
        session.get.return_value = 'dfaleye'
        condition = self.backend(storage_client, 'password', False, 'Passwords',
                                 hashlib,
                                 session).check_user('Sds_file', 'dfaleye')
        session.get.assert_called_with('user')
        assert condition == True

    def test_get_author(self, blob, storage_client, list_blobs, blobs_list,
                        bucket, read, hashlib, metadata, session):
        storage_client.list_blobs.return_value = [
            self.blob1('Sds_file', 'Hello Sds', '/file/sds', blob, blobs_list,
                       read, hashlib, metadata, {'user': 'dfaleye'})
        ]

        session.get.return_value = 'dfaleye'

        self.backend(storage_client, 'password', False, 'Passwords', hashlib,
                     session).get_author('Sds_file')
        blob.metadata.get.assert_called_with('user_id')

    def test_get_wiki_page(self, blob, storage_client, list_blobs, blobs_list,
                           bucket, read, hashlib, metadata, get_blob):
        storage_client.list_blobs.return_value = [
            self.blob1('ads_file', 'Hello Ads', '/file/ads', blob, blobs_list,
                       read, hashlib, metadata, {'user': 'dfaleye'})
        ]
        ans = self.backend(storage_client, 'Ads', False, False, False,
                           self.session).get_wiki_page('ads_file')

        storage_client.list_blobs.assert_called_with('Ads')
        blob.download_as_string().decode.assert_called_with('utf-8')
        assert blob.name == 'ads_file'
        assert ans == 'Hello Ads'
        assert blob.assert_called_once

    def test_get_categories(self, blob, storage_client, list_blobs, blobs_list,
                            bucket, read, hashlib, metadata):
        categories = self.backend(storage_client, False, False, False, False,
                                  False).get_categories()

        assert categories == [
            "TechExchange", "Internships", "Clubs", "Events", "Other"
        ]

    def test_get_page_category(self, blob, storage_client, list_blobs,
                               blobs_list, bucket, read, hashlib, metadata,
                               get_blob):
        storage_client.bucket.return_value = bucket
        bucket.get_blob.return_value = blob
        blob.metadata.get.return_value = "TechExchange"

        page_category = self.backend(storage_client, 'Sds', False, False, False,
                                     False).get_page_category("Hello Sds")

        assert page_category == "TechExchange"
        assert blob.assert_called_once

    
    def test_get_commentbucket(self, blob, storage_client, list_blobs, blobs_list, bucket, read,hashlib, metadata, wiki_users_comments, authors_images, json,session):
        wiki_users_comments.get_blob.return_value = self.blob1('Sds_file', str({'ADS':{'A':['First ever comment']}}),
                                                      '/file/sds', blob,
                                                      blobs_list, read, hashlib, metadata,
                                                      "TechExchange", "application/json")
        json.loads.return_value = {'ADS':{'A':['First ever comment']}}
        blob.download_as_string.return_value = str({'ADS':{'A':['First ever comment']}})
        json_object = self.backend(storage_client, 'Pds', authors_images, False,
                     False,session,wiki_users_comments, 'Mock_Comments',json).get_commentbucket()
        
        wiki_users_comments.get_blob.assert_called_with('Mock_Comments')
        json.loads.assert_called_with(str({'ADS':{'A':['First ever comment']}}))
        assert json_object == {'ADS':{'A':['First ever comment']}}
    
    def test_get_commentbucket_Notjson(self, blob, storage_client, list_blobs, blobs_list, bucket, read,hashlib, metadata, wiki_users_comments, authors_images, json, session):
        wiki_users_comments.get_blob.return_value = self.blob1('Sds_file', str({'ADS':{'A':['First ever comment']}}),
                                                      '/file/sds', blob,
                                                      blobs_list, read, hashlib, metadata,
                                                      "TechExchange", "application")
        json.loads.return_value = {'ADS':{'A':['First ever comment']}}
        json_object = self.backend(storage_client, 'Pds', authors_images, False,
                     False, session,wiki_users_comments, 'Mock_Comments',json).get_commentbucket()
        
        wiki_users_comments.get_blob.assert_called_with('Mock_Comments')
        assert json_object == {}

    def test_add_comment(self, blob, storage_client, list_blobs, blobs_list, bucket, read,hashlib, metadata, wiki_users_comments, authors_images, json, session):
        wiki_users_comments.get_blob.return_value = self.blob1('Sds_file', str({'ADS':{'A':['First ever comment']}}),
                                                      '/file/sds', blob,
                                                      blobs_list, read, hashlib, metadata,
                                                      "TechExchange", "application")
        json.dumps.return_value = str({'ADS':{'A':['First ever comment']}})
        json_object = self.backend(storage_client, 'Pds', authors_images, False,
                     False, session, wiki_users_comments, 'Mock_Comments',json).add_comment({'ADS':{'A':['First ever comment']}})
        
        wiki_users_comments.get_blob.assert_called_with('Mock_Comments')
        assert json_object == str({'ADS':{'A':['First ever comment']}})
        json.dumps.assert_called_with({'ADS':{'A':['First ever comment']}})
        blob.upload_from_string.assert_called_with( str({'ADS':{'A':['First ever comment']}}), content_type = 'application/json')
