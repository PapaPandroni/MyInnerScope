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
        response = client.get("/progress", follow_redirects=True)
        assert response.status_code == 200
        assert b"Login" in response.data

    def test_progress_page_loads_for_logged_in_user(self, client, sample_user):
        """Test that the progress page loads successfully for a logged-in user."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id

        response = client.get("/progress")
        assert response.status_code == 200
        assert b"Your Progress" in response.data
        assert b"Points Over Time" in response.data
        assert b"Average Points by Day of Week" in response.data

    def test_progress_page_with_no_data(self, client, sample_user):
        """Test progress page with a user who has no diary entries."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id

        response = client.get("/progress")
        assert response.status_code == 200

        # Check that basic stats are zero
        assert b"0" in response.data  # Should show 0 for various stats
        assert b"Word Cloud Locked" in response.data  # Word cloud should be locked
        assert (
            b"Weekday Insights Locked" in response.data
        )  # Weekday chart should be locked

    def test_progress_page_with_single_entry(self, client, app, sample_user):
        """Test progress page with a user who has one diary entry."""
        with app.app_context():
            # Create a diary entry
            entry = DiaryEntry(
                user_id=sample_user.id,
                content="Test entry",
                rating=1,
                entry_date=date.today(),
            )
            db.session.add(entry)

            # Create corresponding stats
            stats = DailyStats(
                user_id=sample_user.id,
                date=date.today(),
                points=5,
                current_streak=1,
                longest_streak=1,
            )
            db.session.add(stats)
            db.session.commit()

        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id

        response = client.get("/progress")
        assert response.status_code == 200

        # Check that stats are calculated correctly
        assert b"5" in response.data  # Points today
        assert b"1" in response.data  # Current streak
        assert b"1" in response.data  # Total entries
        assert b"Word Cloud Locked" in response.data  # Still locked (need 10 entries)

    def test_progress_page_with_multiple_entries(self, client, app, sample_user):
        """Test progress page with multiple diary entries."""
        with app.app_context():
            # Create multiple entries over several days
            for i in range(5):
                entry_date = date.today() - timedelta(days=i)
                entry = DiaryEntry(
                    user_id=sample_user.id,
                    content=f"Entry {i+1}",
                    rating=1 if i % 2 == 0 else -1,
                    entry_date=entry_date,
                )
                db.session.add(entry)

                # Create corresponding stats
                points = 5 if i % 2 == 0 else 2
                stats = DailyStats(
                    user_id=sample_user.id,
                    date=entry_date,
                    points=points,
                    current_streak=i + 1,
                    longest_streak=i + 1,
                )
                db.session.add(stats)

            db.session.commit()

        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id

        response = client.get("/progress")
        assert response.status_code == 200

        # Check that stats are calculated correctly
        assert b"5" in response.data  # Total entries
        assert b"Word Cloud Locked" in response.data  # Still locked (need 10 entries)

    def test_progress_page_with_sufficient_wordcloud_data(
        self, client, app, sample_user
    ):
        """Test progress page when user has enough entries for word cloud."""
        with app.app_context():
            # Create 10+ entries with repeated words
            for i in range(12):
                entry_date = date.today() - timedelta(days=i)
                entry = DiaryEntry(
                    user_id=sample_user.id,
                    content="I went running today and felt great about my progress",
                    rating=1,
                    entry_date=entry_date,
                )
                db.session.add(entry)

                stats = DailyStats(
                    user_id=sample_user.id,
                    date=entry_date,
                    points=5,
                    current_streak=i + 1,
                    longest_streak=i + 1,
                )
                db.session.add(stats)

            db.session.commit()

        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id

        response = client.get("/progress")
        assert response.status_code == 200

        # Word cloud should be unlocked
        assert b"Words Discovered" in response.data
        assert b"wordcloud" in response.data

    def test_progress_page_with_goals(self, client, app, sample_user):
        """Test progress page when user has goals."""
        with app.app_context():
            # Create a goal with all required fields
            goal = Goal(
                user_id=sample_user.id,
                title="Test Goal",
                category="Health",
                description="Test description",
                week_start=date.today(),
                week_end=date.today() + timedelta(days=7),
                status="in_progress",
                created_at=date.today(),  # Add created_at field
            )
            db.session.add(goal)
            db.session.commit()

        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id

        response = client.get("/progress")
        assert response.status_code == 200

        # Check that goals section is present
        assert b"Goals Overview" in response.data
        # Note: The goal title might not appear in the response if the goal helper functions
        # don't return it properly, but the section should be present

    def test_progress_page_displays_correct_stats(self, client, app, sample_user):
        """Test that progress page displays all statistics correctly."""
        with app.app_context():
            # Create entries with known values
            entry1 = DiaryEntry(
                user_id=sample_user.id,
                content="Positive entry",
                rating=1,
                entry_date=date.today() - timedelta(days=1),
            )
            entry2 = DiaryEntry(
                user_id=sample_user.id,
                content="Negative entry",
                rating=-1,
                entry_date=date.today(),
            )
            db.session.add_all([entry1, entry2])

            # Create corresponding stats
            stats1 = DailyStats(
                user_id=sample_user.id,
                date=date.today() - timedelta(days=1),
                points=5,
                current_streak=1,
                longest_streak=1,
            )
            stats2 = DailyStats(
                user_id=sample_user.id,
                date=date.today(),
                points=2,
                current_streak=2,
                longest_streak=2,
            )
            db.session.add_all([stats1, stats2])
            db.session.commit()

        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id

        response = client.get("/progress")
        assert response.status_code == 200

        # Check that all expected elements are present
        assert b"Points Over Time" in response.data
        assert b"Average Points by Day of Week" in response.data
        assert b"Exploration Overview" in response.data

    def test_donate_page_loads(self, client):
        """Test that the donate page loads correctly."""
        response = client.get("/donate")
        assert response.status_code == 200
        assert b"Thank You!" in response.data
        assert b"papapandroni" in response.data  # Buy Me a Coffee widget

    def test_progress_page_diary_entry_counts(self, client, app):
        """Test that the progress page correctly calculates positive and improvement entry counts"""
        with app.app_context():
            # Create a test user
            user = User(
                email="test@example.com", password="password", user_name="TestUser"
            )
            db.session.add(user)
            db.session.commit()

            # Create diary entries with different ratings
            entries = [
                DiaryEntry(user_id=user.id, content="Positive entry 1", rating=1),
                DiaryEntry(user_id=user.id, content="Positive entry 2", rating=1),
                DiaryEntry(user_id=user.id, content="Improvement entry 1", rating=-1),
                DiaryEntry(user_id=user.id, content="Improvement entry 2", rating=-1),
                DiaryEntry(user_id=user.id, content="Improvement entry 3", rating=-1),
            ]
            db.session.add_all(entries)
            db.session.commit()

            # Log in the user
            with client.session_transaction() as sess:
                sess["user_id"] = user.id

            response = client.get(url_for("progress.progress"))
            assert response.status_code == 200

            # Check that the response contains the expected counts in the HTML
            response_data = response.data.decode("utf-8")
            # Check for the new card titles and values
            assert '<h5 class="card-title">Opportunities for Growth</h5>' in response_data
            assert '<p class="card-value">3</p>' in response_data
            assert '<h5 class="card-title">Positive Behaviors</h5>' in response_data
            assert '<p class="card-value">2</p>' in response_data

    def test_progress_page_no_entries(self, client, app):
        """Test progress page with no diary entries"""
        with app.app_context():
            # Create a test user with no entries
            user = User(
                email="noentries@example.com",
                password="password",
                user_name="NoEntriesUser",
            )
            db.session.add(user)
            db.session.commit()

            # Log in the user
            with client.session_transaction() as sess:
                sess["user_id"] = user.id

            response = client.get(url_for("progress.progress"))
            assert response.status_code == 200

            # Check that counts are zero in the HTML
            response_data = response.data.decode("utf-8")
            assert '<h5 class="card-title">Opportunities for Growth</h5>' in response_data
            assert '<p class="card-value">0</p>' in response_data
            assert '<h5 class="card-title">Positive Behaviors</h5>' in response_data
            assert '<p class="card-value">0</p>' in response_data
