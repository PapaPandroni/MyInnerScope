"""
Tests for authentication routes
"""
import pytest
from models import User, db


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
    
    def test_register_new_user(self, client, app):
        """Test registering a new user"""
        with app.app_context():
            response = client.post('/register', data={
                'email': 'newuser@example.com',
                'password': 'newpassword123',
                'confirm_password': 'newpassword123',
                'user_name': 'New User'
            }, follow_redirects=True)
            
            assert response.status_code == 200
            
            # Check that user was created in database
            user = User.query.filter_by(email='newuser@example.com').first()
            assert user is not None
            assert user.user_name == 'New User'
    
    def test_register_existing_user(self, client, sample_user):
        """Test registering with an existing email"""
        response = client.post('/register', data={
            'email': 'test@example.com',  # Same as sample_user
            'password': 'password123',
            'confirm_password': 'password123',
            'user_name': 'Another User'
        }, follow_redirects=True)
        
        # Should show an error or redirect
        assert response.status_code == 200
    
    def test_login_valid_user(self, client, sample_user):
        """Test logging in with valid credentials"""
        response = client.post('/login', data={
            'email': 'test@example.com',
            'password': 'testpassword123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    def test_login_invalid_credentials(self, client):
        """Test logging in with invalid credentials"""
        response = client.post('/login', data={
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    def test_logout(self, client, sample_user):
        """Test logout functionality"""
        # First login
        client.post('/login', data={
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        
        # Then logout
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200 