from flask import Flask
from .extensions import jwt

def create_app():
    app = Flask(__name__)
    register_extensions(app)
    return app

def register_extensions(app):
    jwt.init_app(app)