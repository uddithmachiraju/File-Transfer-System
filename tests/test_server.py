import os 
import sys 
import pytest 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.server import app 

@pytest.fixture
def client():
    app.config['TESTING'] = True 
    client = app.test_client() 
    yield client 

def test_upload_success(client):
    """Test if file uploads successfully"""
    data = {
        "file" : (open("tests/sample.json", "rb"),
        "sample.txt")
    }
    response = client.post("/", data = data, content_type = "multipart/form-data")
    assert response.status_code == 200 
    assert "uploaded successfully" in response.get_data(as_text = True) 

def test_no_file_upload(client):
    """Test if no file was uploaded"""
    response = client.post("/", data = {}, content_type = "multipart/form-data")
    assert response.status_code == 500 
    assert "Error uploading File" in response.get_data(as_text = True) 

def test_home_page(client):
    """Test the home page"""
    response = client.get("/")
    assert response.status_code == 200 