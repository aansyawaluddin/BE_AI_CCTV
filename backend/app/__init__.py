from flask import Flask
from .model.config import Session, Base, engine 
from .model.location import location_bp
from .model.camera import camera_bp
from .model.recording import recording_bp
from .model.cameraConfig import camera_config_bp
from flask_migrate import Migrate
from flask_cors import CORS

from .model.models import Location, Camera, Recording

def create_app(app=None):
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(location_bp, url_prefix='/api')
    app.register_blueprint(camera_bp, url_prefix='/api')
    app.register_blueprint(recording_bp, url_prefix='/api')
    app.register_blueprint(camera_config_bp, url_prefix='/api')


    Base.metadata.create_all(engine)

    migrate = Migrate(app, Base)

    return app
