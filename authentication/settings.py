import os
from dotenv import load_dotenv

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', '')
JWT_SECRET_TOKEN = os.getenv('JWT_SECRET_TOKEN', '')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY', '')
TOKEN_EXPIRATION_TIME = 7200
REFRESH_TOKEN_EXPIRATION_TIME = 7200

APP_HOST = os.getenv('APP_HOST', 'http://localhost:3000')
