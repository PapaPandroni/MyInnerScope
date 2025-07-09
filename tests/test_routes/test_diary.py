import pytest
from flask import url_for, session
from datetime import date, timedelta
from app.models import User, DiaryEntry, DailyStats, db
from tests.conftest import extract_csrf_token


class TestDiaryRoutes:
    """Test cases for diary entry routes."""

    def test_diary_entry_page_requires_login(self, client):
        """Test that accessing the diary page redirects to login if not authenticated."""
        response = client.get("/diary", follow_redirects=True)
        assert response.status_code == 200
        assert b"Login" in response.data
        assert url_for("auth.login_page") in response.request.path

    def test_diary_entry_page_loads_for_logged_in_user(self, client, sample_user):
        """Test that the diary page loads successfully for a logged-in user."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        response = client.get("/diary")
        assert response.status_code == 200
        assert b"Daily Reflection" in response.data
        assert b"Describe one specific moment from today" in response.data

    def test_create_diary_entry_success_positive_rating(self, client, app, sample_user):
        """Test successful creation of a diary entry with a positive rating."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id

        # Get CSRF token from the diary page
        response = client.get("/diary")
        csrf_token = extract_csrf_token(response.data)

        data = {
            "content": "Today I helped a friend with their project.",
            "rating": "1",
            "csrf_token": csrf_token,
        }
        response = client.post("/diary", data=data, follow_redirects=True)
        assert response.status_code == 200
        assert (
            b"Today I helped a friend with their project." in response.data
        )  # Should show in recent entries

        with app.app_context():
            entry = DiaryEntry.query.filter_by(
                user_id=sample_user.id,
                content="Today I helped a friend with their project.",
            ).first()
            assert entry is not None
            assert entry.rating == 1
            assert entry.entry_date == date.today()

            stats = DailyStats.query.filter_by(
                user_id=sample_user.id, date=date.today()
            ).first()
            assert stats is not None
            assert stats.points == 5  # 5 points for positive rating

    def test_create_diary_entry_success_negative_rating(self, client, app, sample_user):
        """Test successful creation of a diary entry with a negative rating."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id

        response = client.get("/diary")
        csrf_token = extract_csrf_token(response.data)

        data = {
            "content": "I procrastinated on an important task today.",
            "rating": "-1",
            "csrf_token": csrf_token,
        }
        response = client.post("/diary", data=data, follow_redirects=True)
        assert response.status_code == 200
        assert b"I procrastinated on an important task today." in response.data

        with app.app_context():
            entry = DiaryEntry.query.filter_by(
                user_id=sample_user.id,
                content="I procrastinated on an important task today.",
            ).first()
            assert entry is not None
            assert entry.rating == -1

            stats = DailyStats.query.filter_by(
                user_id=sample_user.id, date=date.today()
            ).first()
            assert stats is not None
            assert stats.points == 2  # 2 points for negative rating

    def test_create_diary_entry_invalid_content_empty(self, client, app, sample_user):
        """Test that an empty diary entry is rejected."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id

        response = client.get("/diary")
        csrf_token = extract_csrf_token(response.data)

        data = {"content": "", "rating": "1", "csrf_token": csrf_token}
        response = client.post("/diary", data=data, follow_redirects=True)
        assert response.status_code == 400  # Bad request due to validation error
        assert b"Diary entry content is required" in response.data

        with app.app_context():
            entry = DiaryEntry.query.filter_by(
                user_id=sample_user.id, content=""
            ).first()
            assert entry is None  # No entry should be created

    def test_create_diary_entry_invalid_content_too_long(
        self, client, app, sample_user
    ):
        """Test that a diary entry with content exceeding 2000 characters is rejected."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id

        response = client.get("/diary")
        csrf_token = extract_csrf_token(response.data)

        long_content = "a" * 2001  # 2001 characters
        data = {"content": long_content, "rating": "1", "csrf_token": csrf_token}
        response = client.post("/diary", data=data, follow_redirects=True)
        assert response.status_code == 400
        assert b"Diary entry must be between 1 and 2000 characters" in response.data

        with app.app_context():
            entry = DiaryEntry.query.filter_by(
                user_id=sample_user.id, content=long_content
            ).first()
            assert entry is None

    def test_create_diary_entry_invalid_rating(self, client, app, sample_user):
        """Test that a diary entry with an invalid rating is rejected."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id

        response = client.get("/diary")
        csrf_token = extract_csrf_token(response.data)

        data = {
            "content": "Some content.",
            "rating": "0",  # Invalid rating
            "csrf_token": csrf_token,
        }
        response = client.post("/diary", data=data)
        assert response.status_code == 400
        assert b"alert alert-danger" in response.data
        assert (
            b"Rating must be either -1 (want to change) or 1 (encouraged)"
            in response.data
        )

        with app.app_context():
            entry = DiaryEntry.query.filter_by(
                user_id=sample_user.id, content="Some content."
            ).first()
            assert entry is None

    def test_diary_entry_updates_streak_new_day(self, client, app, sample_user):
        """Test that creating entries on consecutive days updates the streak."""
        with app.app_context():
            # Day 1 entry
            entry1 = DiaryEntry(
                user_id=sample_user.id,
                content="Day 1",
                rating=1,
                entry_date=date.today() - timedelta(days=1),
            )
            db.session.add(entry1)
            db.session.commit()

            stats1 = DailyStats(
                user_id=sample_user.id,
                date=date.today() - timedelta(days=1),
                points=5,
                current_streak=1,
                longest_streak=1,
            )
            db.session.add(stats1)
            db.session.commit()

        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id

        response = client.get("/diary")
        csrf_token = extract_csrf_token(response.data)

        # Day 2 entry (today)
        data = {"content": "Day 2", "rating": "1", "csrf_token": csrf_token}
        client.post("/diary", data=data, follow_redirects=True)

        with app.app_context():
            stats2 = DailyStats.query.filter_by(
                user_id=sample_user.id, date=date.today()
            ).first()
            assert stats2 is not None
            assert stats2.current_streak == 2
            assert stats2.longest_streak == 2

    def test_diary_entry_resets_streak_gap_day(self, client, app, sample_user):
        """Test that a gap in entries resets the streak."""
        with app.app_context():
            # Day 1 entry
            entry1 = DiaryEntry(
                user_id=sample_user.id,
                content="Day 1",
                rating=1,
                entry_date=date.today() - timedelta(days=2),
            )
            db.session.add(entry1)
            db.session.commit()

            stats1 = DailyStats(
                user_id=sample_user.id,
                date=date.today() - timedelta(days=2),
                points=5,
                current_streak=1,
                longest_streak=1,
            )
            db.session.add(stats1)
            db.session.commit()

        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id

        response = client.get("/diary")
        csrf_token = extract_csrf_token(response.data)

        # Day 3 entry (today, after a 1-day gap)
        data = {"content": "Day 3", "rating": "1", "csrf_token": csrf_token}
        client.post("/diary", data=data, follow_redirects=True)

        with app.app_context():
            stats2 = DailyStats.query.filter_by(
                user_id=sample_user.id, date=date.today()
            ).first()
            assert stats2 is not None
            assert stats2.current_streak == 1  # Streak should reset to 1
            assert (
                stats2.longest_streak == 1
            )  # Longest streak remains 1 from previous entry
