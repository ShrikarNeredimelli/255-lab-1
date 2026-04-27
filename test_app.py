import pytest
from main import app, init_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['DATABASE'] = ':memory:'
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_contact(client):
    response = client.post('/', data={
        'name': 'Test User',
        'phone': '555-1234'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_missing_fields(client):
    response = client.post('/', data={
        'name': '',
        'phone': ''
    }, follow_redirects=True)
    assert response.status_code == 200
