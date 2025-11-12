# app.py - Frontend Service
from flask import Flask
from flask_session import Session
from extensions import bcrypt
from config import Config, setup_logging
from backend_client import get_backend_client

# Setup logging first
logger = setup_logging()
logger.info("Frontend service starting...")

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
bcrypt.init_app(app)
Session(app)

# Initialize backend client
backend_client = get_backend_client(Config.BACKEND_SERVICE_URL)
logger.info(f"Backend client initialized with URL: {Config.BACKEND_SERVICE_URL}")

# Make backend_client available to blueprints
app.backend_client = backend_client

# Register blueprints
from pages.Home_Page.Home_Page import home_page
app.register_blueprint(home_page, url_prefix='/')

from pages.Registration_Page.Registration_Page import registration_page
app.register_blueprint(registration_page, url_prefix='/register')

from pages.Login_Page.Login_Page import login_page
app.register_blueprint(login_page, url_prefix='/login')

from pages.User_Profile_Page.User_Profile_Page import user_profile_page
app.register_blueprint(user_profile_page, url_prefix='/profile')

from pages.Question_Page.Question_Page import question_page
app.register_blueprint(question_page, url_prefix='/question')

from pages.Feedback_Page.Feedback_Page import feedback_page
app.register_blueprint(feedback_page, url_prefix='/feedback')

from pages.Contact_Page.Contact_Page import contact_page
app.register_blueprint(contact_page, url_prefix='/contact')

logger.info("All blueprints registered successfully")


@app.before_request
def log_request():
    """Log all incoming requests"""
    from flask import request
    logger.info(f"[FRONTEND] Request: {request.method} {request.path}")


@app.after_request
def log_response(response):
    """Log all outgoing responses"""
    from flask import request
    logger.info(f"[FRONTEND] Response: {request.method} {request.path} - Status: {response.status_code}")
    return response


if __name__ == '__main__':
    logger.info(f"Starting frontend service on {Config.HOST}:{Config.PORT}")
    logger.info(f"Debug mode: {Config.DEBUG}")
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
