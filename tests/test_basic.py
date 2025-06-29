"""
Basic tests for the Aim for the Stars application
"""
import pytest
from models import User, db
from tests.conftest import extract_csrf_token


def test_index_route(client):
    """Test that the index route returns 200 and contains expected content"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Aim for the Stars' in response.data


def test_register_route(client):
    """Test that the register route returns 200 and contains expected content"""
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data


def test_login_route(client):
    """Test that the login route returns 200 and contains expected content"""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data


def test_register_form_submission(client):
    """Test registering a new user with CSRF token"""
    response = client.get('/register')
    assert response.status_code == 200
    csrf_token = extract_csrf_token(response.data)
    response = client.post('/register', data={
        'email': 'newuser@example.com',
        'password': 'TestPassword123',
        'password_again': 'TestPassword123',
        'user_name': 'New User',
        'csrf_token': csrf_token
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Registration successful' in response.data or b'Login' in response.data
    with client.application.app_context():
        user = User.query.filter_by(email='newuser@example.com').first()
        assert user is not None
        assert user.user_name == 'New User'


def test_login_form_submission(client):
    """Test logging in with valid credentials and CSRF token"""
    # Register the user first
    response = client.get('/register')
    csrf_token = extract_csrf_token(response.data)
    client.post('/register', data={
        'email': 'test@example.com',
        'password': 'TestPassword123',
        'password_again': 'TestPassword123',
        'user_name': 'Test User',
        'csrf_token': csrf_token
    }, follow_redirects=True)
    # Now login
    response = client.get('/login')
    csrf_token = extract_csrf_token(response.data)
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'TestPassword123',
        'csrf_token': csrf_token
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Diary' in response.data or b'diary' in response.data or b'Logout' in response.data


def test_protected_routes_require_login(client):
    """Test that protected routes redirect to login when not authenticated"""
    # Test diary route
    response = client.get('/diary', follow_redirects=True)
    assert response.status_code == 200
    # Should redirect to login page
    assert b'Login' in response.data
    
    # Test goals route
    response = client.get('/goals', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
    
    # Test progress route
    response = client.get('/progress', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data


def test_database_connection(app):
    """Test that database connection works"""
    with app.app_context():
        # Try to create a simple user
        user = User(
            email='test@example.com',
            password='testpassword123',
            user_name='Test User'
        )
        db.session.add(user)
        db.session.commit()
        
        # Verify user was created
        assert user.id is not None
        
        # Clean up
        db.session.delete(user)
        db.session.commit()


def test_static_files(client):
    """Test that static files are served correctly"""
    # Test CSS files
    response = client.get('/static/css/custom_css.css')
    assert response.status_code == 200
    
    # Test JS files
    response = client.get('/static/js/goals.js')
    assert response.status_code == 200


def test_error_pages(client):
    """Test that error pages are handled correctly"""
    # Test 404 page
    response = client.get('/nonexistent-route')
    assert response.status_code == 404 