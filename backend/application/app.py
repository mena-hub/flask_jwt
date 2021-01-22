from flask import Flask
from flask_restful import Api
from .config import Config
from .extensions import jwt
from resources.token import AccountSettings

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    register_resources(app)
    return app

def register_extensions(app):
    jwt.init_app(app)

def register_resources(app):
    api = Api(app)
    api.add_resource(AccountSettings, "/account/change_settings")