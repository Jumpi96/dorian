from flask import Flask
from app.config import Config
from app.services.dynamodb import DynamoDBService
from app.routes.auth import init_auth_routes
from app.routes.wardrobe import init_wardrobe_routes

def create_app(dynamoDBService=DynamoDBService()):
    app = Flask(__name__)
    app.secret_key = Config.JWT_SECRET_KEY
    
    # Initialize routes
    init_auth_routes(app, dynamoDBService)
    init_wardrobe_routes(app, dynamoDBService)
    
    return app 