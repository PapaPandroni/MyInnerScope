"""
Tests for goal helper utilities
"""
import pytest
from datetime import datetime, date, timedelta
from models import Goal, db
from models.goal import GoalCategory, GoalStatus
from utils.goal_helpers import get_current_goals, get_overdue_goals, create_goal, get_goal_stats


class TestGoalHelpers:
    """Test cases for goal helper functions"""
    
    def test_get_current_goals(self, app, sample_user):
        """Test getting current goals for a user"""
        with app.app_context():
            # Create a current goal
            today = date.today()
            goal = Goal(
                user_id=sample_user.id,
                category=GoalCategory.EXERCISE,
                title='Test Goal',
                description='A test goal',
                week_start=today,
                week_end=today + timedelta(days=6),
                status=GoalStatus.ACTIVE
            )
            db.session.add(goal)
            db.session.commit()
            
            # Get current goals
            current_goals = get_current_goals(sample_user.id)
            
            assert len(current_goals) == 1
            assert current_goals[0].title == 'Test Goal'
    
    def test_get_overdue_goals(self, app, sample_user):
        """Test getting overdue goals for a user"""
        with app.app_context():
            # Create an overdue goal
            today = date.today()
            overdue_goal = Goal(
                user_id=sample_user.id,
                category=GoalCategory.EXERCISE,
                title='Overdue Goal',
                description='An overdue goal',
                week_start=today - timedelta(days=14),
                week_end=today - timedelta(days=7),
                status=GoalStatus.ACTIVE
            )
            db.session.add(overdue_goal)
            db.session.commit()
            
            # Get overdue goals
            overdue_goals = get_overdue_goals(sample_user.id)
            
            assert len(overdue_goals) == 1
            assert overdue_goals[0].title == 'Overdue Goal'
    
    def test_create_goal(self, app, sample_user):
        """Test creating a new goal"""
        with app.app_context():
            # Create a goal using the helper function
            goal = create_goal(
                user_id=sample_user.id,
                category=GoalCategory.EXERCISE,
                title='New Goal',
                description='A new goal created by helper'
            )
            
            assert goal.id is not None
            assert goal.title == 'New Goal'
            assert goal.category == GoalCategory.EXERCISE
            assert goal.status == GoalStatus.ACTIVE
            assert goal.user_id == sample_user.id
    
    def test_get_goal_stats(self, app, sample_user):
        """Test getting goal statistics"""
        with app.app_context():
            # Create goals with different statuses
            today = date.today()
            
            # Active goal
            active_goal = Goal(
                user_id=sample_user.id,
                category=GoalCategory.EXERCISE,
                title='Active Goal',
                week_start=today,
                week_end=today + timedelta(days=6),
                status=GoalStatus.ACTIVE
            )
            
            # Completed goal
            completed_goal = Goal(
                user_id=sample_user.id,
                category=GoalCategory.LEARNING,
                title='Completed Goal',
                week_start=today - timedelta(days=14),
                week_end=today - timedelta(days=7),
                status=GoalStatus.COMPLETED
            )
            
            # Failed goal
            failed_goal = Goal(
                user_id=sample_user.id,
                category=GoalCategory.MINDFULNESS,
                title='Failed Goal',
                week_start=today - timedelta(days=21),
                week_end=today - timedelta(days=14),
                status=GoalStatus.FAILED
            )
            
            db.session.add_all([active_goal, completed_goal, failed_goal])
            db.session.commit()
            
            # Get stats
            stats = get_goal_stats(sample_user.id)
            
            assert stats['total_goals'] == 3
            assert stats['completed_goals'] == 1
            assert stats['failed_goals'] == 1
            assert stats['active_goals'] == 1
            assert stats['completion_rate'] == pytest.approx(33.3, rel=0.1)
    
    def test_get_goal_stats_empty(self, app, sample_user):
        """Test getting goal stats when user has no goals"""
        with app.app_context():
            stats = get_goal_stats(sample_user.id)
            
            assert stats['total_goals'] == 0
            assert stats['completed_goals'] == 0
            assert stats['failed_goals'] == 0
            assert stats['active_goals'] == 0
            assert stats['completion_rate'] == 0 