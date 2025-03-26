import requests 
import sys 
import os 
from flask import Flask, request, render_template, flash
from tqdm import tqdm 
from app.logger import get_logger

logger = get_logger("client") 

SERVER_IP = "192.168.131.45"
PORT = 5001 
UPLOAD_URL = f"http://{SERVER_IP}:{PORT}" 

# Initialize Flask app
app = Flask(__name__, template_folder = "../templates") 
app.secret_key = "Raju@2003" 

@app.route("/")
def upload_form():
    """Render file upload form."""
    return render_template("index.html")

@app.route("/", methods=["POST"])
def uploade_file(file_path):
    """Handles file upload to the server."""
    try:
        file = request.files.get("file")
        if not file:
            flash("No file selected!", "error")
            return render_template("index.html")

        files = {"file": (file.filename, file.stream)}
        response = requests.post(UPLOAD_URL, files=files)

        if response.status_code == 200:
            flash(f"File '{file.filename}' uploaded successfully!", "success")
        else:
            flash(f"Failed to upload '{file.filename}'. Server response: {response.text}", "error")

    except requests.exceptions.RequestException as e:
        flash(f"Connection error: {e}", "error")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)