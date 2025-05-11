import pytest
from unittest.mock import Mock, patch
from app.services.llm import LLMService

@pytest.fixture
def mock_openai_client():
    with patch('app.services.llm.OpenAI') as mock:
        yield mock

@pytest.fixture
def llm_service(mock_openai_client):
    return LLMService()

def test_get_completion_success(llm_service, mock_openai_client):
    # Mock response
    mock_response = Mock()
    mock_response.choices = [
        Mock(message=Mock(content='{"key": "value"}'))
    ]
    mock_openai_client.return_value.chat.completions.create.return_value = mock_response

    # Test the service
    response = llm_service.get_completion("test prompt")
    
    # Verify the response
    assert response == {"key": "value"}
    
    # Verify the API was called correctly
    mock_openai_client.return_value.chat.completions.create.assert_called_once_with(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "test prompt"}],
        response_format={"type": "json_object"}
    )

def test_get_completion_custom_model(llm_service, mock_openai_client):
    # Mock response
    mock_response = Mock()
    mock_response.choices = [
        Mock(message=Mock(content='{"key": "value"}'))
    ]
    mock_openai_client.return_value.chat.completions.create.return_value = mock_response

    # Test with custom model
    response = llm_service.get_completion("test prompt", model="gpt-4")
    
    # Verify the API was called with custom model
    mock_openai_client.return_value.chat.completions.create.assert_called_once_with(
        model="gpt-4",
        messages=[{"role": "user", "content": "test prompt"}],
        response_format={"type": "json_object"}
    )

def test_get_completion_api_error(llm_service, mock_openai_client):
    # Mock API error
    mock_openai_client.return_value.chat.completions.create.side_effect = Exception("API Error")

    # Test error handling
    with pytest.raises(Exception) as exc_info:
        llm_service.get_completion("test prompt")
    
    assert "Failed to get completion from OpenAI" in str(exc_info.value)

def test_get_completion_invalid_json(llm_service, mock_openai_client):
    # Mock response with invalid JSON
    mock_response = Mock()
    mock_response.choices = [
        Mock(message=Mock(content='invalid json'))
    ]
    mock_openai_client.return_value.chat.completions.create.return_value = mock_response

    # Test error handling for invalid JSON
    with pytest.raises(Exception) as exc_info:
        llm_service.get_completion("test prompt")
    
    assert "Failed to parse JSON response" in str(exc_info.value) 