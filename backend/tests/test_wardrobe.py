import pytest
from flask import Flask, request
from unittest.mock import MagicMock
from app.routes.wardrobe import init_wardrobe_routes

# Fake JWT payload to simulate authenticated user
MOCK_USER = {"sub": "user-123"}

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config["TESTING"] = True

    # Override requires_auth decorator
    def fake_requires_auth(f):
        def wrapped(*args, **kwargs):
            request.user = MOCK_USER
            return f(*args, **kwargs)
        wrapped.__name__ = f.__name__
        return wrapped

    # Monkey patch it into wardrobe module before init
    from app.routes import wardrobe
    wardrobe.requires_auth = fake_requires_auth

    # Provide a mocked DynamoDB client
    mock_dynamodb = MagicMock()
    init_wardrobe_routes(app, mock_dynamodb)

    with app.test_client() as test_client:
        yield test_client, mock_dynamodb

def test_add_wardrobe_item_success(client):
    test_client, mock_dynamodb = client
    description = "Parka beige"
    mock_dynamodb.add_wardrobe_item.return_value = None

    response = test_client.post("/wardrobe", json={"description": description})
    data = response.get_json()

    assert response.status_code == 201
    assert "itemId" in data
    assert data["description"] == description
    mock_dynamodb.add_wardrobe_item.assert_called_once()
    kwargs = mock_dynamodb.add_wardrobe_item.call_args.kwargs
    assert kwargs["user_id"] == MOCK_USER["sub"]
    assert kwargs["description"] == description

def test_add_wardrobe_item_missing_description(client):
    test_client, _ = client
    response = test_client.post("/wardrobe", json={})

    assert response.status_code == 400
    assert response.get_json() == {"error": "Missing description"}

def test_get_wardrobe_items_success(client):
    test_client, mock_dynamodb = client
    expected_items = [{"itemId": "abc", "description": "White hoodie"}]
    mock_dynamodb.get_wardrobe_items.return_value = expected_items

    response = test_client.get("/wardrobe")
    data = response.get_json()

    assert response.status_code == 200
    assert data["items"] == expected_items
    mock_dynamodb.get_wardrobe_items.assert_called_once_with(MOCK_USER["sub"])

def test_get_wardrobe_items_failure(client):
    test_client, mock_dynamodb = client
    mock_dynamodb.get_wardrobe_items.side_effect = Exception("DB error")

    response = test_client.get("/wardrobe")
    assert response.status_code == 500
    assert response.get_json() == {"error": "An error occurred while retrieving items"}

def test_delete_wardrobe_item_success(client):
    test_client, mock_dynamodb = client
    item_id = "test-item-123"
    mock_dynamodb.delete_wardrobe_item.return_value = True

    response = test_client.delete(f"/wardrobe/{item_id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data == {"message": "Item deleted successfully"}
    mock_dynamodb.delete_wardrobe_item.assert_called_once_with(MOCK_USER["sub"], item_id)

def test_delete_wardrobe_item_failure(client):
    test_client, mock_dynamodb = client
    item_id = "test-item-123"
    mock_dynamodb.delete_wardrobe_item.return_value = False

    response = test_client.delete(f"/wardrobe/{item_id}")
    data = response.get_json()

    assert response.status_code == 500
    assert data == {"error": "Failed to delete item"}
    mock_dynamodb.delete_wardrobe_item.assert_called_once_with(MOCK_USER["sub"], item_id)
