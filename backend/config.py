"""
Configuration Module for Clash Royale Deck Analyzer
Handles all environment variables and application settings
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    TESTING = False
    
    # MySQL Database configuration
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'root')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', ' cr')
    
    # SQLAlchemy Database URI - Use SQLite in development, MySQL in production
    ENVIRONMENT = os.getenv('FLASK_ENV', 'development')
    if ENVIRONMENT == 'development':
        SQLALCHEMY_DATABASE_URI = 'sqlite:///clash_royale_dev.db'
    else:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@"
            f"{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
            "?charset=utf8mb4"
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv('JWT_ACCESS_TOKEN_HOURS', 1)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv('JWT_REFRESH_TOKEN_DAYS', 30)))
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    
    # Clash Royale API Configuration
    CLASH_ROYALE_API_KEY = os.getenv('CLASH_ROYALE_API_KEY', '')
    CLASH_ROYALE_API_BASE_URL = 'https://api.clashroyale.com/v1'
    CLASH_ROYALE_API_TIMEOUT = 10  # seconds
    
    # Caching configuration (in seconds)
    PLAYER_CACHE_DURATION = int(os.getenv('PLAYER_CACHE_DURATION', 300))  # 5 minutes
    CARDS_CACHE_DURATION = int(os.getenv('CARDS_CACHE_DURATION', 86400))  # 24 hours
    
    # CORS Configuration
    # On production (unified service): CORS not needed since frontend is same origin
    # On development: allow localhost dev server ports and external frontend URLs
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173,http://localhost:5174,http://127.0.0.1:3000,http://127.0.0.1:5173,https://deploysus.vercel.app').split(',') if os.getenv('FLASK_ENV', 'development') == 'development' else os.getenv('CORS_ORIGINS', 'https://deploysus.vercel.app').split(',')
    
    # Pagination
    ITEMS_PER_PAGE = int(os.getenv('ITEMS_PER_PAGE', 20))
    
    # Rate limiting
    RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', 'memory://')
    RATELIMIT_DEFAULT = "100/hour"
    
    # Analysis thresholds
    ANALYSIS_THRESHOLDS = {
        'high_elixir': 4.5,
        'low_elixir': 3.0,
        'min_air_defense': 2,
        'min_splash': 2,
        'min_win_conditions': 1,
        'max_win_conditions': 3,
    }


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Enforce strong secret keys in production
    def __init__(self):
        super().__init__()
        if self.SECRET_KEY == 'dev-secret-key-change-in-production':
            raise ValueError("SECRET_KEY must be set in production environment")
        if self.JWT_SECRET_KEY == 'jwt-secret-key-change-in-production':
            raise ValueError("JWT_SECRET_KEY must be set in production environment")
        if not self.CLASH_ROYALE_API_KEY:
            raise ValueError("CLASH_ROYALE_API_KEY must be set in production environment")


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    """Get configuration object based on environment"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    return config.get(config_name, DevelopmentConfig)