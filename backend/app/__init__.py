from flask import Flask
from authlib.integrations.flask_client import OAuth
from app.config import Config
from app.services.dynamodb import DynamoDBService
from app.routes.auth import init_auth_routes
from app.routes.wardrobe import init_wardrobe_routes

oauth = OAuth()

def register_google_oauth(app):
    oauth.init_app(app)
    return oauth.register(
        name='google',
        client_id=Config.GOOGLE_CLIENT_ID,
        client_secret=Config.GOOGLE_CLIENT_SECRET,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        api_base_url='https://www.googleapis.com/oauth2/v2/',
        client_kwargs={'scope': 'openid email profile'}
    )

def create_app(dynamoDBService=DynamoDBService(), google=None):
    app = Flask(__name__)
    app.secret_key = Config.JWT_SECRET_KEY
    if google is None:
        google = register_google_oauth(app)

    # Initialize routes
    init_auth_routes(app, google)
    init_wardrobe_routes(app, dynamoDBService)
    
    return app