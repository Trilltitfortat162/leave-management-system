import os
from datetime import timedelta

class Config:
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    # For development: Use SQLite (no MySQL installation needed)
    # For production: Switch to MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///leave_management.db'
    
    # MySQL configuration (commented out for now - use when deploying)
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/leave_management'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Default leave balance for new employees
    DEFAULT_LEAVE_BALANCE = 20