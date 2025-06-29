"""
Tests for goal helper functions
"""
import pytest
from datetime import datetime, timedelta
from utils.goal_helpers import *


class TestGoalHelpers:
    """Test cases for goal helper functions"""
    
    def test_get_goal_dates(self):
        """Test getting start and end dates for a new goal"""
        start_date = datetime.now().date()
        start, end = Goal.get_goal_dates(start_date)
        
        assert start == start_date
        assert end == start_date + timedelta(days=6)
        assert (end - start).days == 6
    
    def test_goal_is_current_property(self, sample_goal):
        """Test the is_current property of goals"""
        # Goal should be current since it was created today
        assert sample_goal.is_current == True
        
        # Test with a past goal
        sample_goal.week_start = datetime.now().date() - timedelta(days=10)
        sample_goal.week_end = datetime.now().date() - timedelta(days=4)
        assert sample_goal.is_current == False
        
        # Test with a future goal
        sample_goal.week_start = datetime.now().date() + timedelta(days=1)
        sample_goal.week_end = datetime.now().date() + timedelta(days=7)
        assert sample_goal.is_current == False
    
    def test_goal_days_remaining_property(self, sample_goal):
        """Test the days_remaining property"""
        # Should have 6 days remaining (week_end - today)
        assert sample_goal.days_remaining == 6
        
        # Test with past goal
        sample_goal.week_end = datetime.now().date() - timedelta(days=1)
        assert sample_goal.days_remaining == 0
    
    def test_goal_progress_percentage_property(self, sample_goal):
        """Test the progress_percentage property"""
        # On the first day, should be ~14% (1/7 days)
        percentage = sample_goal.progress_percentage
        assert 10 <= percentage <= 20  # Allow some flexibility for timing
        
        # Test with a goal that's halfway through
        sample_goal.week_start = datetime.now().date() - timedelta(days=3)
        sample_goal.week_end = datetime.now().date() + timedelta(days=3)
        percentage = sample_goal.progress_percentage
        assert 50 <= percentage <= 60  # Should be around 50% 