import os
import secrets
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Use key from .env; fall back to a random key (safe, but sessions reset on restart).
    # For production always set SECRET_KEY in .env.
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)

    # Secure session cookies
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE   = os.environ.get('HTTPS', 'false').lower() == 'true'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=12)
    
    # PostgreSQL connection
    DB_HOST     = os.environ.get('DB_HOST', 'localhost')
    DB_PORT     = os.environ.get('DB_PORT', '5432')
    DB_NAME     = os.environ.get('DB_NAME', 'warehouse_db')
    DB_USER     = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload folder for images
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # External API URL for today's truck stats
    # Expected JSON: {"loaded": 182, "unloaded": 165, "issues": 3}
    TRUCK_API_URL = os.environ.get('TRUCK_API_URL', '')
