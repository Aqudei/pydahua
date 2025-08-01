import os
from dotenv import load_dotenv

# Load .env early
load_dotenv()

class Config:
    DEBUG = False
    TESTING = False
    CAMERA_IP = os.getenv("CAMERA_IP")
    CAMERA_USER = os.getenv("CAMERA_USER")
    CAMERA_PASS = os.getenv("CAMERA_PASS")

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
