from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configure session
    app.config['SECRET_KEY'] = os.getenv('MAIN_APP_SECRET_KEY', 'default_secret_key')
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours in seconds
    
    from .views import views
    app.register_blueprint(views, url_prefix='/')
    
    return app