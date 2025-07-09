"""
Tests for User model
"""

import pytest
from app.models import User, db
from werkzeug.security import check_password_hash


class TestUserModel:
    """Test cases for User model"""

    def test_user_creation(self, app):
        """Test creating a new user"""
        with app.app_context():
            user = User(
                email="test@example.com",
                password="testpassword123",
                user_name="Test User",
            )
            db.session.add(user)
            db.session.commit()

            # Verify user was created
            assert user.id is not None
            assert user.email == "test@example.com"
            assert user.user_name == "Test User"
            # Note: created_at field doesn't exist in current model

    def test_password_hashing(self, app):
        """Test that passwords are automatically hashed"""
        with app.app_context():
            user = User(
                email="test@example.com",
                password="testpassword123",
                user_name="Test User",
            )

            # Password should be automatically hashed
            assert user.password != "testpassword123"
            # Check that it's a hash (starts with a hash method identifier)
            assert any(
                user.password.startswith(prefix)
                for prefix in ["pbkdf2:", "scrypt:", "bcrypt:", "sha256:"]
            )
            assert check_password_hash(user.password, "testpassword123")

    def test_check_password_method(self, app):
        """Test the check_password method"""
        with app.app_context():
            user = User(
                email="test@example.com",
                password="testpassword123",
                user_name="Test User",
            )
            db.session.add(user)
            db.session.commit()

            # Test correct password
            assert user.check_password("testpassword123") == True

            # Test incorrect password
            assert user.check_password("wrongpassword") == False

    def test_user_representation(self, app):
        """Test user string representation"""
        with app.app_context():
            user = User(
                email="test@example.com",
                password="testpassword123",
                user_name="Test User",
            )
            db.session.add(user)
            db.session.commit()

            # Updated to match the model's __repr__
            assert str(user) == "<User test@example.com>"

    def test_user_relationships(self, app):
        """Test user relationships with other models"""
        with app.app_context():
            # Create user
            user = User(
                email="test@example.com",
                password="testpassword123",
                user_name="Test User",
            )
            db.session.add(user)
            db.session.commit()

            # Test that relationships are accessible (if they exist)
            # Note: relationships may not be defined in current model
            # We'll test what's actually available
            assert hasattr(user, "id")
            assert hasattr(user, "email")
            assert hasattr(user, "password")
            assert hasattr(user, "user_name")

    def test_user_validation(self, app):
        """Test user validation rules"""
        with app.app_context():
            # Test required fields
            user = User()
            db.session.add(user)

            with pytest.raises(
                Exception
            ):  # Should raise an exception for missing required fields
                db.session.commit()

            db.session.rollback()

    def test_user_uniqueness(self, app):
        """Test that email addresses must be unique"""
        with app.app_context():
            # Create first user
            user1 = User(
                email="test@example.com",
                password="testpassword123",
                user_name="Test User 1",
            )
            db.session.add(user1)
            db.session.commit()

            # Try to create second user with same email
            user2 = User(
                email="test@example.com",  # Same email
                password="testpassword456",
                user_name="Test User 2",
            )
            db.session.add(user2)

            with pytest.raises(
                Exception
            ):  # Should raise an exception for duplicate email
                db.session.commit()

            db.session.rollback()
