import pytest
import jwt
from flask import redirect
from unittest.mock import patch, MagicMock
from app import create_app
from app.config import Config

@pytest.fixture
def client():
    # Create mock Google OAuth2 client
    mock_google = MagicMock()
    mock_google.authorize_redirect.return_value = redirect("https://accounts.google.com/o/oauth2/v2/auth")
    mock_google.authorize_access_token.return_value = {'access_token': 'mock-token'}
    mock_google.get.return_value.json.return_value = {
        'id': 'mock-user-id',
        'email': 'mock@example.com',
        'name': 'Mock User'
    }

    # Mock DynamoDB
    mock_dynamodb = MagicMock()

    app = create_app(mock_dynamodb, google=mock_google)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['JSONIFY_MIMETYPE'] = 'application/json'
    Config.FRONTEND_REDIRECT_SUCCESS = 'http://localhost:3000/auth/success'
    Config.JWT_SECRET_KEY = 'mock-jwt-secret'

    with app.test_client() as test_client:
        yield test_client, mock_google

def test_login_endpoint(client):
    test_client, mock_google = client
    response = test_client.get('/auth/login')
    assert response.status_code == 302
    assert 'accounts.google.com/o/oauth2/v2/auth' in response.location

def test_callback_endpoint_success(client):
    test_client, mock_google = client
    response = test_client.get('/auth/callback', follow_redirects=False)

    # Validate redirect URL and cookie presence
    assert response.status_code == 302
    assert response.location.startswith(Config.FRONTEND_REDIRECT_SUCCESS)
    assert 'auth_token' in response.headers.get('Set-Cookie', '')

