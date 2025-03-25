import os 
import json 
from app.logger import get_logger
from flask import Flask, request, render_template

with open("app/congig.json", "rb") as file:
    params = json.load(file) 

# Add logger file to add logs 
logger = get_logger("server")

# Use Flask for API
app = Flask(__name__) 

# Add a uploads folder to store all the uploaded files
os.makedirs("uploads/", exist_ok = True)

@app.route("/")
def upload_form():
    return render_template("templates/index.html") 

@app.route("/", methods = ["POST"])
def upload_file():
    try:
        file = request.files['file']
        if not file:
            logger.warning("No file was uploaded!")
            return "No file Uploaded!", 400 
        file_path = os.path.join("uploads", file.filename) 
        file.save(file_path) 
        logger.info(f"File {file.filename} uploaded successfully from {request.remote_addr}")
        return f"File {file.filename} uploaded successfully", 200 
    
    except Exception as e:
        logger.error(f"Error uploading file {e}")
        return "Error uploading File", 500  
    
if __name__ == "__main__":
    logger.info(f"Starting the server on port {params['PORT']}")
    app.run(host = "0.0.0.0", port = params['PORT'], debug = True) 