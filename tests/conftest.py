"""
Test configuration and fixtures for Aim for the Stars application
"""
import pytest
import tempfile
import os
import re
from app import create_app
from models import db
from models import User, DiaryEntry, DailyStats, Goal


def extract_csrf_token(response_data):
    """Extract CSRF token from response data"""
    if b'csrf-token' in response_data:
        # Look specifically for the csrf-token meta tag
        match = re.search(b'<meta[^>]*name="csrf-token"[^>]*content="([^"]+)"', response_data)
        if match:
            return match.group(1).decode('utf-8')
    return None


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app('testing')
    
    # Ensure the app context is available
    with app.app_context():
        # Create all tables
        db.create_all()
        
        yield app
        
        # Clean up after the test
        db.session.remove()
        db.drop_all()
    
    # Close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def sample_user(app):
    """Create a sample user for testing."""
    with app.app_context():
        user = User(
            email='test@example.com',
            password='testpassword123',
            user_name='Test User'
        )
        db.session.add(user)
        db.session.commit()
        # Refresh the user to ensure it's attached to the session
        db.session.refresh(user)
        return user


@pytest.fixture
def sample_diary_entry(app, sample_user):
    """Create a sample diary entry for testing."""
    with app.app_context():
        # Get the user ID directly to avoid session issues
        user_id = sample_user.id
        entry = DiaryEntry(
            user_id=user_id,
            content='This is a test diary entry',
            rating=5
        )
        db.session.add(entry)
        db.session.commit()
        db.session.refresh(entry)
        return entry


@pytest.fixture
def sample_goal(app, sample_user):
    """Create a sample goal for testing."""
    from datetime import datetime, timedelta
    
    with app.app_context():
        # Get the user ID directly to avoid session issues
        user_id = sample_user.id
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=6)
        
        goal = Goal(
            user_id=user_id,
            category='EXERCISE',
            title='Test Goal',
            description='A test goal for testing',
            week_start=start_date,
            week_end=end_date
        )
        db.session.add(goal)
        db.session.commit()
        db.session.refresh(goal)
        return goal


@pytest.fixture
def sample_daily_stats(app, sample_user):
    """Create sample daily stats for testing."""
    from datetime import date
    
    with app.app_context():
        # Get the user ID directly to avoid session issues
        user_id = sample_user.id
        stats = DailyStats(
            user_id=user_id,
            date=date.today(),
            points=10,
            current_streak=3,
            longest_streak=5
        )
        db.session.add(stats)
        db.session.commit()
        db.session.refresh(stats)
        return stats


@pytest.fixture
def auth_headers(sample_user):
    """Get authentication headers for a logged-in user."""
    return {'Cookie': f'user_id={sample_user.id}'} 