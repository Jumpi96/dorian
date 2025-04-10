import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_endpoint(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert response.json == {"user": "fakeUserId"}

def test_callback_endpoint(client):
    response = client.get('/auth/callback')
    assert response.status_code == 200
    assert response.json == {"user": "fakeUserId"} 