import pytest
from unittest.mock import patch, MagicMock
from app import create_app
from app.services.dynamodb import DynamoDBService
import jwt
from datetime import datetime, timedelta
from google.oauth2 import id_token
from google.auth.transport import requests
from app.config import Config

# Create a mock DynamoDB service class
class MockDynamoDBService:
    def __init__(self):
        self.get_user_called = False
        self.create_user_called = False
        
    def get_user(self, user_id):
        self.get_user_called = True
        self.last_user_id = user_id
        return None
        
    def create_user(self, user_id, email):
        self.create_user_called = True
        self.last_user_id = user_id
        self.last_email = email
        return True



@pytest.fixture
def client():
    # Patch the DynamoDB service
    mock_dynamodb = MockDynamoDBService()
    app = create_app(mock_dynamodb)
    app.config['TESTING'] = True
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_MIMETYPE'] = 'application/json'
    
    # Set mock values for testing
    Config.GOOGLE_CLIENT_ID = 'mock-client-id'
    Config.JWT_SECRET_KEY = 'mock-jwt-secret'
    with app.test_client() as client:
        client.mock_dynamodb = mock_dynamodb  # Attach the mock to the client
        yield client

def test_login_endpoint(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    data = response.get_json()
    assert 'auth_url' in data
    assert 'client_id' in data
    assert 'redirect_uri' in data
    assert 'scope' in data

@patch('google.oauth2.id_token.verify_oauth2_token')
def test_callback_endpoint_failure(mock_verify, client):
    # Mock Google token verification to raise an exception
    mock_verify.side_effect = Exception('Invalid token')
    
    response = client.get('/auth/callback?token=invalid_token')
    assert response.status_code == 401
    assert 'error' in response.get_json()

def test_callback_endpoint_missing_token(client):
    response = client.get('/auth/callback')
    assert response.status_code == 401
    assert 'error' in response.get_json()

@patch('google.oauth2.id_token.verify_oauth2_token')
def test_callback_endpoint_success(mock_verify, client):
    # Mock Google token verification to return a valid user ID and email
    mock_verify.return_value = {
        'sub': 'mock-user-id',
        'email': 'mock@example.com'
    }
    
    response = client.get('/auth/callback?token=valid_token')
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data
    assert 'user' in data
    assert data['user']['id'] == 'mock-user-id'
    assert data['user']['email'] == 'mock@example.com'

    assert client.mock_dynamodb.get_user_called
    assert client.mock_dynamodb.create_user_called
