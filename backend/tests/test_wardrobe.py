import pytest
from unittest.mock import patch, MagicMock
from app import create_app
import jwt
from datetime import datetime, timedelta
from app.config import Config

# Create a mock DynamoDB service class
class MockDynamoDBService:
    def __init__(self):
        self.wardrobe_items = {}
        self.add_wardrobe_item_called = False
        self.get_wardrobe_items_called = False
        
    def add_wardrobe_item(self, user_id, item_id, description):
        self.add_wardrobe_item_called = True
        if user_id not in self.wardrobe_items:
            self.wardrobe_items[user_id] = []
        self.wardrobe_items[user_id].append({
            'itemId': item_id,
            'description': description
        })
        return True
        
    def get_wardrobe_items(self, user_id):
        self.get_wardrobe_items_called = True
        return self.wardrobe_items.get(user_id, [])

@pytest.fixture
def client():
    # Patch the DynamoDB service
    mock_dynamodb = MockDynamoDBService()
    app = create_app(mock_dynamodb)
    app.config['TESTING'] = True
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_MIMETYPE'] = 'application/json'
    
    # Set mock values for testing
    Config.JWT_SECRET_KEY = 'mock-jwt-secret'
    with app.test_client() as client:
        client.mock_dynamodb = mock_dynamodb  # Attach the mock to the client
        yield client
        
@pytest.fixture
def valid_token():
    # Create a valid JWT token for testing
    payload = {
        'sub': 'test-user-id',
        'email': 'test@example.com',
        'exp': datetime.now() + timedelta(days=1)
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

def test_add_wardrobe_item_unauthorized(client):
    response = client.post('/wardrobe/add', json={'description': 'Test item'})
    assert response.status_code == 401
    assert 'error' in response.get_json()

def test_add_wardrobe_item_missing_description(client, valid_token):
    headers = {'Authorization': f'Bearer {valid_token}'}
    response = client.post('/wardrobe/add', json={}, headers=headers)
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_add_wardrobe_item_success(client, valid_token):
    headers = {'Authorization': f'Bearer {valid_token}'}
    response = client.post('/wardrobe/add', 
                         json={'description': 'Test item'}, 
                         headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert 'itemId' in data
    assert 'description' in data
    assert data['description'] == 'Test item'
    assert client.mock_dynamodb.add_wardrobe_item_called

def test_get_wardrobe_items_unauthorized(client):
    response = client.get('/wardrobe')
    assert response.status_code == 401
    assert 'error' in response.get_json()

def test_get_wardrobe_items_empty(client, valid_token):
    headers = {'Authorization': f'Bearer {valid_token}'}
    response = client.get('/wardrobe', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'items' in data
    assert len(data['items']) == 0
    assert client.mock_dynamodb.get_wardrobe_items_called

def test_get_wardrobe_items_with_items(client, valid_token):
    # First add an item
    headers = {'Authorization': f'Bearer {valid_token}'}
    client.post('/wardrobe/add', 
               json={'description': 'Test item'}, 
               headers=headers)
    
    # Then get the items
    response = client.get('/wardrobe', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'items' in data
    assert len(data['items']) == 1
    assert data['items'][0]['description'] == 'Test item'

def test_multi_user_wardrobe_items(client):
    # Create tokens for two different users
    user1_token = jwt.encode(
        {'sub': 'user1', 'email': 'user1@example.com', 'exp': datetime.now() + timedelta(days=1)},
        Config.JWT_SECRET_KEY,
        algorithm='HS256'
    )
    user2_token = jwt.encode(
        {'sub': 'user2', 'email': 'user2@example.com', 'exp': datetime.now() + timedelta(days=1)},
        Config.JWT_SECRET_KEY,
        algorithm='HS256'
    )
    
    # Add items for both users
    client.post('/wardrobe/add', 
               json={'description': 'User1 item'}, 
               headers={'Authorization': f'Bearer {user1_token}'})
    client.post('/wardrobe/add', 
               json={'description': 'User2 item'}, 
               headers={'Authorization': f'Bearer {user2_token}'})
    
    # Check that each user only sees their own items
    response1 = client.get('/wardrobe', 
                         headers={'Authorization': f'Bearer {user1_token}'})
    data1 = response1.get_json()
    assert len(data1['items']) == 1
    assert data1['items'][0]['description'] == 'User1 item'
    
    response2 = client.get('/wardrobe', 
                         headers={'Authorization': f'Bearer {user2_token}'})
    data2 = response2.get_json()
    assert len(data2['items']) == 1
    assert data2['items'][0]['description'] == 'User2 item' 