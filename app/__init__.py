from flask import Flask
from flask_cors import CORS
from config import config_map

from .dahua_ipc.dahua import DahuaCameraAPI

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_map[config_name])
    CORS(app)

    # Initialize Dahua camera with config values
    app.cam = DahuaCameraAPI(
        app.config["CAMERA_IP"],
        app.config["CAMERA_USER"],
        app.config["CAMERA_PASS"],
    )

    # Register routes
    from .routes import register_routes
    register_routes(app)

    return app
