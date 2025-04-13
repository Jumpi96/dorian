from flask import Flask, jsonify, redirect, request, session
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt
import datetime
from app.config import Config
from app.services.dynamodb import DynamoDBService

def create_app(testing=False):
    app = Flask(__name__)
    app.secret_key = Config.JWT_SECRET_KEY
    
    # Initialize DynamoDB service
    dynamodb = DynamoDBService(testing=testing)
    
    @app.route('/auth/login', methods=['GET'])
    def login():
        # In a real implementation, this would redirect to Google's OAuth consent screen
        # For testing, we'll simulate the OAuth flow
        return jsonify({
            "auth_url": "https://accounts.google.com/o/oauth2/v2/auth",
            "client_id": Config.GOOGLE_CLIENT_ID,
            "redirect_uri": Config.GOOGLE_REDIRECT_URI,
            "scope": "openid email profile"
        })

    @app.route('/auth/callback', methods=['GET'])
    def callback():
        # In a real implementation, this would handle the OAuth callback
        # For testing, we'll simulate receiving a token
        token = request.args.get('token')
        
        if not token:
            return jsonify({'error': 'Missing token'}), 401
            
        try:
            # Verify the token with Google
            idinfo = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                Config.GOOGLE_CLIENT_ID
            )
            
            # Extract user info
            user_id = idinfo['sub']
            email = idinfo['email']
            
            try:
                # Check if user exists in DynamoDB
                user = dynamodb.get_user(user_id)
                if not user:
                    # Create new user if doesn't exist
                    dynamodb.create_user(user_id, email)
                
                # Create JWT
                token = jwt.encode({
                    'sub': user_id,
                    'email': email,
                    'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
                }, Config.JWT_SECRET_KEY, algorithm='HS256')
                
                print(f"Created JWT token: {token}")
                print(f"JWT secret key: {Config.JWT_SECRET_KEY}")
                
                response_data = {
                    'token': token,
                    'user': {
                        'id': user_id,
                        'email': email
                    }
                }
                print(f"Response data: {response_data}")
                
                return jsonify(response_data)
            except Exception as e:
                print(f"Error with DynamoDB: {str(e)}")
                return jsonify({'error': 'Database error'}), 500
            
        except Exception as e:
            return jsonify({'error': str(e)}), 401

    return app 