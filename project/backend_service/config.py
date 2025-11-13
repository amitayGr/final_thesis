import os
import logging

class Config:
    """Backend Service Configuration"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('BACKEND_SECRET_KEY', 'backend-default-secret-key-change-in-production')
    HOST = os.environ.get('BACKEND_HOST', '0.0.0.0')
    PORT = int(os.environ.get('BACKEND_PORT', 5001))
    DEBUG = os.environ.get('BACKEND_DEBUG', 'False').lower() == 'true'
    
    # Database Configuration - SQL Server
    DB_CONFIG = {
        'driver': os.environ.get('DB_DRIVER', 'SQL Server'),
        'server': os.environ.get('DB_SERVER', 'DESKTOP-824DEOL\\SQLEXPRESS01'),
        'database': os.environ.get('DB_DATABASE', 'AKINTOR'),
        'trusted_connection': os.environ.get('DB_TRUSTED_CONNECTION', 'yes')
    }
    
    # Logging Configuration
    LOG_FILE = os.environ.get('BACKEND_LOG_FILE', '../logs/backend_service.log')
    LOG_LEVEL = os.environ.get('BACKEND_LOG_LEVEL', 'INFO')
    
    # Algorithm Configuration
    ENTROPY_ALPHA = 0.25
    SCALE_FACTOR = 1.5
    THEOREM_THRESHOLD = 0.01


def setup_logging():
    """Configure logging for the backend service"""
    log_dir = os.path.dirname(Config.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format='[%(asctime)s] [BACKEND] [%(levelname)s] - %(message)s',
        handlers=[
            logging.FileHandler(Config.LOG_FILE),
            logging.StreamHandler()  # Also print to console
        ]
    )
    
    return logging.getLogger('backend_service')
