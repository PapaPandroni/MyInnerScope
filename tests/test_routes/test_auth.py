"""
Tests for authentication routes
"""
import pytest
from models import User, db
from tests.conftest import extract_csrf_token


class TestAuthRoutes:
    """Test cases for authentication routes"""
    
    def test_index_route(self, client):
        """Test the main index route"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Aim for the Stars' in response.data
    
    def test_register_page(self, client):
        """Test the registration page loads"""
        response = client.get('/register')
        assert response.status_code == 200
        assert b'Register' in response.data
    
    def test_login_page(self, client):
        """Test the login page loads"""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Login' in response.data
    
    def test_register_new_user(self, client):
        """Test registering a new user"""
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
    
    def test_register_existing_user(self, client):
        """Test registering with an existing email"""
        # Register a user first
        response = client.get('/register')
        csrf_token = extract_csrf_token(response.data)
        client.post('/register', data={
            'email': 'test@example.com',
            'password': 'TestPassword123',
            'password_again': 'TestPassword123',
            'user_name': 'Test User',
            'csrf_token': csrf_token
        }, follow_redirects=True)
        # Try to register again with the same email
        response = client.get('/register')
        csrf_token = extract_csrf_token(response.data)
        response = client.post('/register', data={
            'email': 'test@example.com',
            'password': 'AnotherPassword1',
            'password_again': 'AnotherPassword1',
            'user_name': 'Another User',
            'csrf_token': csrf_token
        }, follow_redirects=True)
        assert response.status_code == 400
        assert b'Email already registered' in response.data
    
    def test_login_valid_user(self, client):
        """Test logging in with valid credentials"""
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
    
    def test_login_invalid_credentials(self, client):
        """Test logging in with invalid credentials"""
        response = client.get('/login')
        csrf_token = extract_csrf_token(response.data)
        response = client.post('/login', data={
            'email': 'nonexistent@example.com',
            'password': 'WrongPassword1',
            'csrf_token': csrf_token
        }, follow_redirects=True)
        assert response.status_code == 401 or b'Incorrect password' in response.data or b'No user found' in response.data
    
    def test_logout(self, client):
        """Test logout functionality"""
        # Register and login first
        response = client.get('/register')
        csrf_token = extract_csrf_token(response.data)
        client.post('/register', data={
            'email': 'test@example.com',
            'password': 'TestPassword123',
            'password_again': 'TestPassword123',
            'user_name': 'Test User',
            'csrf_token': csrf_token
        }, follow_redirects=True)
        response = client.get('/login')
        csrf_token = extract_csrf_token(response.data)
        client.post('/login', data={
            'email': 'test@example.com',
            'password': 'TestPassword123',
            'csrf_token': csrf_token
        }, follow_redirects=True)
        # Then logout
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'logged out' in response.data or b'Login' in response.data 