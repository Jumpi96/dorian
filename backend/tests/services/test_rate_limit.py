import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timezone
from app.services.rate_limit import RateLimitService, RateLimitError
from app.clients.dynamodb import DynamoDBError

@pytest.fixture
def mock_dynamodb_client():
    return Mock()

@pytest.fixture
def rate_limit_service(mock_dynamodb_client):
    return RateLimitService(dynamodb_client=mock_dynamodb_client)

def test_first_request_of_day(rate_limit_service, mock_dynamodb_client):
    # Mock empty response for first request
    mock_dynamodb_client.get_item.return_value = {}
    
    # Test first request
    result = rate_limit_service.check_and_increment('user1')
    
    assert result is True
    mock_dynamodb_client.get_item.assert_called_once()
    mock_dynamodb_client.put_item.assert_called_once()
    # Verify the put_item call had the correct structure
    put_item_args = mock_dynamodb_client.put_item.call_args[1]
    assert put_item_args['table_name'] == 'dev-rate-limits'
    assert put_item_args['item']['userId'] == 'user1'
    assert put_item_args['item']['count'] == 1

@patch('app.services.rate_limit.datetime')
def test_increment_existing_count(mock_datetime, rate_limit_service, mock_dynamodb_client):
    # Mock datetime to return a fixed date
    mock_datetime.now.return_value = datetime(2024, 3, 20, tzinfo=timezone.utc)
    
    # Mock existing record with count < MAX_REQUESTS_PER_DAY
    mock_dynamodb_client.get_item.return_value = {
        'Item': {
            'id': 'user1:2024-03-20',
            'userId': 'user1',
            'count': 5,
            'createdAt': '2024-03-20T00:00:00+00:00'
        }
    }
    
    # Test incrementing count
    result = rate_limit_service.check_and_increment('user1')
    
    assert result is True
    mock_dynamodb_client.get_item.assert_called_once()
    mock_dynamodb_client.update_item.assert_called_once()
    # Verify the update_item call had the correct structure
    update_args = mock_dynamodb_client.update_item.call_args[1]
    assert update_args['table_name'] == 'dev-rate-limits'
    assert update_args['key'] == {'id': 'user1:2024-03-20'}
    assert update_args['update_expression'] == 'SET #count = #count + :inc'
    assert update_args['expression_attribute_names'] == {'#count': 'count'}
    assert update_args['expression_attribute_values'] == {':inc': 1}

@patch('app.services.rate_limit.datetime')
def test_rate_limit_exceeded(mock_datetime, rate_limit_service, mock_dynamodb_client):
    # Mock datetime to return a fixed date
    mock_datetime.now.return_value = datetime(2024, 3, 20, tzinfo=timezone.utc)
    
    # Mock existing record with count >= MAX_REQUESTS_PER_DAY
    mock_dynamodb_client.get_item.return_value = {
        'Item': {
            'id': 'user1:2024-03-20',
            'userId': 'user1',
            'count': 10,
            'createdAt': '2024-03-20T00:00:00+00:00'
        }
    }
    
    # Test rate limit exceeded
    with pytest.raises(RateLimitError) as exc_info:
        rate_limit_service.check_and_increment('user1')
    
    assert "Daily rate limit exceeded" in str(exc_info.value)
    mock_dynamodb_client.get_item.assert_called_once()
    mock_dynamodb_client.update_item.assert_not_called()

def test_dynamodb_error_fail_open(rate_limit_service, mock_dynamodb_client):
    # Mock DynamoDB error
    mock_dynamodb_client.get_item.side_effect = DynamoDBError("DynamoDB error")
    
    # Test fail-open behavior
    result = rate_limit_service.check_and_increment('user1')
    
    assert result is True
    mock_dynamodb_client.get_item.assert_called_once()
    mock_dynamodb_client.put_item.assert_not_called()
    mock_dynamodb_client.update_item.assert_not_called() 