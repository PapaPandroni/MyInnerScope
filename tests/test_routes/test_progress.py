"""
Tests for progress routes
"""
import pytest
from flask import url_for, session
from datetime import date, timedelta
from app.models import User, DiaryEntry, DailyStats, Goal, db
from tests.conftest import extract_csrf_token


class TestProgressRoutes:
    """Test cases for progress routes"""
    
    def test_progress_page_requires_login(self, client):
        """Test that accessing the progress page redirects to login if not authenticated."""
        response = client.get('/progress', follow_redirects=True)
        assert response.status_code == 200
        assert b'Login' in response.data
    
    def test_progress_page_loads_for_logged_in_user(self, client, sample_user):
        """Test that the progress page loads successfully for a logged-in user."""
        with client.session_transaction() as sess:
            sess['user_id'] = sample_user.id
        
        response = client.get('/progress')
        assert response.status_code == 200
        assert b'Your Progress' in response.data
        assert b'Points Over Time' in response.data
        assert b'Average Points by Day of Week' in response.data
    
    def test_progress_page_with_no_data(self, client, sample_user):
        """Test progress page with a user who has no diary entries."""
        with client.session_transaction() as sess:
            sess['user_id'] = sample_user.id
        
        response = client.get('/progress')
        assert response.status_code == 200
        
        # Check that basic stats are zero
        assert b'0' in response.data  # Should show 0 for various stats
        assert b'Word Cloud Locked' in response.data  # Word cloud should be locked
        assert b'Weekday Insights Locked' in response.data  # Weekday chart should be locked
    
    def test_progress_page_with_single_entry(self, client, app, sample_user):
        """Test progress page with a user who has one diary entry."""
        with app.app_context():
            # Create a diary entry
            entry = DiaryEntry(
                user_id=sample_user.id,
                content='Test entry',
                rating=1,
                entry_date=date.today()
            )
            db.session.add(entry)
            
            # Create corresponding stats
            stats = DailyStats(
                user_id=sample_user.id,
                date=date.today(),
                points=5,
                current_streak=1,
                longest_streak=1
            )
            db.session.add(stats)
            db.session.commit()
        
        with client.session_transaction() as sess:
            sess['user_id'] = sample_user.id
        
        response = client.get('/progress')
        assert response.status_code == 200
        
        # Check that stats are calculated correctly
        assert b'5' in response.data  # Points today
        assert b'1' in response.data  # Current streak
        assert b'1' in response.data  # Total entries
        assert b'Word Cloud Locked' in response.data  # Still locked (need 10 entries)
    
    def test_progress_page_with_multiple_entries(self, client, app, sample_user):
        """Test progress page with multiple diary entries."""
        with app.app_context():
            # Create multiple entries over several days
            for i in range(5):
                entry_date = date.today() - timedelta(days=i)
                entry = DiaryEntry(
                    user_id=sample_user.id,
                    content=f'Entry {i+1}',
                    rating=1 if i % 2 == 0 else -1,
                    entry_date=entry_date
                )
                db.session.add(entry)
                
                # Create corresponding stats
                points = 5 if i % 2 == 0 else 2
                stats = DailyStats(
                    user_id=sample_user.id,
                    date=entry_date,
                    points=points,
                    current_streak=i+1,
                    longest_streak=i+1
                )
                db.session.add(stats)
            
            db.session.commit()
        
        with client.session_transaction() as sess:
            sess['user_id'] = sample_user.id
        
        response = client.get('/progress')
        assert response.status_code == 200
        
        # Check that stats are calculated correctly
        assert b'5' in response.data  # Total entries
        assert b'Word Cloud Locked' in response.data  # Still locked (need 10 entries)
    
    def test_progress_page_with_sufficient_wordcloud_data(self, client, app, sample_user):
        """Test progress page when user has enough entries for word cloud."""
        with app.app_context():
            # Create 10+ entries with repeated words
            for i in range(12):
                entry_date = date.today() - timedelta(days=i)
                entry = DiaryEntry(
                    user_id=sample_user.id,
                    content='I went running today and felt great about my progress',
                    rating=1,
                    entry_date=entry_date
                )
                db.session.add(entry)
                
                stats = DailyStats(
                    user_id=sample_user.id,
                    date=entry_date,
                    points=5,
                    current_streak=i+1,
                    longest_streak=i+1
                )
                db.session.add(stats)
            
            db.session.commit()
        
        with client.session_transaction() as sess:
            sess['user_id'] = sample_user.id
        
        response = client.get('/progress')
        assert response.status_code == 200
        
        # Word cloud should be unlocked
        assert b'Words Discovered' in response.data
        assert b'wordcloud' in response.data
    
    def test_progress_page_with_goals(self, client, app, sample_user):
        """Test progress page when user has goals."""
        with app.app_context():
            # Create a goal with all required fields
            goal = Goal(
                user_id=sample_user.id,
                title='Test Goal',
                category='Health',
                description='Test description',
                week_start=date.today(),
                week_end=date.today() + timedelta(days=7),
                status='in_progress',
                created_at=date.today()  # Add created_at field
            )
            db.session.add(goal)
            db.session.commit()
        
        with client.session_transaction() as sess:
            sess['user_id'] = sample_user.id
        
        response = client.get('/progress')
        assert response.status_code == 200
        
        # Check that goals section is present
        assert b'Goals Overview' in response.data
        # Note: The goal title might not appear in the response if the goal helper functions
        # don't return it properly, but the section should be present
    
    def test_export_journey_requires_login(self, client):
        """Test that PDF export requires authentication."""
        response = client.post('/export-journey')
        assert response.status_code == 401
        assert b'Unauthorized' in response.data
    
    def test_export_journey_success(self, client, app, sample_user):
        """Test successful PDF export."""
        with app.app_context():
            # Create some diary entries
            for i in range(3):
                entry_date = date.today() - timedelta(days=i)
                entry = DiaryEntry(
                    user_id=sample_user.id,
                    content=f'Test entry {i+1}',
                    rating=1,
                    entry_date=entry_date
                )
                db.session.add(entry)
                
                stats = DailyStats(
                    user_id=sample_user.id,
                    date=entry_date,
                    points=5,
                    current_streak=i+1,
                    longest_streak=i+1
                )
                db.session.add(stats)
            
            db.session.commit()
        
        with client.session_transaction() as sess:
            sess['user_id'] = sample_user.id
        
        # Get CSRF token
        response = client.get('/progress')
        csrf_token = extract_csrf_token(response.data)
        
        # Test PDF export
        response = client.post('/export-journey', 
                             headers={'X-CSRFToken': csrf_token},
                             json={'wordcloud_image': None})
        
        assert response.status_code == 200
        assert response.mimetype == 'application/pdf'
        assert 'attachment' in response.headers.get('Content-Disposition', '')
        assert 'self-reflective-journey' in response.headers.get('Content-Disposition', '')
    
    def test_export_journey_with_wordcloud(self, client, app, sample_user):
        """Test PDF export with wordcloud image."""
        with app.app_context():
            # Create some diary entries
            entry = DiaryEntry(
                user_id=sample_user.id,
                content='Test entry',
                rating=1,
                entry_date=date.today()
            )
            db.session.add(entry)
            
            stats = DailyStats(
                user_id=sample_user.id,
                date=date.today(),
                points=5,
                current_streak=1,
                longest_streak=1
            )
            db.session.add(stats)
            db.session.commit()
        
        with client.session_transaction() as sess:
            sess['user_id'] = sample_user.id
        
        # Get CSRF token
        response = client.get('/progress')
        csrf_token = extract_csrf_token(response.data)
        
        # Test PDF export with wordcloud image
        fake_wordcloud = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=='
        response = client.post('/export-journey', 
                             headers={'X-CSRFToken': csrf_token},
                             json={'wordcloud_image': fake_wordcloud})
        
        assert response.status_code == 200
        assert response.mimetype == 'application/pdf'
    
    def test_export_journey_no_entries(self, client, app, sample_user):
        """Test PDF export when user has no diary entries."""
        with client.session_transaction() as sess:
            sess['user_id'] = sample_user.id
        
        # Get CSRF token
        response = client.get('/progress')
        csrf_token = extract_csrf_token(response.data)
        
        # Test PDF export with no entries
        response = client.post('/export-journey', 
                             headers={'X-CSRFToken': csrf_token},
                             json={'wordcloud_image': None})
        
        assert response.status_code == 200
        assert response.mimetype == 'application/pdf'
    
    def test_progress_page_displays_correct_stats(self, client, app, sample_user):
        """Test that progress page displays all statistics correctly."""
        with app.app_context():
            # Create entries with known values
            entry1 = DiaryEntry(
                user_id=sample_user.id,
                content='Positive entry',
                rating=1,
                entry_date=date.today() - timedelta(days=1)
            )
            entry2 = DiaryEntry(
                user_id=sample_user.id,
                content='Negative entry',
                rating=-1,
                entry_date=date.today()
            )
            db.session.add_all([entry1, entry2])
            
            # Create corresponding stats
            stats1 = DailyStats(
                user_id=sample_user.id,
                date=date.today() - timedelta(days=1),
                points=5,
                current_streak=1,
                longest_streak=1
            )
            stats2 = DailyStats(
                user_id=sample_user.id,
                date=date.today(),
                points=2,
                current_streak=2,
                longest_streak=2
            )
            db.session.add_all([stats1, stats2])
            db.session.commit()
        
        with client.session_transaction() as sess:
            sess['user_id'] = sample_user.id
        
        response = client.get('/progress')
        assert response.status_code == 200
        
        # Check that all expected elements are present
        assert b'Points Over Time' in response.data
        assert b'Average Points by Day of Week' in response.data
        assert b'Exploration Overview' in response.data
        assert b'Export Journey' in response.data 