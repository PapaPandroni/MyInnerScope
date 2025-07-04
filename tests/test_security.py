
import pytest
from app import create_app
from models import User, db, Goal
from datetime import datetime

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def logged_in_client(client):
    """A test client that is logged in."""
    client.post('/register', data={'email': 'test@test.com', 'password': 'password', 'password_again': 'password'})
    client.post('/login', data={'email': 'test@test.com', 'password': 'password'})
    return client

def test_login_rate_limit(client):
    """Test that the login route is rate-limited."""
    for i in range(25):
        response = client.post('/login', data={'email': 'test@test.com', 'password': 'password'})
        if i < 20:
            assert response.status_code != 429
        else:
            assert response.status_code == 429

def test_register_rate_limit(client):
    """Test that the register route is rate-limited."""
    for i in range(25):
        response = client.post('/register', data={'email': f'test{i}@test.com', 'password': 'password', 'password_again': 'password'})
        if i < 20:
            assert response.status_code != 429
        else:
            assert response.status_code == 429

def test_diary_entry_rate_limit(logged_in_client):
    """Test that the diary entry route is rate-limited."""
    for i in range(35):
        response = logged_in_client.post('/diary', data={'content': 'Test content', 'rating': 1})
        if i < 30:
            assert response.status_code != 429
        else:
            assert response.status_code == 429

def test_create_goal_rate_limit(logged_in_client):
    """Test that the create goal route is rate-limited."""
    for i in range(35):
        response = logged_in_client.post('/goals/create', data={'title': 'Test Goal', 'category': 'LEARNING', 'description': 'Test description'})
        if i < 30:
            assert response.status_code != 429
        else:
            assert response.status_code == 429

def test_delete_account_rate_limit(logged_in_client):
    """Test that the delete account route is rate-limited."""
    for i in range(25):
        response = logged_in_client.post('/delete-account', data={'password': 'password'})
        if i < 20:
            assert response.status_code != 429
        else:
            assert response.status_code == 429
