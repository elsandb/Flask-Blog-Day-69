"""Flask-Blog app configuration"""
import os

from dotenv import load_dotenv

# Specify a .env-file.
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """Set Flask configuration variables."""
    # General config
    ENVIRONMENT = os.environ.get('ENVIRONMENT')
    FLASK_DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


