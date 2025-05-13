import pytest
from unittest.mock import Mock, patch
from app.services.trips import TripNotFoundError

@pytest.fixture
def mock_trips_service():
    return Mock()

@pytest.fixture
def client(mock_trips_service):
    from flask import Flask
    app = Flask(__name__)
    app.config['TESTING'] = True
    
    # Mock the auth decorator
    def fake_requires_auth(f):
        def wrapped(*args, **kwargs):
            from flask import request
            request.user = {'sub': 'test_user'}
            return f(*args, **kwargs)
        wrapped.__name__ = f.__name__
        return wrapped
    
    # Monkey patch it into trips module before init
    from app.routes import trips
    trips.requires_auth = fake_requires_auth
    
    # Initialize routes with mocked service
    from app.routes.trips import init_trip_routes
    init_trip_routes(app, mock_trips_service)
    
    with app.test_client() as test_client:
        yield test_client, mock_trips_service

def test_get_user_trip(client):
    test_client, mock_trips_service = client
    # Arrange
    mock_trip = {
        "tripId": "trip_123",
        "userId": "test_user",
        "description": "Test Trip",
        "packingList": {"tops": ["shirt1"]},
        "createdAt": "2024-03-20T00:00:00+00:00"
    }
    mock_trips_service.get_user_trip.return_value = mock_trip
    
    # Act
    response = test_client.get('/trips')
    
    # Assert
    assert response.status_code == 200
    assert response.json == mock_trip
    mock_trips_service.get_user_trip.assert_called_once_with('test_user')

def test_get_user_trip_not_found(client):
    test_client, mock_trips_service = client
    # Arrange
    mock_trips_service.get_user_trip.return_value = None
    
    # Act
    response = test_client.get('/trips')
    
    # Assert
    assert response.status_code == 404
    assert response.json['type'] == 'not_found'
    assert 'No trip found' in response.json['error']

def test_delete_trip(client):
    test_client, mock_trips_service = client
    # Arrange
    trip_id = "trip_123"
    
    # Act
    response = test_client.delete(f'/trips/{trip_id}')
    
    # Assert
    assert response.status_code == 200
    assert response.json['message'] == 'Trip deleted successfully'
    mock_trips_service.delete_trip.assert_called_once_with('test_user', trip_id)

def test_delete_trip_not_found(client):
    test_client, mock_trips_service = client
    # Arrange
    trip_id = "trip_123"
    mock_trips_service.delete_trip.side_effect = TripNotFoundError(f"Trip {trip_id} not found")
    
    # Act
    response = test_client.delete(f'/trips/{trip_id}')
    
    # Assert
    assert response.status_code == 500
    assert 'Trip trip_123 not found' in response.json['error'] 