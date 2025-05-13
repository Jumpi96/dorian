import pytest
from unittest.mock import Mock, patch
from app.clients.dynamodb import DynamoDBClient, DynamoDBError

@pytest.fixture
def mock_boto3():
    with patch('app.clients.dynamodb.boto3') as mock:
        yield mock

@pytest.fixture
def dynamodb_client(mock_boto3):
    return DynamoDBClient()

def test_get_table(dynamodb_client, mock_boto3):
    # Test getting a table
    table = dynamodb_client.get_table('test-table')
    mock_boto3.resource.return_value.Table.assert_called_once_with('test-table')

def test_put_item_success(dynamodb_client, mock_boto3):
    # Mock successful put_item
    mock_table = Mock()
    mock_boto3.resource.return_value.Table.return_value = mock_table
    
    # Test putting an item
    result = dynamodb_client.put_item('test-table', {'id': '1', 'data': 'test'})
    
    assert result is True
    mock_table.put_item.assert_called_once_with(Item={'id': '1', 'data': 'test'})

def test_put_item_error(dynamodb_client, mock_boto3):
    # Mock put_item error
    mock_table = Mock()
    mock_table.put_item.side_effect = Exception('DynamoDB error')
    mock_boto3.resource.return_value.Table.return_value = mock_table
    
    # Test error handling
    with pytest.raises(DynamoDBError):
        dynamodb_client.put_item('test-table', {'id': '1'})

def test_get_item_success(dynamodb_client, mock_boto3):
    # Mock successful get_item
    mock_table = Mock()
    mock_table.get_item.return_value = {'Item': {'id': '1', 'data': 'test'}}
    mock_boto3.resource.return_value.Table.return_value = mock_table
    
    # Test getting an item
    result = dynamodb_client.get_item('test-table', {'id': '1'})
    
    assert result == {'Item': {'id': '1', 'data': 'test'}}
    mock_table.get_item.assert_called_once_with(Key={'id': '1'})

def test_update_item_success(dynamodb_client, mock_boto3):
    # Mock successful update_item
    mock_table = Mock()
    mock_boto3.resource.return_value.Table.return_value = mock_table
    
    # Test updating an item
    result = dynamodb_client.update_item(
        'test-table',
        {'id': '1'},
        'SET #count = #count + :inc',
        {'#count': 'count'},
        {':inc': 1}
    )
    
    assert result is True
    mock_table.update_item.assert_called_once_with(
        Key={'id': '1'},
        UpdateExpression='SET #count = #count + :inc',
        ExpressionAttributeNames={'#count': 'count'},
        ExpressionAttributeValues={':inc': 1}
    )

def test_delete_item_success(dynamodb_client, mock_boto3):
    # Mock successful delete_item
    mock_table = Mock()
    mock_boto3.resource.return_value.Table.return_value = mock_table
    
    # Test deleting an item
    result = dynamodb_client.delete_item('test-table', {'id': '1'})
    
    assert result is True
    mock_table.delete_item.assert_called_once_with(Key={'id': '1'})

def test_query_success(dynamodb_client, mock_boto3):
    # Mock successful query
    mock_table = Mock()
    mock_table.query.return_value = {'Items': [{'id': '1', 'data': 'test'}]}
    mock_boto3.resource.return_value.Table.return_value = mock_table
    
    # Test querying items
    result = dynamodb_client.query(
        'test-table',
        'userId = :uid',
        {':uid': 'user1'}
    )
    
    assert result == {'Items': [{'id': '1', 'data': 'test'}]}
    mock_table.query.assert_called_once_with(
        KeyConditionExpression='userId = :uid',
        ExpressionAttributeValues={':uid': 'user1'},
        ScanIndexForward=True
    ) 