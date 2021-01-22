from flask import Flask
from .config import Config
from .extensions import jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    return app

def register_extensions(app):
    jwt.init_app(app)