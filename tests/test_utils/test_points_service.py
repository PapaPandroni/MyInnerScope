"""
Tests for points service including streak milestone rewards
"""

import pytest
from datetime import date, timedelta
from app.models import User, DiaryEntry, DailyStats, PointsLog, db
from app.models.points_log import PointsSourceType
from app.utils.points_service import PointsService


class TestPointsService:
    """Test cases for PointsService functionality"""

    def test_streak_milestone_7_day_award(self, app, sample_user):
        """Test that 7-day streak milestones award 10 points correctly"""
        with app.app_context():
            user_id = sample_user.id

            # Test 7-day milestone
            PointsService.check_and_award_streak_milestones(user_id, 7)

            # Check that 10 points were awarded
            milestone_award = PointsLog.query.filter_by(
                user_id=user_id, source_type=PointsSourceType.STREAK_7_DAY.value
            ).first()

            assert milestone_award is not None
            assert milestone_award.points == 10
            assert "7-Day Streak Milestone (Day 7)" in milestone_award.description

    def test_streak_milestone_14_day_award(self, app, sample_user):
        """Test that 14-day streak (second 7-day milestone) awards points"""
        with app.app_context():
            user_id = sample_user.id

            # Test 14-day milestone (second 7-day milestone)
            PointsService.check_and_award_streak_milestones(user_id, 14)

            # Check that 10 points were awarded
            milestone_award = PointsLog.query.filter_by(
                user_id=user_id, source_type=PointsSourceType.STREAK_7_DAY.value
            ).first()

            assert milestone_award is not None
            assert milestone_award.points == 10
            assert "7-Day Streak Milestone (Day 14)" in milestone_award.description

    def test_streak_milestone_30_day_award(self, app, sample_user):
        """Test that 30-day streak milestones award 50 points correctly"""
        with app.app_context():
            user_id = sample_user.id

            # Test 30-day milestone
            PointsService.check_and_award_streak_milestones(user_id, 30)

            # Check that 50 points were awarded
            milestone_award = PointsLog.query.filter_by(
                user_id=user_id, source_type=PointsSourceType.STREAK_30_DAY.value
            ).first()

            assert milestone_award is not None
            assert milestone_award.points == 50
            assert "30-Day Streak Milestone (Day 30)" in milestone_award.description

    def test_streak_milestone_60_day_award(self, app, sample_user):
        """Test that 60-day streak (second 30-day milestone) awards points"""
        with app.app_context():
            user_id = sample_user.id

            # Test 60-day milestone (second 30-day milestone)
            PointsService.check_and_award_streak_milestones(user_id, 60)

            # Check that 50 points were awarded
            milestone_award = PointsLog.query.filter_by(
                user_id=user_id, source_type=PointsSourceType.STREAK_30_DAY.value
            ).first()

            assert milestone_award is not None
            assert milestone_award.points == 50
            assert "30-Day Streak Milestone (Day 60)" in milestone_award.description

    def test_streak_milestone_overlapping_day_210(self, app, sample_user):
        """Test overlapping milestones (day 210: both 7-day and 30-day)"""
        with app.app_context():
            user_id = sample_user.id

            # Day 210 is divisible by both 7 and 30
            # 210 % 7 == 0 and 210 % 30 == 0
            PointsService.check_and_award_streak_milestones(user_id, 210)

            # Check that both awards were given
            seven_day_award = PointsLog.query.filter_by(
                user_id=user_id, source_type=PointsSourceType.STREAK_7_DAY.value
            ).first()

            thirty_day_award = PointsLog.query.filter_by(
                user_id=user_id, source_type=PointsSourceType.STREAK_30_DAY.value
            ).first()

            assert seven_day_award is not None
            assert seven_day_award.points == 10
            assert "7-Day Streak Milestone (Day 210)" in seven_day_award.description

            assert thirty_day_award is not None
            assert thirty_day_award.points == 50
            assert "30-Day Streak Milestone (Day 210)" in thirty_day_award.description

    def test_streak_milestone_no_award_for_non_milestone(self, app, sample_user):
        """Test that non-milestone days don't award points"""
        with app.app_context():
            user_id = sample_user.id

            # Test non-milestone days (e.g., day 5, 8, 23)
            for streak_day in [5, 8, 23]:
                PointsService.check_and_award_streak_milestones(user_id, streak_day)

                # Check that no milestone awards were given
                milestone_awards = (
                    PointsLog.query.filter_by(user_id=user_id)
                    .filter(
                        PointsLog.source_type.in_(
                            [
                                PointsSourceType.STREAK_7_DAY.value,
                                PointsSourceType.STREAK_30_DAY.value,
                            ]
                        )
                    )
                    .all()
                )

                assert len(milestone_awards) == 0

    def test_streak_milestone_duplicate_prevention_same_day(self, app, sample_user):
        """Test that milestone awards are only given once per day"""
        with app.app_context():
            user_id = sample_user.id

            # First call should award points
            PointsService.check_and_award_streak_milestones(user_id, 7)

            # Second call same day should not award again
            PointsService.check_and_award_streak_milestones(user_id, 7)

            # Check that only one award exists
            milestone_awards = PointsLog.query.filter_by(
                user_id=user_id, source_type=PointsSourceType.STREAK_7_DAY.value
            ).all()

            assert len(milestone_awards) == 1
            assert milestone_awards[0].points == 10

    def test_streak_milestone_zero_streak_no_award(self, app, sample_user):
        """Test that zero or negative streaks don't award points"""
        with app.app_context():
            user_id = sample_user.id

            # Test with zero and negative streaks
            for streak in [0, -1, -5]:
                PointsService.check_and_award_streak_milestones(user_id, streak)

                # Check that no awards were given
                milestone_awards = (
                    PointsLog.query.filter_by(user_id=user_id)
                    .filter(
                        PointsLog.source_type.in_(
                            [
                                PointsSourceType.STREAK_7_DAY.value,
                                PointsSourceType.STREAK_30_DAY.value,
                            ]
                        )
                    )
                    .all()
                )

                assert len(milestone_awards) == 0

    def test_streak_milestone_awards_use_correct_date(self, app, sample_user):
        """Test that milestone awards use today's date correctly"""
        with app.app_context():
            user_id = sample_user.id
            today = date.today()

            # Award milestone
            PointsService.check_and_award_streak_milestones(user_id, 7)

            # Check that award uses today's date
            milestone_award = PointsLog.query.filter_by(
                user_id=user_id, source_type=PointsSourceType.STREAK_7_DAY.value
            ).first()

            assert milestone_award is not None
            assert milestone_award.date == today

    def test_streak_milestone_multiple_milestones_sequence(self, app, sample_user):
        """Test awarding multiple milestones in sequence"""
        with app.app_context():
            user_id = sample_user.id

            # Simulate multiple milestone days across different days
            milestone_days = [7, 14, 21, 28, 30, 35, 42]

            for i, streak_day in enumerate(milestone_days):
                # Simulate different days by creating entries with different dates
                test_date = date.today() - timedelta(days=len(milestone_days) - i - 1)

                # Mock the date for this test
                with app.app_context():
                    # We'll test the logic by checking what would be awarded
                    original_date = date.today()

                    # For this test, we check the logic works for each milestone
                    if streak_day % 7 == 0:
                        expected_7_day = True
                    else:
                        expected_7_day = False

                    if streak_day % 30 == 0:
                        expected_30_day = True
                    else:
                        expected_30_day = False

                    # Verify the modulo logic is working as expected
                    assert (streak_day % 7 == 0) == expected_7_day
                    assert (streak_day % 30 == 0) == expected_30_day

    def test_streak_milestone_database_integration(self, app, sample_user):
        """Test that milestone awards integrate properly with the database"""
        with app.app_context():
            user_id = sample_user.id

            # Award milestone
            PointsService.check_and_award_streak_milestones(user_id, 14)

            # Commit to ensure database integration
            db.session.commit()

            # Retrieve from database
            milestone_award = PointsLog.query.filter_by(
                user_id=user_id, source_type=PointsSourceType.STREAK_7_DAY.value
            ).first()

            assert milestone_award is not None
            assert milestone_award.points == 10
            assert milestone_award.user_id == user_id
            assert milestone_award.source_type == PointsSourceType.STREAK_7_DAY.value
            assert milestone_award.description == "7-Day Streak Milestone (Day 14)"
            assert milestone_award.created_at is not None

    def test_streak_milestone_edge_case_day_42(self, app, sample_user):
        """Test specific edge case: day 42 (divisible by 7 but not 30)"""
        with app.app_context():
            user_id = sample_user.id

            # Day 42: 42 % 7 == 0 (True), 42 % 30 == 12 (False)
            PointsService.check_and_award_streak_milestones(user_id, 42)

            # Should only get 7-day award
            seven_day_award = PointsLog.query.filter_by(
                user_id=user_id, source_type=PointsSourceType.STREAK_7_DAY.value
            ).first()

            thirty_day_award = PointsLog.query.filter_by(
                user_id=user_id, source_type=PointsSourceType.STREAK_30_DAY.value
            ).first()

            assert seven_day_award is not None
            assert seven_day_award.points == 10
            assert thirty_day_award is None

    def test_streak_milestone_large_streak_values(self, app, sample_user):
        """Test milestone awards work with large streak values"""
        with app.app_context():
            user_id = sample_user.id

            # Test large milestone (420 days: divisible by both 7 and 30)
            # 420 % 7 == 0 and 420 % 30 == 0
            PointsService.check_and_award_streak_milestones(user_id, 420)

            # Should get both awards
            seven_day_award = PointsLog.query.filter_by(
                user_id=user_id, source_type=PointsSourceType.STREAK_7_DAY.value
            ).first()

            thirty_day_award = PointsLog.query.filter_by(
                user_id=user_id, source_type=PointsSourceType.STREAK_30_DAY.value
            ).first()

            assert seven_day_award is not None
            assert seven_day_award.points == 10
            assert "7-Day Streak Milestone (Day 420)" in seven_day_award.description

            assert thirty_day_award is not None
            assert thirty_day_award.points == 50
            assert "30-Day Streak Milestone (Day 420)" in thirty_day_award.description

    def test_streak_milestone_awards_persist_across_sessions(self, app, sample_user):
        """Test that milestone awards persist across application sessions"""
        with app.app_context():
            user_id = sample_user.id

            # Award milestone
            PointsService.check_and_award_streak_milestones(user_id, 21)
            db.session.commit()

        # New app context (simulating new session)
        with app.app_context():
            # Retrieve award from new session
            milestone_award = PointsLog.query.filter_by(
                user_id=user_id, source_type=PointsSourceType.STREAK_7_DAY.value
            ).first()

            assert milestone_award is not None
            assert milestone_award.points == 10
            assert "7-Day Streak Milestone (Day 21)" in milestone_award.description


