from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from config import Config

mongo = PyMongo()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    mongo.init_app(app)
    login_manager.init_app(app)

    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    return app
