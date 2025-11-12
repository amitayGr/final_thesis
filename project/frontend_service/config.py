import os
import logging
from datetime import timedelta


class Config:
    """Frontend Service Configuration"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('FRONTEND_SECRET_KEY', 'frontend-default-secret-key-change-in-production')
    HOST = os.environ.get('FRONTEND_HOST', '0.0.0.0')
    PORT = int(os.environ.get('FRONTEND_PORT', 5000))
    DEBUG = os.environ.get('FRONTEND_DEBUG', 'False').lower() == 'true'
    JSON_AS_ASCII = False
    
    # Session Configuration
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=5)
    SESSION_FILE_THRESHOLD = 500
    
    # Backend Service Configuration
    BACKEND_SERVICE_URL = os.environ.get('BACKEND_SERVICE_URL', 'http://localhost:5001')
    BACKEND_TIMEOUT = int(os.environ.get('BACKEND_TIMEOUT', 30))
    
    # Logging Configuration
    LOG_FILE = os.environ.get('FRONTEND_LOG_FILE', '../logs/frontend_service.log')
    LOG_LEVEL = os.environ.get('FRONTEND_LOG_LEVEL', 'INFO')


def setup_logging():
    """Configure logging for the frontend service"""
    log_dir = os.path.dirname(Config.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format='[%(asctime)s] [FRONTEND] [%(levelname)s] - %(message)s',
        handlers=[
            logging.FileHandler(Config.LOG_FILE),
            logging.StreamHandler()  # Also print to console
        ]
    )
    
    return logging.getLogger('frontend_service')
