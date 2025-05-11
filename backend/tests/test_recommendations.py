import pytest
from flask import Flask, request
from unittest.mock import Mock
from app.services.recommendations import InsufficientWardrobeError

# Fake JWT payload to simulate authenticated user
MOCK_USER = {"sub": "test_user"}

@pytest.fixture
def mock_recommendations_service():
    return Mock()

@pytest.fixture
def mock_interactions_service():
    return Mock()

@pytest.fixture
def client(mock_recommendations_service, mock_interactions_service):
    app = Flask(__name__)
    app.config["TESTING"] = True

    # Override requires_auth decorator
    def fake_requires_auth(f):
        def wrapped(*args, **kwargs):
            request.user = MOCK_USER
            return f(*args, **kwargs)
        wrapped.__name__ = f.__name__
        return wrapped

    # Monkey patch it into recommendations module before init
    from app.routes import recommendations
    recommendations.requires_auth = fake_requires_auth

    # Initialize routes with mocked services
    from app.routes.recommendations import init_recommendation_routes
    init_recommendation_routes(app, mock_recommendations_service, mock_interactions_service)

    with app.test_client() as test_client:
        yield test_client, mock_recommendations_service, mock_interactions_service

def test_recommend_outfit_success(client):
    test_client, mock_recommendations_service, mock_interactions_service = client
    situation = "casual dinner"
    recommendation = {
        "top": "Black t-shirt",
        "bottom": "Blue jeans",
        "shoes": "White sneakers"
    }
    interaction_id = "rec_2024-03-21T12:00:00"
    
    mock_recommendations_service.get_outfit_recommendation.return_value = recommendation
    mock_interactions_service.save_recommendation_interaction.return_value = interaction_id
    
    response = test_client.post('/recommend/wear', json={"situation": situation})
    
    assert response.status_code == 200
    assert response.json == {
        "outfit": recommendation,
        "interaction_id": interaction_id
    }
    
    mock_recommendations_service.get_outfit_recommendation.assert_called_once_with(
        MOCK_USER["sub"], situation
    )
    mock_interactions_service.save_recommendation_interaction.assert_called_once_with(
        user_id=MOCK_USER["sub"], situation=situation, recommendation=recommendation
    )

def test_recommend_outfit_missing_situation(client):
    test_client, _, _ = client
    response = test_client.post('/recommend/wear', json={})
    
    assert response.status_code == 400
    assert response.json == {"error": "Missing situation in request"}

def test_recommend_outfit_insufficient_items(client):
    test_client, mock_recommendations_service, _ = client
    situation = "casual dinner"
    
    mock_recommendations_service.get_outfit_recommendation.side_effect = InsufficientWardrobeError(
        "Need at least 3 items in wardrobe for recommendations. Current items: 2"
    )
    
    response = test_client.post('/recommend/wear', json={"situation": situation})
    
    assert response.status_code == 400
    assert response.json == {
        "error": "Need at least 3 items in wardrobe for recommendations. Current items: 2",
        "type": "insufficient_wardrobe",
        "message": "Please add more items to your wardrobe before requesting recommendations."
    }

def test_recommend_outfit_general_error(client):
    test_client, mock_recommendations_service, _ = client
    situation = "casual dinner"
    
    mock_recommendations_service.get_outfit_recommendation.side_effect = Exception("Test error")
    
    response = test_client.post('/recommend/wear', json={"situation": situation})
    
    assert response.status_code == 500
    assert response.json == {"error": "Test error"}

def test_recommend_items_to_buy_success(client):
    test_client, mock_recommendations_service, mock_interactions_service = client
    situation = "casual dinner"
    recommendation = {
        "item": "Black leather loafers",
        "explanation": "These versatile loafers would be perfect for your casual dinner. They can be dressed up or down, and would complement your existing wardrobe by providing a sophisticated footwear option that works well with both jeans and dress pants. The black color makes them easy to pair with any outfit."
    }
    interaction_id = "buy_2024-03-21T12:00:00"
    
    mock_recommendations_service.get_items_to_buy_recommendation.return_value = recommendation
    mock_interactions_service.save_purchase_recommendation_interaction.return_value = interaction_id
    
    response = test_client.post('/recommend/buy', json={"situation": situation})
    
    assert response.status_code == 200
    assert response.json == {
        "item_to_buy": recommendation,
        "interaction_id": interaction_id
    }
    
    mock_recommendations_service.get_items_to_buy_recommendation.assert_called_once_with(
        MOCK_USER["sub"], situation
    )
    mock_interactions_service.save_purchase_recommendation_interaction.assert_called_once_with(
        user_id=MOCK_USER["sub"], situation=situation, recommendation=recommendation
    )

def test_recommend_items_to_buy_missing_situation(client):
    test_client, _, _ = client
    response = test_client.post('/recommend/buy', json={})
    
    assert response.status_code == 400
    assert response.json == {"error": "Missing situation in request"}

def test_recommend_items_to_buy_insufficient_items(client):
    test_client, mock_recommendations_service, _ = client
    situation = "casual dinner"
    
    mock_recommendations_service.get_items_to_buy_recommendation.side_effect = InsufficientWardrobeError(
        "Need at least 3 items in wardrobe for recommendations. Current items: 2"
    )
    
    response = test_client.post('/recommend/buy', json={"situation": situation})
    
    assert response.status_code == 400
    assert response.json == {
        "error": "Need at least 3 items in wardrobe for recommendations. Current items: 2",
        "type": "insufficient_wardrobe",
        "message": "Please add more items to your wardrobe before requesting recommendations."
    }

def test_recommend_items_to_buy_general_error(client):
    test_client, mock_recommendations_service, _ = client
    situation = "casual dinner"
    
    mock_recommendations_service.get_items_to_buy_recommendation.side_effect = Exception("Test error")
    
    response = test_client.post('/recommend/buy', json={"situation": situation})
    
    assert response.status_code == 500
    assert response.json == {"error": "Test error"} 