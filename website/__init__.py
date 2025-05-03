from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from dotenv import load_dotenv
import os

load_dotenv()


def create_app():
    app = Flask(__name__)


    # Import routes
    from .views import views
    
    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Required for flash messages
        
    return app


