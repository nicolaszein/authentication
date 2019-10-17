import os
from dotenv import load_dotenv

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', '')
JWT_SECRET_TOKEN = os.getenv('JWT_SECRET_TOKEN', '')
TOKEN_EXPIRATION_TIME = 7200
