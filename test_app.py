import pytest
import os
import sqlite3
from unittest.mock import patch

# Patch the DATABASE path before importing app
import main
main.DATABASE = ':memory:'

from main import app, init_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    main.DATABASE = ':memory:'
    with app.test_client() as client:
        with app.app_context():
            db = sqlite3.connect(':memory:')
            db.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL
                );
            ''')
            db.commit()
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