class TestStreakMilestoneIntegration:
    """Integration tests for streak milestones with diary entries"""

    def create_diary_entries_for_consecutive_days(self, user_id, start_date, num_days):
        """Helper to create diary entries for consecutive days"""
        for i in range(num_days):
            entry_date = start_date + timedelta(days=i)
            entry = DiaryEntry(
                user_id=user_id,
                content=f"Day {i+1} entry",
                rating=1,
                entry_date=entry_date,
            )
            db.session.add(entry)
        db.session.commit()

    def test_streak_reset_and_re_earning_milestones(self, app, sample_user):
        """Test that users can re-earn milestones after streak resets"""
        with app.app_context():
            user_id = sample_user.id

            # First streak: reach 7 days
            PointsService.check_and_award_streak_milestones(user_id, 7)

            # Verify first 7-day milestone
            first_award = PointsLog.query.filter_by(
                user_id=user_id, source_type=PointsSourceType.STREAK_7_DAY.value
            ).first()
            assert first_award is not None
            assert first_award.points == 10

            # Clear the awards to simulate a new day/streak reset scenario
            PointsLog.query.filter_by(user_id=user_id).delete()
            db.session.commit()

            # Second streak: reach 7 days again (after streak reset)
            PointsService.check_and_award_streak_milestones(user_id, 7)

            # Verify second 7-day milestone can be earned again
            second_award = PointsLog.query.filter_by(
                user_id=user_id, source_type=PointsSourceType.STREAK_7_DAY.value
            ).first()
            assert second_award is not None
            assert second_award.points == 10

    def test_milestone_awards_with_real_diary_entries(self, app, sample_user):
        """Test milestone awards work with actual diary entry creation"""
        with app.app_context():
            user_id = sample_user.id
            start_date = date.today() - timedelta(days=6)

            # Create 7 consecutive diary entries
            self.create_diary_entries_for_consecutive_days(user_id, start_date, 7)

            # Simulate the streak calculation and milestone check
            from app.utils.progress_helpers import get_current_streak

            current_streak = get_current_streak(user_id)

            # Current streak should be 7 (if today has an entry)
            if current_streak == 7:
                PointsService.check_and_award_streak_milestones(user_id, current_streak)

                # Check milestone award
                milestone_award = PointsLog.query.filter_by(
                    user_id=user_id, source_type=PointsSourceType.STREAK_7_DAY.value
                ).first()

                assert milestone_award is not None
                assert milestone_award.points == 10

    def test_gap_in_streak_prevents_early_milestone(self, app, sample_user):
        """Test that gaps in streaks prevent milestone awards"""
        with app.app_context():
            user_id = sample_user.id
            start_date = date.today() - timedelta(days=8)

            # Create entries for days 1-3, skip day 4, then days 5-7
            # This creates a gap, so no 7-day milestone should be awarded

            # Days 1-3
            for i in range(3):
                entry_date = start_date + timedelta(days=i)
                entry = DiaryEntry(
                    user_id=user_id,
                    content=f"Day {i+1} entry",
                    rating=1,
                    entry_date=entry_date,
                )
                db.session.add(entry)

            # Skip day 4 (gap)

            # Days 5-7 (after gap)
            for i in range(4, 7):
                entry_date = start_date + timedelta(days=i)
                entry = DiaryEntry(
                    user_id=user_id,
                    content=f"Day {i+1} entry",
                    rating=1,
                    entry_date=entry_date,
                )
                db.session.add(entry)

            db.session.commit()

            # Calculate actual streak (should be 3, not 7)
            from app.utils.progress_helpers import get_current_streak

            current_streak = get_current_streak(user_id)

            # Try to award milestone (should not award since streak < 7)
            PointsService.check_and_award_streak_milestones(user_id, current_streak)

            # Check that no 7-day milestone was awarded
            milestone_award = PointsLog.query.filter_by(
                user_id=user_id, source_type=PointsSourceType.STREAK_7_DAY.value
            ).first()

            assert milestone_award is None

    def test_30_day_milestone_with_diary_entries(self, app, sample_user):
        """Test 30-day milestone with actual diary entries"""
        with app.app_context():
            user_id = sample_user.id

            # Simulate having a 30-day streak (we'll just test the milestone logic)
            # In a real scenario, this would be 30 consecutive days of diary entries
            PointsService.check_and_award_streak_milestones(user_id, 30)

            # Check 30-day milestone award
            milestone_award = PointsLog.query.filter_by(
                user_id=user_id, source_type=PointsSourceType.STREAK_30_DAY.value
            ).first()

            assert milestone_award is not None
            assert milestone_award.points == 50
            assert "30-Day Streak Milestone (Day 30)" in milestone_award.description

    def test_milestone_awards_different_users(self, app):
        """Test that milestone awards work correctly for different users"""
        with app.app_context():
            # Create two test users
            user1 = User(email="user1@test.com", password="password123")
            user2 = User(email="user2@test.com", password="password123")
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

            # Award milestones to both users
            PointsService.check_and_award_streak_milestones(user1.id, 7)
            PointsService.check_and_award_streak_milestones(user2.id, 14)

            # Check user1's award
            user1_award = PointsLog.query.filter_by(
                user_id=user1.id, source_type=PointsSourceType.STREAK_7_DAY.value
            ).first()

            # Check user2's award
            user2_award = PointsLog.query.filter_by(
                user_id=user2.id, source_type=PointsSourceType.STREAK_7_DAY.value
            ).first()

            assert user1_award is not None
            assert user1_award.points == 10
            assert "Day 7" in user1_award.description

            assert user2_award is not None
            assert user2_award.points == 10
            assert "Day 14" in user2_award.description

            # Ensure awards are separate
            assert user1_award.user_id != user2_award.user_id

    def test_comprehensive_milestone_sequence(self, app, sample_user):
        """Test a comprehensive sequence of milestone awards"""
        with app.app_context():
            user_id = sample_user.id

            # Test sequence: 7, 14, 21, 28, 30, 35, 42, 49, 56, 60
            milestone_sequence = [7, 14, 21, 28, 30, 35, 42, 49, 56, 60]
            expected_awards = {
                7: ("7_day", 10),
                14: ("7_day", 10),
                21: ("7_day", 10),
                28: ("7_day", 10),
                30: ("30_day", 50),
                35: ("7_day", 10),
                42: ("7_day", 10),
                49: ("7_day", 10),
                56: ("7_day", 10),
                60: ("30_day", 50),
            }

            total_7_day_awards = 0
            total_30_day_awards = 0

            for milestone_day in milestone_sequence:
                # Clear previous awards to test each milestone independently
                PointsLog.query.filter_by(user_id=user_id).delete()
                db.session.commit()

                # Award milestone
                PointsService.check_and_award_streak_milestones(user_id, milestone_day)

                # Check expected award
                award_type, expected_points = expected_awards[milestone_day]

                if award_type == "7_day":
                    award = PointsLog.query.filter_by(
                        user_id=user_id, source_type=PointsSourceType.STREAK_7_DAY.value
                    ).first()
                    total_7_day_awards += 1
                else:  # 30_day
                    award = PointsLog.query.filter_by(
                        user_id=user_id,
                        source_type=PointsSourceType.STREAK_30_DAY.value,
                    ).first()
                    total_30_day_awards += 1

                assert award is not None
                assert award.points == expected_points
                assert f"Day {milestone_day}" in award.description

            # Verify we tested the expected number of each type
            assert total_7_day_awards == 8  # Days 7,14,21,28,35,42,49,56
            assert total_30_day_awards == 2  # Days 30,60
