"""
Tests for the User model
"""
import pytest
from models import User, db


class TestUserModel:
    """Test cases for User model"""
    
    def test_create_user(self, app):
        """Test creating a new user"""
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
            assert user.password == 'testpassword123'
            assert user.user_name == 'Test User'
    
    def test_user_email_uniqueness(self, app):
        """Test that email addresses must be unique"""
        with app.app_context():
            # Create first user
            user1 = User(
                email='test@example.com',
                password='password1',
                user_name='User 1'
            )
            db.session.add(user1)
            db.session.commit()
            
            # Try to create second user with same email
            user2 = User(
                email='test@example.com',
                password='password2',
                user_name='User 2'
            )
            db.session.add(user2)
            
            # This should raise an integrity error
            with pytest.raises(Exception):
                db.session.commit()
    
    def test_user_required_fields(self, app):
        """Test that required fields are enforced"""
        with app.app_context():
            # Test missing email
            user = User(password='password', user_name='Test')
            db.session.add(user)
            with pytest.raises(Exception):
                db.session.commit()
            
            db.session.rollback()
            
            # Test missing password
            user = User(email='test@example.com', user_name='Test')
            db.session.add(user)
            with pytest.raises(Exception):
                db.session.commit()
    
    def test_user_relationships(self, app, sample_user, sample_diary_entry, sample_goal, sample_daily_stats):
        """Test user relationships with other models"""
        with app.app_context():
            # Test diary entries relationship
            assert len(sample_user.entries) == 1
            assert sample_user.entries[0].content == 'This is a test diary entry'
            
            # Test goals relationship
            assert len(sample_user.goals) == 1
            assert sample_user.goals[0].title == 'Test Goal'
            
            # Test daily stats relationship
            assert len(sample_user.daily_stats) == 1
            assert sample_user.daily_stats[0].points == 10 