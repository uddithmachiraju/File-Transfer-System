import requests 
import sys 
import os 
from tqdm import tqdm 
from app.logger import get_logger

logger = get_logger("client") 

SERVER_IP = ""
PORT = 5001 
UPLOAD_URL = f"http://{SERVER_IP}:{PORT}" 

def uploade_file(file_path):
    """Uploads a file to the flask server"""
    if not os.path.exists(file_path):
        logger.error(f"File not found on path {file_path}") 
        return
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)

    with open(file_path, "rb") as file:
        with tqdm(total = file_size, unit = "B", unit_scale = True, desc = f"Uploading {file_name}") as progress:
            response = requests.post(
                UPLOAD_URL, 
                file = {
                    "file": file
                },
                stream = True
            )
            progress.update(file_size) 

    if response.status_code == 200:
        logger.info(f"File {file_name} Uploaded Successfully!")
    else:
        logger.error(f"Failed uploading {file_name}. Server Response {response.text}") 

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python client.py <file_path>")
    else:
        uploade_file(sys.argv[1]) 
