import pytest
from datetime import datetime, UTC
from unittest.mock import Mock, patch
from app.services.trips import TripsService, TripNotFoundError
from app.clients.dynamodb import DynamoDBError

@pytest.fixture
def mock_dynamodb():
    return Mock()

@pytest.fixture
def trips_service(mock_dynamodb):
    return TripsService(mock_dynamodb)

def test_save_trip(trips_service, mock_dynamodb):
    # Arrange
    user_id = "test_user"
    description = "Test Trip"
    packing_list = {"tops": ["shirt1", "shirt2"]}
    timestamp = datetime.now(UTC).isoformat()
    
    with patch('app.services.trips.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime.fromisoformat(timestamp)
        mock_datetime.UTC = UTC
        
        # Act
        trip_id = trips_service.save_trip(user_id, description, packing_list)
        
        # Assert
        assert trip_id.startswith("trip_")
        mock_dynamodb.put_item.assert_called_once_with(
            table_name='dev-trips',
            item={
                "tripId": trip_id,
                "userId": user_id,
                "description": description,
                "packingList": packing_list,
                "createdAt": timestamp
            }
        )

def test_get_user_trip(trips_service, mock_dynamodb):
    # Arrange
    user_id = "test_user"
    mock_trip = {
        "tripId": "trip_123",
        "userId": user_id,
        "description": "Test Trip",
        "packingList": {"tops": ["shirt1"]},
        "createdAt": "2024-03-20T00:00:00+00:00"
    }
    mock_dynamodb.query.return_value = {"Items": [mock_trip]}
    
    # Act
    trip = trips_service.get_user_trip(user_id)
    
    # Assert
    assert trip == mock_trip
    mock_dynamodb.query.assert_called_once_with(
        table_name='dev-trips',
        key_condition_expression='userId = :uid',
        expression_attribute_values={':uid': user_id},
        scan_index_forward=False,
        limit=1
    )

def test_get_user_trip_not_found(trips_service, mock_dynamodb):
    # Arrange
    user_id = "test_user"
    mock_dynamodb.query.return_value = {"Items": []}
    
    # Act
    trip = trips_service.get_user_trip(user_id)
    
    # Assert
    assert trip is None

def test_delete_trip(trips_service, mock_dynamodb):
    # Arrange
    user_id = "test_user"
    trip_id = "trip_123"
    mock_dynamodb.get_item.return_value = {
        "Item": {
            "tripId": trip_id,
            "userId": user_id
        }
    }
    
    # Act
    trips_service.delete_trip(user_id, trip_id)
    
    # Assert
    mock_dynamodb.get_item.assert_called_once_with(
        table_name='dev-trips',
        key={
            'userId': user_id,
            'tripId': trip_id
        }
    )
    mock_dynamodb.delete_item.assert_called_once_with(
        table_name='dev-trips',
        key={
            'userId': user_id,
            'tripId': trip_id
        }
    )

def test_delete_trip_not_found(trips_service, mock_dynamodb):
    # Arrange
    user_id = "test_user"
    trip_id = "trip_123"
    mock_dynamodb.get_item.return_value = {}
    
    # Act & Assert
    with pytest.raises(TripNotFoundError):
        trips_service.delete_trip(user_id, trip_id)

def test_delete_trip_dynamodb_error(trips_service, mock_dynamodb):
    # Arrange
    user_id = "test_user"
    trip_id = "trip_123"
    mock_dynamodb.get_item.side_effect = DynamoDBError("Test error")
    
    # Act & Assert
    with pytest.raises(DynamoDBError):
        trips_service.delete_trip(user_id, trip_id) 