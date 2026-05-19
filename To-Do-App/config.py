import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Secret key — long and random in production
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-fallback-key-change-this'

    # Database — uses environment variable in production, local file in dev
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or 'sqlite:///focusflow.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Production settings
    DEBUG = os.environ.get('FLASK_DEBUG', 'False') == 'True'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# Flask will use this based on the FLASK_ENV environment variable
config = {
    'development': DevelopmentConfig,
    'production':  ProductionConfig,
    'default':     DevelopmentConfig
}