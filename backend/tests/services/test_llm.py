import pytest
from unittest.mock import Mock, patch
from app.services.llm import LLMService
from app.services.rate_limit import RateLimitError

@pytest.fixture
def mock_openai_client():
    with patch('app.services.llm.OpenAI') as mock:
        yield mock

@pytest.fixture
def mock_rate_limit_service():
    return Mock()

@pytest.fixture
def llm_service(mock_openai_client, mock_rate_limit_service):
    return LLMService(rate_limit_service=mock_rate_limit_service)

def test_get_completion_success(llm_service, mock_openai_client, mock_rate_limit_service):
    # Mock rate limit check
    mock_rate_limit_service.check_and_increment.return_value = True
    
    # Mock OpenAI response
    mock_response = Mock()
    mock_response.choices = [
        Mock(message=Mock(content='{"key": "value"}'))
    ]
    mock_openai_client.return_value.chat.completions.create.return_value = mock_response

    # Test the service
    response = llm_service.get_completion("test prompt", user_id="test_user")
    
    # Verify the response
    assert response == {"key": "value"}
    
    # Verify rate limit was checked
    mock_rate_limit_service.check_and_increment.assert_called_once_with("test_user")
    
    # Verify the API was called correctly
    mock_openai_client.return_value.chat.completions.create.assert_called_once_with(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "test prompt"}],
        response_format={"type": "json_object"}
    )

def test_get_completion_rate_limit_exceeded(llm_service, mock_rate_limit_service):
    # Mock rate limit check to raise RateLimitError
    mock_rate_limit_service.check_and_increment.side_effect = RateLimitError("Daily rate limit exceeded")

    # Test rate limit error
    with pytest.raises(RateLimitError) as exc_info:
        llm_service.get_completion("test prompt", user_id="test_user")
    
    assert "Daily rate limit exceeded" in str(exc_info.value)
    
    # Verify rate limit was checked
    mock_rate_limit_service.check_and_increment.assert_called_once_with("test_user")

def test_get_completion_custom_model(llm_service, mock_openai_client, mock_rate_limit_service):
    # Mock rate limit check
    mock_rate_limit_service.check_and_increment.return_value = True
    
    # Mock response
    mock_response = Mock()
    mock_response.choices = [
        Mock(message=Mock(content='{"key": "value"}'))
    ]
    mock_openai_client.return_value.chat.completions.create.return_value = mock_response

    # Test with custom model
    response = llm_service.get_completion("test prompt", user_id="test_user", model="gpt-4")
    
    # Verify rate limit was checked
    mock_rate_limit_service.check_and_increment.assert_called_once_with("test_user")
    
    # Verify the API was called with custom model
    mock_openai_client.return_value.chat.completions.create.assert_called_once_with(
        model="gpt-4",
        messages=[{"role": "user", "content": "test prompt"}],
        response_format={"type": "json_object"}
    )

def test_get_completion_api_error(llm_service, mock_openai_client, mock_rate_limit_service):
    # Mock rate limit check
    mock_rate_limit_service.check_and_increment.return_value = True
    
    # Mock API error
    mock_openai_client.return_value.chat.completions.create.side_effect = Exception("API Error")

    # Test error handling
    with pytest.raises(Exception) as exc_info:
        llm_service.get_completion("test prompt", user_id="test_user")
    
    assert "Failed to get completion from OpenAI" in str(exc_info.value)
    
    # Verify rate limit was checked
    mock_rate_limit_service.check_and_increment.assert_called_once_with("test_user")

def test_get_completion_invalid_json(llm_service, mock_openai_client, mock_rate_limit_service):
    # Mock rate limit check
    mock_rate_limit_service.check_and_increment.return_value = True
    
    # Mock response with invalid JSON
    mock_response = Mock()
    mock_response.choices = [
        Mock(message=Mock(content='invalid json'))
    ]
    mock_openai_client.return_value.chat.completions.create.return_value = mock_response

    # Test error handling for invalid JSON
    with pytest.raises(Exception) as exc_info:
        llm_service.get_completion("test prompt", user_id="test_user")
    
    assert "Failed to parse JSON response" in str(exc_info.value)
    
    # Verify rate limit was checked
    mock_rate_limit_service.check_and_increment.assert_called_once_with("test_user") 