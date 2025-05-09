import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Google OAuth
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

    # Frontend
    FRONTEND_REDIRECT_SUCCESS = 'http://localhost:3000/login-success'
    
    # AWS
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1') 