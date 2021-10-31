from os import environ
#from dotenv import load_dotenv
from pathlib import Path

basedir = Path(__file__).parent.absolute()
#load_dotenv(Path(__file__).parent / 'project/.env')


class Config:
    """Base config."""
    SECRET_KEY = environ.get('SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Database
    DATABASE = "flaskr.db"

    # Credentials
    USERNAME = "admin"
    PASSWORD = "admin"


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    db = "flaskr.db"
    DATABASE = basedir.joinpath(db)


class DevConfig(Config):
    FLASK_ENV = 'development'
    db = "test.db"
    DATABASE = basedir.joinpath(db)
    DEBUG = True
    TESTING = True
