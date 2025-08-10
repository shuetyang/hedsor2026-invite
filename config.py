import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    """Configuration class for the Flask application"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-this-in-production')
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///wedding.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email Configuration
    RESEND_API_KEY = os.environ.get('RESEND_API_KEY')
    FROM_EMAIL = os.environ.get('FROM_EMAIL', 'onboarding@resend.dev')
    
    # Optional: Custom domain
    CUSTOM_DOMAIN = os.environ.get('CUSTOM_DOMAIN')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
