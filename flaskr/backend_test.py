from flaskr.backend import Backend
import pytest 
from unittest.mock import MagicMock
# TODO(Project 1): Write tests for Backend methods.

class Testback_end:
# note to self create a seperate class for fixture


    @pytest.fixture(scope="class", autouse=True)
    def list_blobs(self):
        list_blobs = MagicMock()
        return list_blobs
    
    @pytest.fixture(scope="class", autouse=True)
    def bucket(self):
        blob = MagicMock()
        return blob

    @pytest.fixture(scope="class", autouse=True)    
    def storage_client(self, list_blobs,bucket):
        storage_client = MagicMock() 
        storage_client.list_blobs.return_value = list_blobs
        storage_client.bucket = bucket        
        return storage_client
    
    @pytest.fixture(scope="class", autouse=True)
    def read(self):
        read = MagicMock()
        return read
    
    @pytest.fixture(scope="class", autouse=True)
    def f(self,read):
        f = MagicMock()
        return f

    @pytest.fixture(scope="class", autouse=True)
    def blob(self,f):
        blob = MagicMock()
        blob.open.return_value.__enter__.return_value = f
        return blob

    @pytest.fixture(scope="class", autouse=True)
    def authors_images(self,blob):
        authors_images = MagicMock()
        authors_images.blob.return_value = blob
        return authors_images
    

    @pytest.fixture(scope="class", autouse=True)
    def decode(self):
        decode = MagicMock()
        return decode 
    

    def download_as_string(self,decode):
        download_as_string = MagicMock()
        download_as_string.decode.return_value = decode
        return download_as_string
    
    def BytesIO(self,contain_script_bytes):
        BytesIO = MagicMock()
        BytesIO.return_value = contain_script_bytes
        return contain_script_bytes

    @pytest.fixture(scope="class", autouse=True)
    def blobs_list(self):
        return []

    def blob1(self,object_name, contained_script,file ,blob,blobs_list ,read):
        
        blob.download_as_string.return_value.decode.return_value=contained_script
        blob.name=object_name
        blob.contains= (object_name,contained_script)
        blobs_list.append(blob.contains) 
        blob.upload_from_file = file
        #print(self.BytesIO)
        blob.read.return_value = contained_script
        print(blobs_list)
        return blob    
    
    def backend(self,storage_client,wiki_name, authors_images):
        return Backend(storage_client, wiki_name, authors_images, self.BytesIO)

    def test_get_wiki_page(self, blob, storage_client, list_blobs,blobs_list, bucket,read):
        storage_client.list_blobs.return_value = [ self.blob1('ads_file', 'Hello Ads','/file/ads', blob,blobs_list, read)]
        ans = self.backend(storage_client,'Ads', False).get_wiki_page('ads_file') 
        
        storage_client.list_blobs.assert_called_with('Ads')
        blob.download_as_string().decode.assert_called_once()
        blob.download_as_string().decode.assert_called_with('utf-8')
        assert blob.name == 'ads_file'
        assert ans == 'Hello Ads'
        assert blob.assert_called_once
    
    def test_get_wiki_page_fail(self, blob, storage_client, list_blobs,blobs_list, bucket,read):
        storage_client.list_blobs.return_value = [ self.blob1('ads_file', 'Hello Ads','/file/ads', blob,blobs_list, read)]
        ans = self.backend(storage_client,'Ads', False).get_wiki_page('ads_file_not_found') 
        
        storage_client.list_blobs.assert_called_with('Ads')
        blob.download_as_string().decode.assert_called_once()
        assert blob.name == 'ads_file'
        blob.download_as_string().decode.assert_called_with('utf-8')
        assert ans == None
        assert blob.assert_called_once
    
    def test_get_all_page(self, blob, storage_client, list_blobs,blobs_list,bucket,read):
        blobs_list.clear()
        storage_client.list_blobs.return_value = [ self.blob1('Sds_file', 'Hello Sds','/file/sds',blob,blobs_list, read),self.blob1('SdsF_file', 'Hello Sds section f','/file/sds',blob,blobs_list, read) ]
        self.backend(storage_client,'Sds', False).get_all_page_names() 
        
        storage_client.list_blobs.assert_called_with('Sds')
        assert blobs_list == [('Sds_file', 'Hello Sds'), ('SdsF_file', 'Hello Sds section f')]
        assert blob.assert_called_once
    
    def test_upload(self, blob, storage_client, list_blobs,blobs_list,bucket, read):
        blobs_list.clear()
        storage_client.list_blobs.return_value = self.blob1('Sds_file', 'Hello Sds', '/file/sds',blob,blobs_list, read)
        bucket.blob.return_value = ['Sds_file']
        
        self.backend(storage_client,'Sds',False).upload('/file/sds','Sds_file')
        
        storage_client.list_blobs.assert_called_with('Sds')
        assert blob.upload_from_file == '/file/sds'
        assert blob.name == 'Sds_file'
        assert blob.assert_called_once


    def test_get_image(self, blob, storage_client, list_blobs,blobs_list,bucket,f, read,authors_images):
        blobs_list.clear()
        authors_images.blob.return_value = self.blob1('Sds_file', 'Image', '/file/sds',blob,blobs_list, read)
        f.read.return_value = 'Hello Sds'
        #BytesIo = self.BytesIO
        self.backend(storage_client,'Pds', authors_images).get_image('Sds_file')
        
        storage_client.list_blobs.assert_called_with('Sds')
        blob.open.assert_called_with('rb')
        assert f.read() == 'Hello Sds'
        assert blob.upload_from_file == '/file/sds'      
        assert blob.name == 'Sds_file'
        assert blob.assert_called_once

