import os
import argparse
from flask import Flask, request, render_template
from app.logger import get_logger

# Logger setup
logger = get_logger("server")

# Argument Parser for IP and Port
parser = argparse.ArgumentParser(description="Flask File Upload Server")
parser.add_argument("--host", default="0.0.0.0", help="Host IP address (default: 0.0.0.0)")
parser.add_argument("--port", type=int, help="Port number (default: from config.json)")

args = parser.parse_args()
HOST = args.host
PORT = args.port

# Initialize Flask App
app = Flask(__name__, template_folder="../templates")

# Ensure uploads directory exists
os.makedirs("uploads", exist_ok=True)

@app.route("/")
def upload_form():
    return render_template("intro.html")

@app.route("/", methods=["POST"])
def upload_file():
    try:
        file = request.files['file']
        if not file:
            logger.warning("No file uploaded!")
            return "No file Uploaded!", 400
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)
        logger.info(f"File {file.filename} uploaded successfully from {request.remote_addr}")
        return f"File {file.filename} uploaded successfully", 200
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        return "Error uploading File", 500  

if __name__ == "__main__":
    logger.info(f"Starting the server on {HOST}:{PORT}")
    app.run(host=HOST, port=PORT, debug=True)
