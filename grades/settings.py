import os
from dotenv import load_dotenv

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', '')
