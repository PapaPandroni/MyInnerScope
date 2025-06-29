"""
Basic tests to demonstrate the testing framework
"""
import pytest
from models import User, db
from sqlalchemy import text


def test_app_creation(app):
    """Test that the app can be created"""
    assert app is not None
    assert app.config['TESTING'] is True


def test_database_creation(app):
    """Test that database tables can be created"""
    with app.app_context():
        # This should work without errors
        db.create_all()
        
        # Check that tables exist
        with db.engine.connect() as conn:
            result = conn.execute(text('SELECT name FROM sqlite_master WHERE type="table"'))
            tables = result.fetchall()
            table_names = [table[0] for table in tables]
            
            assert 'user' in table_names
            assert 'diary_entry' in table_names
            assert 'goal' in table_names
            assert 'daily_stats' in table_names


def test_user_creation(app):
    """Test creating a user in the database"""
    with app.app_context():
        user = User(
            email='test@example.com',
            password='testpassword123',
            user_name='Test User'
        )
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.email == 'test@example.com'


def test_index_route(client):
    """Test that the index route returns a response"""
    response = client.get('/')
    assert response.status_code == 200


def test_register_page(client):
    """Test that the register page loads"""
    response = client.get('/register')
    assert response.status_code == 200 