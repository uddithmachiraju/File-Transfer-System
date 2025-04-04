import requests
import argparse
from flask import Flask, request, render_template, flash
from app.logger import get_logger

logger = get_logger("client")

# Argument Parser for IP and Port
parser = argparse.ArgumentParser(description="Flask File Upload Client")
parser.add_argument("--server_ip", required=True, help="Server IP address (Required)")
parser.add_argument("--server_port", type=int, default=5001, help="Server Port (default: 5001)")

args = parser.parse_args()
SERVER_IP = args.server_ip
PORT = args.server_port 
UPLOAD_URL = f"http://{SERVER_IP}:{PORT}"

# Initialize Flask App
app = Flask(__name__, template_folder="../templates")
app.secret_key = "Raju@2003"

@app.route("/")
def upload_form():
    """Render file upload form."""
    return render_template("index.html")

@app.route("/", methods=["POST"])
def upload_file():
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
    logger.info(f"Client sending requests to {UPLOAD_URL}")
    app.run(host="0.0.0.0", port=5002, debug=True)
