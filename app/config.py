"""
Configuration settings for My Inner Scope application
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class with common settings"""
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///users.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Application settings
    WTF_CSRF_ENABLED = True  # If you use Flask-WTF forms
    
    # Session management
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours in seconds

    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    @staticmethod
    def validate():
        """Validate that required environment variables are set"""
        if not Config.SECRET_KEY:
            raise ValueError(
                "No SECRET_KEY environment variable set. "
                "Please create a .env file with SECRET_KEY=your-secret-key"
            )

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    # You might want a separate dev database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL', 'sqlite:///users.db')

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    # In production, you might use PostgreSQL or MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///prod_users.db')

class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    DEBUG = True
    # Use in-memory database for tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # Disable CSRF for easier testing
    WTF_CSRF_ENABLED = False

# Dictionary to easily switch between configurations
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
