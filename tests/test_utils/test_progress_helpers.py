"""
Tests for progress helper functions
"""

import pytest
from datetime import date, timedelta
from app.models import User, DiaryEntry, DailyStats, db
from app.utils.progress_helpers import (
    get_display_name,
    get_today_stats,
    get_total_points,
    get_current_streak,
    get_longest_streak,
    get_total_entries,
    get_points_data,
    get_top_days_with_entries,
    get_weekday_data,
    get_sample_weekday_data,
    get_trend_message,
    get_recent_entries,
    get_unique_weekdays_with_entries,
)


class TestProgressHelpers:
    """Test cases for progress helper functions"""

    def test_get_display_name_with_user_name(self, app):
        """Test get_display_name when user has a user_name."""
        with app.app_context():
            user = User(
                email="test@example.com", password="password123", user_name="Test User"
            )
            db.session.add(user)
            db.session.commit()

            display_name = get_display_name(user)
            assert display_name == "Test User"

    def test_get_display_name_without_user_name(self, app):
        """Test get_display_name when user has no user_name."""
        with app.app_context():
            user = User(email="test@example.com", password="password123")
            db.session.add(user)
            db.session.commit()

            display_name = get_display_name(user)
            assert display_name == "test"

    def test_get_today_stats_with_data(self, app, sample_user):
        """Test get_today_stats when user has stats for today."""
        with app.app_context():
            today = date.today()
            stats = DailyStats(
                user_id=sample_user.id,
                date=today,
                points=15,
                current_streak=3,
                longest_streak=5,
            )
            db.session.add(stats)
            db.session.commit()

            points = get_today_stats(sample_user.id, today)
            assert points == 15

    def test_get_today_stats_without_data(self, app, sample_user):
        """Test get_today_stats when user has no stats for today."""
        with app.app_context():
            today = date.today()
            points = get_today_stats(sample_user.id, today)
            assert points == 0

    def test_get_total_points_with_data(self, app, sample_user):
        """Test get_total_points when user has multiple stats."""
        with app.app_context():
            # Create stats for multiple days
            for i in range(3):
                stats = DailyStats(
                    user_id=sample_user.id,
                    date=date.today() - timedelta(days=i),
                    points=10 + i,
                    current_streak=1,
                    longest_streak=1,
                )
                db.session.add(stats)
            db.session.commit()

            total_points = get_total_points(sample_user.id)
            assert total_points == 33  # 10 + 11 + 12

    def test_get_total_points_without_data(self, app, sample_user):
        """Test get_total_points when user has no stats."""
        with app.app_context():
            total_points = get_total_points(sample_user.id)
            assert total_points == 0

    def test_get_current_streak_with_data(self, app, sample_user):
        """Test get_current_streak when user has diary entries."""
        with app.app_context():
            today = date.today()
            
            # Create diary entries for consecutive days ending today
            for i in range(5):
                entry_date = today - timedelta(days=4-i)  # 5 days ago to today
                entry = DiaryEntry(
                    user_id=sample_user.id,
                    content=f"Day {i+1} entry",
                    rating=1,
                    entry_date=entry_date
                )
                db.session.add(entry)
            db.session.commit()

            current_streak = get_current_streak(sample_user.id)
            assert current_streak == 5

    def test_get_current_streak_without_data(self, app, sample_user):
        """Test get_current_streak when user has no stats."""
        with app.app_context():
            current_streak = get_current_streak(sample_user.id)
            assert current_streak == 0

    def test_get_longest_streak_with_data(self, app, sample_user):
        """Test get_longest_streak when user has stats."""
        with app.app_context():
            # Create multiple stats with different longest streaks
            for i in range(3):
                stats = DailyStats(
                    user_id=sample_user.id,
                    date=date.today() - timedelta(days=i),
                    points=10,
                    current_streak=1,
                    longest_streak=5 + i,
                )
                db.session.add(stats)
            db.session.commit()

            longest_streak = get_longest_streak(sample_user.id)
            assert longest_streak == 7  # Should get the highest value

    def test_get_longest_streak_without_data(self, app, sample_user):
        """Test get_longest_streak when user has no stats."""
        with app.app_context():
            longest_streak = get_longest_streak(sample_user.id)
            assert longest_streak == 0

    def test_get_total_entries_with_data(self, app, sample_user):
        """Test get_total_entries when user has diary entries."""
        with app.app_context():
            # Create multiple diary entries
            for i in range(5):
                entry = DiaryEntry(
                    user_id=sample_user.id,
                    content=f"Entry {i+1}",
                    rating=1,
                    entry_date=date.today() - timedelta(days=i),
                )
                db.session.add(entry)
            db.session.commit()

            total_entries = get_total_entries(sample_user.id)
            assert total_entries == 5

    def test_get_total_entries_without_data(self, app, sample_user):
        """Test get_total_entries when user has no diary entries."""
        with app.app_context():
            total_entries = get_total_entries(sample_user.id)
            assert total_entries == 0

    def test_get_points_data_with_data(self, app, sample_user):
        """Test get_points_data when user has multiple stats."""
        with app.app_context():
            # Create stats for multiple days
            for i in range(3):
                stats = DailyStats(
                    user_id=sample_user.id,
                    date=date.today()
                    - timedelta(days=2 - i),  # Order: 2 days ago, 1 day ago, today
                    points=10,
                    current_streak=1,
                    longest_streak=1,
                )
                db.session.add(stats)
            db.session.commit()

            points_data = get_points_data(sample_user.id)
            assert len(points_data) == 3
            assert points_data[0][1] == 10  # First day: 10 points
            assert points_data[1][1] == 20  # Second day: cumulative 20 points
            assert points_data[2][1] == 30  # Third day: cumulative 30 points

    def test_get_points_data_without_data(self, app, sample_user):
        """Test get_points_data when user has no stats."""
        with app.app_context():
            points_data = get_points_data(sample_user.id)
            assert points_data == []

    def test_get_top_days_with_entries_with_data(self, app, sample_user):
        """Test get_top_days_with_entries when user has data."""
        with app.app_context():
            # Create stats and entries for multiple days
            for i in range(3):
                day_date = date.today() - timedelta(days=i)
                stats = DailyStats(
                    user_id=sample_user.id,
                    date=day_date,
                    points=20 - i * 5,  # 20, 15, 10 points
                    current_streak=1,
                    longest_streak=1,
                )
                db.session.add(stats)

                # Create entries for each day
                for j in range(2):
                    entry = DiaryEntry(
                        user_id=sample_user.id,
                        content=f"Entry {i+1}-{j+1}",
                        rating=1,
                        entry_date=day_date,
                    )
                    db.session.add(entry)
            db.session.commit()

            top_days = get_top_days_with_entries(sample_user.id)
            assert len(top_days) == 3
            assert top_days[0]["points"] == 20  # Highest points first
            assert top_days[1]["points"] == 15
            assert top_days[2]["points"] == 10
            assert len(top_days[0]["entries"]) == 2  # Each day has 2 entries

    def test_get_top_days_with_entries_without_data(self, app, sample_user):
        """Test get_top_days_with_entries when user has no data."""
        with app.app_context():
            top_days = get_top_days_with_entries(sample_user.id)
            assert top_days == []

    def test_get_weekday_data_with_sufficient_data(self, app, sample_user):
        """Test get_weekday_data when user has sufficient data."""
        with app.app_context():
            # Create diary entries on 2+ different weekdays (to unlock chart)
            base_date = date.today()
            monday_date = base_date - timedelta(days=base_date.weekday())
            tuesday_date = monday_date + timedelta(days=1)
            
            # Diary entries on Monday and Tuesday (unlocks chart)
            entry1 = DiaryEntry(
                user_id=sample_user.id,
                content="Monday entry",
                rating=1,
                entry_date=monday_date,
            )
            db.session.add(entry1)
            
            entry2 = DiaryEntry(
                user_id=sample_user.id,
                content="Tuesday entry",
                rating=1,
                entry_date=tuesday_date,
            )
            db.session.add(entry2)
            
            # Create daily stats for all weekdays (chart data)
            for i in range(7):
                stats_date = monday_date + timedelta(days=i)
                stats = DailyStats(
                    user_id=sample_user.id,
                    date=stats_date,
                    points=10,
                    current_streak=1,
                    longest_streak=1,
                )
                db.session.add(stats)
            db.session.commit()

            weekday_data, has_sufficient = get_weekday_data(sample_user.id)
            assert len(weekday_data) == 7
            assert has_sufficient is True  # Should unlock due to diary entries on 2+ weekdays
            # Check that all weekdays are present
            weekday_names = [day["name"] for day in weekday_data]
            expected_names = [
                "Sunday",
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
            ]
            assert weekday_names == expected_names

    def test_get_weekday_data_with_insufficient_data(self, app, sample_user):
        """Test get_weekday_data when user has insufficient data."""
        with app.app_context():
            # Create diary entry on only one weekday (insufficient for unlock)
            entry = DiaryEntry(
                user_id=sample_user.id,
                content="Single entry",
                rating=1,
                entry_date=date.today(),
            )
            db.session.add(entry)
            
            # Create stats for multiple days (but chart won't unlock due to diary entries)
            for i in range(3):
                stats = DailyStats(
                    user_id=sample_user.id,
                    date=date.today() - timedelta(days=i),
                    points=10,
                    current_streak=1,
                    longest_streak=1,
                )
                db.session.add(stats)
            db.session.commit()

            weekday_data, has_sufficient = get_weekday_data(sample_user.id)
            assert len(weekday_data) == 7
            assert has_sufficient is False  # Only 1 unique weekday with diary entries

    def test_get_weekday_data_without_data(self, app, sample_user):
        """Test get_weekday_data when user has no data."""
        with app.app_context():
            weekday_data, has_sufficient = get_weekday_data(sample_user.id)
            assert len(weekday_data) == 7
            assert has_sufficient is False
            # All days should have 0 avg_points
            for day in weekday_data:
                assert day["avg_points"] == 0

    def test_get_sample_weekday_data(self):
        """Test get_sample_weekday_data returns correct structure."""
        sample_data = get_sample_weekday_data()
        assert len(sample_data) == 7

        # Check that all weekdays are present
        weekday_names = [day["name"] for day in sample_data]
        expected_names = [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        ]
        assert weekday_names == expected_names

        # Check that all days have avg_points
        for day in sample_data:
            assert "avg_points" in day
            assert isinstance(day["avg_points"], (int, float))

    def test_get_trend_message_insufficient_data(self, app, sample_user):
        """Test get_trend_message when user has insufficient data."""
        with app.app_context():
            # Create only one entry (less than 13 days of data)
            entry = DiaryEntry(
                user_id=sample_user.id,
                content="Test entry",
                rating=1,
                entry_date=date.today(),
            )
            db.session.add(entry)
            db.session.commit()

            trend_message = get_trend_message(sample_user.id, date.today())
            assert "Keep writing to unlock insights" in trend_message

    def test_get_trend_message_improving_trend(self, app, sample_user):
        """Test get_trend_message when user is improving."""
        with app.app_context():
            # Create entries and stats for 14 days
            for i in range(14):
                day_date = date.today() - timedelta(days=13 - i)
                entry = DiaryEntry(
                    user_id=sample_user.id,
                    content=f"Entry {i+1}",
                    rating=1,
                    entry_date=day_date,
                )
                db.session.add(entry)

                # Higher points in last 7 days (improving trend)
                points = 15 if i >= 7 else 5
                stats = DailyStats(
                    user_id=sample_user.id,
                    date=day_date,
                    points=points,
                    current_streak=1,
                    longest_streak=1,
                )
                db.session.add(stats)
            db.session.commit()

            trend_message = get_trend_message(sample_user.id, date.today())
            assert "earning more points than last week" in trend_message

    def test_get_trend_message_declining_trend(self, app, sample_user):
        """Test get_trend_message when user is declining."""
        with app.app_context():
            # Create entries and stats for 14 days
            for i in range(14):
                day_date = date.today() - timedelta(days=13 - i)
                entry = DiaryEntry(
                    user_id=sample_user.id,
                    content=f"Entry {i+1}",
                    rating=1,
                    entry_date=day_date,
                )
                db.session.add(entry)

                # Lower points in last 7 days (declining trend)
                points = 5 if i >= 7 else 15
                stats = DailyStats(
                    user_id=sample_user.id,
                    date=day_date,
                    points=points,
                    current_streak=1,
                    longest_streak=1,
                )
                db.session.add(stats)
            db.session.commit()

            trend_message = get_trend_message(sample_user.id, date.today())
            assert "Let's beat last week" in trend_message

    def test_get_trend_message_steady_trend(self, app, sample_user):
        """Test get_trend_message when user has steady progress."""
        with app.app_context():
            # Create entries and stats for 14 days
            for i in range(14):
                day_date = date.today() - timedelta(days=13 - i)
                entry = DiaryEntry(
                    user_id=sample_user.id,
                    content=f"Entry {i+1}",
                    rating=1,
                    entry_date=day_date,
                )
                db.session.add(entry)

                # Similar points in both weeks (steady trend)
                points = 10
                stats = DailyStats(
                    user_id=sample_user.id,
                    date=day_date,
                    points=points,
                    current_streak=1,
                    longest_streak=1,
                )
                db.session.add(stats)
            db.session.commit()

            trend_message = get_trend_message(sample_user.id, date.today())
            assert "Steady progress" in trend_message

    def test_get_recent_entries_with_data(self, app, sample_user):
        """Test get_recent_entries when user has entries."""
        with app.app_context():
            # Create multiple entries
            for i in range(5):
                entry = DiaryEntry(
                    user_id=sample_user.id,
                    content=f"Entry {i+1}",
                    rating=1,
                    entry_date=date.today() - timedelta(days=i),
                )
                db.session.add(entry)
            db.session.commit()

            recent_entries = get_recent_entries(sample_user.id, limit=3)
            assert len(recent_entries) == 3
            # Should be ordered by ID desc (most recent first)
            assert recent_entries[0].content == "Entry 5"
            assert recent_entries[1].content == "Entry 4"
            assert recent_entries[2].content == "Entry 3"

    def test_get_recent_entries_without_data(self, app, sample_user):
        """Test get_recent_entries when user has no entries."""
        with app.app_context():
            recent_entries = get_recent_entries(sample_user.id)
            assert recent_entries == []

    def test_get_recent_entries_default_limit(self, app, sample_user):
        """Test get_recent_entries uses default limit of 3."""
        with app.app_context():
            # Create 5 entries
            for i in range(5):
                entry = DiaryEntry(
                    user_id=sample_user.id,
                    content=f"Entry {i+1}",
                    rating=1,
                    entry_date=date.today(),
                )
                db.session.add(entry)
            db.session.commit()

            recent_entries = get_recent_entries(sample_user.id)  # No limit specified
            assert len(recent_entries) == 3  # Default limit

    def test_get_unique_weekdays_with_entries_with_data(self, app, sample_user):
        """Test get_unique_weekdays_with_entries when user has entries on multiple weekdays."""
        with app.app_context():
            # Create entries on different weekdays
            base_date = date.today()
            
            # Monday (weekday 0)
            monday_date = base_date - timedelta(days=base_date.weekday())
            entry1 = DiaryEntry(
                user_id=sample_user.id,
                content="Monday entry",
                rating=1,
                entry_date=monday_date,
            )
            db.session.add(entry1)
            
            # Tuesday (weekday 1)
            tuesday_date = monday_date + timedelta(days=1)
            entry2 = DiaryEntry(
                user_id=sample_user.id,
                content="Tuesday entry",
                rating=1,
                entry_date=tuesday_date,
            )
            db.session.add(entry2)
            
            # Friday (weekday 4)
            friday_date = monday_date + timedelta(days=4)
            entry3 = DiaryEntry(
                user_id=sample_user.id,
                content="Friday entry",
                rating=1,
                entry_date=friday_date,
            )
            db.session.add(entry3)
            
            # Another Monday entry (same weekday as first)
            another_monday = monday_date + timedelta(days=7)
            entry4 = DiaryEntry(
                user_id=sample_user.id,
                content="Another Monday entry",
                rating=1,
                entry_date=another_monday,
            )
            db.session.add(entry4)
            
            db.session.commit()

            unique_weekdays = get_unique_weekdays_with_entries(sample_user.id)
            assert unique_weekdays == 3  # Monday, Tuesday, Friday (Monday counted only once)

    def test_get_unique_weekdays_with_entries_without_data(self, app, sample_user):
        """Test get_unique_weekdays_with_entries when user has no entries."""
        with app.app_context():
            unique_weekdays = get_unique_weekdays_with_entries(sample_user.id)
            assert unique_weekdays == 0

    def test_get_unique_weekdays_with_entries_single_day(self, app, sample_user):
        """Test get_unique_weekdays_with_entries when user has entries on only one weekday."""
        with app.app_context():
            # Create multiple entries on the same weekday
            today = date.today()
            
            entry1 = DiaryEntry(
                user_id=sample_user.id,
                content="First entry today",
                rating=1,
                entry_date=today,
            )
            db.session.add(entry1)
            
            entry2 = DiaryEntry(
                user_id=sample_user.id,
                content="Second entry today",
                rating=1,
                entry_date=today,
            )
            db.session.add(entry2)
            
            db.session.commit()

            unique_weekdays = get_unique_weekdays_with_entries(sample_user.id)
            assert unique_weekdays == 1  # Only one unique weekday

    def test_get_unique_weekdays_with_entries_all_weekdays(self, app, sample_user):
        """Test get_unique_weekdays_with_entries when user has entries on all weekdays."""
        with app.app_context():
            # Create entries for all 7 weekdays
            base_date = date.today()
            monday_date = base_date - timedelta(days=base_date.weekday())
            
            for i in range(7):
                entry_date = monday_date + timedelta(days=i)
                entry = DiaryEntry(
                    user_id=sample_user.id,
                    content=f"Entry for day {i}",
                    rating=1,
                    entry_date=entry_date,
                )
                db.session.add(entry)
            
            db.session.commit()

            unique_weekdays = get_unique_weekdays_with_entries(sample_user.id)
            assert unique_weekdays == 7  # All 7 weekdays

    def test_get_weekday_data_points_vs_diary_logic(self, app, sample_user):
        """Test that chart unlocks based on diary entries, not daily stats."""
        with app.app_context():
            # User has only one diary entry
            entry = DiaryEntry(
                user_id=sample_user.id,
                content="Only diary entry",
                rating=1,
                entry_date=date.today(),
            )
            db.session.add(entry)
            
            # But user has daily stats on multiple weekdays (e.g., from login bonuses)
            base_date = date.today()
            monday_date = base_date - timedelta(days=base_date.weekday())
            
            for i in range(3):  # Monday, Tuesday, Wednesday
                stats = DailyStats(
                    user_id=sample_user.id,
                    date=monday_date + timedelta(days=i),
                    points=5,  # Points from login bonus or other activities
                    current_streak=1,
                    longest_streak=1,
                )
                db.session.add(stats)
            
            db.session.commit()

            weekday_data, has_sufficient = get_weekday_data(sample_user.id)
            assert len(weekday_data) == 7
            # Chart should NOT unlock despite having points on multiple weekdays
            # because user only has diary entries on 1 weekday
            assert has_sufficient is False
            
            # But the chart data should still show points for those days
            monday_data = next(d for d in weekday_data if d["name"] == "Monday")
            tuesday_data = next(d for d in weekday_data if d["name"] == "Tuesday") 
            wednesday_data = next(d for d in weekday_data if d["name"] == "Wednesday")
            assert monday_data["avg_points"] == 5.0
            assert tuesday_data["avg_points"] == 5.0  
            assert wednesday_data["avg_points"] == 5.0
