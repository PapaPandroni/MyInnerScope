"""
Tests for goal helper utilities
"""

import pytest
from datetime import datetime, date, timezone, timedelta
from app.models import Goal, db
from app.models.goal import GoalCategory, GoalStatus
from app.utils.goal_helpers import (
    get_current_goals,
    get_overdue_goals,
    create_goal,
    get_goal_statistics,
)


class TestGoalHelpers:
    """Test cases for goal helper functions"""

    def test_get_current_goals(self, app, sample_user):
        """Test getting current goals for a user"""
        with app.app_context():
            # Create a current goal
            today = datetime.now(timezone.utc).date()
            goal = Goal(
                user_id=sample_user.id,
                category=GoalCategory.EXERCISE,
                title="Test Goal",
                description="A test goal",
                week_start=today,
                week_end=today + timedelta(days=6),
                status=GoalStatus.ACTIVE,
            )
            db.session.add(goal)
            db.session.commit()

            # Get current goals
            current_goals = get_current_goals(sample_user.id)

            assert len(current_goals) == 1
            assert current_goals[0].title == "Test Goal"

    def test_get_overdue_goals(self, app, sample_user):
        """Test getting overdue goals for a user"""
        with app.app_context():
            # Create an overdue goal
            today = datetime.now(timezone.utc).date()
            overdue_goal = Goal(
                user_id=sample_user.id,
                category=GoalCategory.EXERCISE,
                title="Overdue Goal",
                description="An overdue goal",
                week_start=today - timedelta(days=14),
                week_end=today - timedelta(days=7),
                status=GoalStatus.ACTIVE,
            )
            db.session.add(overdue_goal)
            db.session.commit()

            # Get overdue goals
            overdue_goals = get_overdue_goals(sample_user.id)

            assert len(overdue_goals) == 1
            assert overdue_goals[0].title == "Overdue Goal"

    def test_create_goal(self, app, sample_user):
        """Test creating a new goal"""
        with app.app_context():
            # Create a goal using the helper function
            goal = create_goal(
                user_id=sample_user.id,
                category=GoalCategory.EXERCISE,
                title="New Goal",
                description="A new goal created by helper",
            )

            assert goal.id is not None
            assert goal.title == "New Goal"
            assert goal.category == GoalCategory.EXERCISE
            assert goal.status == GoalStatus.ACTIVE
            assert goal.user_id == sample_user.id

    def test_get_goal_stats(self, app, sample_user):
        """Test getting goal statistics"""
        with app.app_context():
            # Create goals with different statuses
            today = datetime.now(timezone.utc).date()

            # Active goal
            active_goal = Goal(
                user_id=sample_user.id,
                category=GoalCategory.EXERCISE,
                title="Active Goal",
                week_start=today,
                week_end=today + timedelta(days=6),
                status=GoalStatus.ACTIVE,
            )

            # Completed goal
            completed_goal = Goal(
                user_id=sample_user.id,
                category=GoalCategory.LEARNING,
                title="Completed Goal",
                week_start=today - timedelta(days=14),
                week_end=today - timedelta(days=7),
                status=GoalStatus.COMPLETED,
            )

            # Failed goal
            failed_goal = Goal(
                user_id=sample_user.id,
                category=GoalCategory.MINDFULNESS,
                title="Failed Goal",
                week_start=today - timedelta(days=21),
                week_end=today - timedelta(days=14),
                status=GoalStatus.FAILED,
            )

            db.session.add_all([active_goal, completed_goal, failed_goal])
            db.session.commit()

            # Get stats
            stats = get_goal_statistics(sample_user.id)

            assert stats["total_completed"] == 1
            assert stats["success_rate"] == 50.0
            assert stats["has_stats"] is True
            assert (
                stats["category_stats"][GoalCategory.LEARNING.value]["completed"] == 1
            )
            assert (
                stats["category_stats"][GoalCategory.MINDFULNESS.value]["failed"] == 1
            )

    def test_get_goal_stats_empty(self, app, sample_user):
        """Test getting goal stats when user has no goals"""
        with app.app_context():
            stats = get_goal_statistics(sample_user.id)

            assert stats["total_completed"] == 0
            assert stats["success_rate"] == 0
            assert stats["has_stats"] is False
