"""Flask-Blog app configuration"""
import os
import secrets

from dotenv import load_dotenv

# Specify a .env-file.
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """Set Flask configuration variables."""
    # General config
    ENVIRONMENT = os.environ.get("ENVIRONMENT")
    FLASK_APP = os.environ.get("FLASK_APP")
    FLASK_DEBUG = True

    SECRET_KEY = secrets.token_hex()    # Generate secret key

    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


