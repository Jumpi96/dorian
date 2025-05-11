import pytest
from unittest.mock import Mock, patch
from app.services.recommendations import RecommendationsService, InsufficientWardrobeError

@pytest.fixture
def mock_llm_service():
    return Mock()

@pytest.fixture
def mock_wardrobe_service():
    return Mock()

@pytest.fixture
def recommendations_service(mock_llm_service, mock_wardrobe_service):
    return RecommendationsService(mock_llm_service, mock_wardrobe_service)

def test_get_outfit_recommendation_success(recommendations_service, mock_llm_service, mock_wardrobe_service):
    # Arrange
    user_id = "test_user"
    situation = "casual dinner"
    wardrobe_items = [
        {"description": "Black t-shirt"},
        {"description": "Blue jeans"},
        {"description": "White sneakers"},
        {"description": "Grey hoodie"}
    ]
    expected_recommendation = {
        "top": "Black t-shirt",
        "bottom": "Blue jeans",
        "shoes": "White sneakers",
        "outerwear": "Grey hoodie"
    }
    
    mock_wardrobe_service.get_wardrobe_items.return_value = wardrobe_items
    mock_llm_service.get_completion.return_value = expected_recommendation
    
    # Act
    recommendation = recommendations_service.get_outfit_recommendation(user_id, situation)
    
    # Assert
    assert recommendation == expected_recommendation
    mock_wardrobe_service.get_wardrobe_items.assert_called_once_with(user_id)
    mock_llm_service.get_completion.assert_called_once()
    
    # Verify prompt construction
    call_args = mock_llm_service.get_completion.call_args
    prompt = call_args[0][0]  # First positional arg is prompt
    user_id_arg = call_args[0][1]  # Second positional arg is user_id
    assert user_id_arg == user_id
    assert "Black t-shirt" in prompt
    assert "Blue jeans" in prompt
    assert "White sneakers" in prompt
    assert "Grey hoodie" in prompt
    assert situation in prompt

def test_get_outfit_recommendation_insufficient_items(recommendations_service, mock_wardrobe_service):
    # Arrange
    user_id = "test_user"
    situation = "casual dinner"
    wardrobe_items = [
        {"description": "Black t-shirt"},
        {"description": "Blue jeans"}
    ]
    
    mock_wardrobe_service.get_wardrobe_items.return_value = wardrobe_items
    
    # Act & Assert
    with pytest.raises(InsufficientWardrobeError) as exc_info:
        recommendations_service.get_outfit_recommendation(user_id, situation)
    
    assert "Need at least 3 items" in str(exc_info.value)
    assert "Current items: 2" in str(exc_info.value)
    mock_wardrobe_service.get_wardrobe_items.assert_called_once_with(user_id)

def test_get_outfit_recommendation_llm_error(recommendations_service, mock_llm_service, mock_wardrobe_service):
    # Arrange
    user_id = "test_user"
    situation = "casual dinner"
    wardrobe_items = [
        {"description": "Black t-shirt"},
        {"description": "Blue jeans"},
        {"description": "White sneakers"}
    ]
    
    mock_wardrobe_service.get_wardrobe_items.return_value = wardrobe_items
    mock_llm_service.get_completion.side_effect = Exception("LLM error")
    
    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        recommendations_service.get_outfit_recommendation(user_id, situation)
    
    assert str(exc_info.value) == "LLM error"
    mock_wardrobe_service.get_wardrobe_items.assert_called_once_with(user_id)
    mock_llm_service.get_completion.assert_called_once() 