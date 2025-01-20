import pytest
from app import create_app
from app.database import init_db, get_db_connection

def setup_module(module):
    """Setup the app and database for testing"""
    init_db()
    global app
    app = create_app()
    app.testing = True

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_generate_api_key(client):
    response = client.post('/generate_api_key')
    assert response.status_code == 201
    json_data = response.get_json()
    assert 'key' in json_data