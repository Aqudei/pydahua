from flask import Flask
from flask_cors import CORS
from flask_cors import cross_origin
from .dahua_ipc import DahuaIPC
from dotenv import load_dotenv
import os

load_dotenv()  # Optional; explicit loading if running via `python app.py`


CAMERA_IP = os.getenv("CAMERA_IP")
CAMERA_USER = os.getenv("CAMERA_USER")
CAMERA_PASS = os.getenv("CAMERA_PASS")

cam = DahuaIPC(CAMERA_IP, CAMERA_USER, CAMERA_PASS)

app = Flask(__name__)
app.debug = True
CORS(app)


@app.route("/autofocus/", methods=["post"])
@cross_origin()
def autofocus():
    cam.AutoFocus()
    
    