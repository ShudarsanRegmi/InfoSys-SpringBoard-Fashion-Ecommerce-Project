import os

class Config:
    """Base configuration with default settings."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'Infosys-Springboard-5.0')  # Keep it secret, set via environment variables
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking for performance
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///database.db')  # Use environment variable for DB URI

class TestConfig(Config):
    """Configuration for testing environment."""
    TESTING = True  # Enable testing mode
    SECRET_KEY = 'test_secret_key'  # Set a secret key for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use an in-memory database for tests
    SESSION_COOKIE_NAME = 'test_session'
    WTF_CSRF_ENABLED = False

class DevelopmentConfig(Config):
    """Configuration for development environment."""
    DEBUG = True  # Enable debug mode for development
