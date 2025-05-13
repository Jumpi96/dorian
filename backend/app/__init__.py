from flask import Flask
from authlib.integrations.flask_client import OAuth
from app.config import Config
from app.clients.dynamodb import DynamoDBClient
from app.services.llm import LLMService
from app.services.rate_limit import RateLimitService
from app.services.wardrobe import WardrobeService
from app.services.recommendations import RecommendationsService
from app.services.interactions import InteractionsService
from app.services.trips import TripsService
from app.routes.auth import init_auth_routes
from app.routes.wardrobe import init_wardrobe_routes
from app.routes.recommendations import init_recommendation_routes
from app.routes.trips import init_trip_routes
from app.services.text_transformations import TextTransformationsService


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

def create_app(dynamoDBClient=DynamoDBClient(), google=None):
    app = Flask(__name__)
    app.secret_key = Config.JWT_SECRET_KEY
    if google is None:
        google = register_google_oauth(app)

    # Initialize services
    rate_limit_service = RateLimitService(dynamoDBClient)
    llm_service = LLMService(rate_limit_service)
    wardrobe_service = WardrobeService(dynamoDBClient)
    recommendations_service = RecommendationsService(llm_service, wardrobe_service)
    interactions_service = InteractionsService(dynamoDBClient)
    trips_service = TripsService(dynamoDBClient)
    text_transformations_service = TextTransformationsService(llm_service)

    # Initialize routes
    init_auth_routes(app, google)
    init_wardrobe_routes(app, wardrobe_service)
    init_recommendation_routes(app, recommendations_service, interactions_service, trips_service, text_transformations_service)
    init_trip_routes(app, trips_service)

    return app