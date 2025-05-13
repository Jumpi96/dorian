import pytest
from unittest.mock import Mock
from app.services.text_transformations import TextTransformationsService

@pytest.fixture
def mock_llm():
    return Mock()

@pytest.fixture
def text_transformations_service(mock_llm):
    return TextTransformationsService(mock_llm)

def test_generate_trip_title(text_transformations_service, mock_llm):
    # Arrange
    situation = "Weekend trip to the beach in summer"
    user_id = "test_user"
    mock_llm.get_completion.return_value = {"title": "Summer Beach Weekend"}
    
    # Act
    title = text_transformations_service.generate_trip_title(situation, user_id)
    
    # Assert
    assert title == "Summer Beach Weekend"
    mock_llm.get_completion.assert_called_once()
    prompt = mock_llm.get_completion.call_args[0][0]
    assert situation in prompt
    assert "JSON" in prompt
    assert "title" in prompt

def test_generate_trip_title_with_quotes(text_transformations_service, mock_llm):
    # Arrange
    situation = "Weekend trip to the beach"
    user_id = "test_user"
    mock_llm.get_completion.return_value = {"title": '"Summer Beach Weekend"'}
    
    # Act
    title = text_transformations_service.generate_trip_title(situation, user_id)
    
    # Assert
    assert title == "Summer Beach Weekend"

def test_generate_trip_title_empty_response(text_transformations_service, mock_llm):
    # Arrange
    situation = "Weekend trip to the beach"
    user_id = "test_user"
    mock_llm.get_completion.return_value = {}
    
    # Act
    title = text_transformations_service.generate_trip_title(situation, user_id)
    
    # Assert
    assert title == ""

def test_generate_trip_title_llm_error(text_transformations_service, mock_llm):
    # Arrange
    situation = "Weekend trip to the beach"
    user_id = "test_user"
    mock_llm.get_completion.side_effect = Exception("LLM error")
    
    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        text_transformations_service.generate_trip_title(situation, user_id)
    assert str(exc_info.value) == "LLM error" 