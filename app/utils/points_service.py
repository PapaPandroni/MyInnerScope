"""
Points Service - Centralized point management system.

This service manages all point-earning activities and maintains consistency
between PointsLog (detailed transactions) and DailyStats (aggregated cache).
"""

from typing import Optional, List
from datetime import datetime, date
from ..models import db, DailyStats, PointsLog
from ..models.points_log import PointsSourceType


class PointsService:
    """Centralized service for managing point transactions."""
    
    @staticmethod
    def award_points(
        user_id: int,
        points: int,
        source_type: PointsSourceType,
        description: str,
        source_id: Optional[int] = None,
        target_date: Optional[date] = None
    ) -> PointsLog:
        """Award points to a user and update daily stats.
        
        Args:
            user_id: User receiving the points
            points: Number of points to award
            source_type: Type of activity earning the points
            description: Human-readable description
            source_id: Optional ID of the source object (diary entry, goal)
            target_date: Date to award points for (defaults to today)
            
        Returns:
            The created PointsLog entry
        """
        if target_date is None:
            target_date = datetime.now().date()
        
        # Create detailed log entry
        log_entry = PointsLog.create_entry(
            user_id=user_id,
            points=points,
            source_type=source_type,
            description=description,
            date=target_date,
            source_id=source_id
        )
        
        # Update daily stats cache
        PointsService._update_daily_stats(user_id, target_date, points)
        
        # Commit both changes together
        db.session.commit()
        
        return log_entry
    
    @staticmethod
    def _update_daily_stats(user_id: int, target_date: date, points: int) -> None:
        """Update DailyStats cache with new points.
        
        Args:
            user_id: User to update stats for
            target_date: Date to update
            points: Points to add
        """
        # Get or create daily stats for the date
        stats = DailyStats.query.filter_by(user_id=user_id, date=target_date).first()
        if not stats:
            stats = DailyStats(user_id=user_id, date=target_date, points=0)
            db.session.add(stats)
        
        # Add points
        stats.points += points
        
        # Update streak calculations if this is today
        today = datetime.now().date()
        if target_date == today:
            PointsService._update_streak_calculations(user_id)
    
    @staticmethod
    def _update_streak_calculations(user_id: int) -> None:
        """Update streak calculations for the user.
        
        Args:
            user_id: User to update streaks for
        """
        from datetime import timedelta
        
        # Get all daily stats ordered by date
        all_stats = DailyStats.query.filter_by(user_id=user_id).order_by(DailyStats.date).all()
        
        if not all_stats:
            return
        
        # Calculate current streak (consecutive days with points ending today)
        current_streak = 0
        today = datetime.now().date()
        
        # Get stats for consecutive days working backwards from today
        check_date = today
        while True:
            stat = DailyStats.query.filter_by(user_id=user_id, date=check_date).first()
            if stat and stat.points > 0:
                current_streak += 1
                check_date = check_date - timedelta(days=1)
            else:
                break
        
        # Calculate longest streak from all stats
        longest_streak = 0
        temp_streak = 0
        
        # Sort stats by date and check for consecutive days
        if len(all_stats) > 1:
            for i in range(len(all_stats)):
                stat = all_stats[i]
                if stat.points > 0:
                    # Check if this continues a streak
                    if i == 0 or (stat.date - all_stats[i-1].date).days <= 1:
                        temp_streak += 1
                        longest_streak = max(longest_streak, temp_streak)
                    else:
                        temp_streak = 1
                        longest_streak = max(longest_streak, temp_streak)
                else:
                    temp_streak = 0
        else:
            # Single stat
            if all_stats[0].points > 0:
                longest_streak = 1
        
        # Update all today's stats with calculated streaks
        today_stats = DailyStats.query.filter_by(user_id=user_id, date=today).first()
        if today_stats:
            today_stats.current_streak = current_streak
            today_stats.longest_streak = longest_streak
    
    @staticmethod
    def get_daily_breakdown(user_id: int, target_date: Optional[date] = None) -> List[dict]:
        """Get detailed breakdown of points earned on a specific date.
        
        Args:
            user_id: User to get breakdown for
            target_date: Date to get breakdown for (defaults to today)
            
        Returns:
            List of dictionaries with point transaction details
        """
        if target_date is None:
            target_date = datetime.now().date()
        
        log_entries = PointsLog.get_daily_breakdown(user_id, target_date)
        
        breakdown = []
        for entry in log_entries:
            breakdown.append({
                "source": entry.description,
                "points": entry.points,
                "source_type": entry.source_type,
                "source_id": entry.source_id,
                "created_at": entry.created_at
            })
        
        return breakdown
    
    @staticmethod
    def get_daily_total(user_id: int, target_date: Optional[date] = None) -> int:
        """Get total points earned on a specific date.
        
        Args:
            user_id: User to get total for
            target_date: Date to get total for (defaults to today)
            
        Returns:
            Total points earned on the date
        """
        return PointsLog.get_daily_total(user_id, target_date)
    
    @staticmethod
    def rebuild_daily_stats_from_log(user_id: int) -> None:
        """Rebuild DailyStats from PointsLog for data consistency.
        
        This can be used to fix any inconsistencies between the detailed log
        and the aggregated stats cache.
        
        Args:
            user_id: User to rebuild stats for
        """
        # Get all dates with log entries for this user
        dates_with_points = db.session.query(PointsLog.date).filter_by(user_id=user_id).distinct().all()
        
        for (log_date,) in dates_with_points:
            # Calculate total points for this date from log
            total_points = PointsLog.get_daily_total(user_id, log_date)
            
            # Update or create daily stats
            stats = DailyStats.query.filter_by(user_id=user_id, date=log_date).first()
            if not stats:
                stats = DailyStats(user_id=user_id, date=log_date, points=total_points)
                db.session.add(stats)
            else:
                stats.points = total_points
        
        # Recalculate streaks
        PointsService._update_streak_calculations(user_id)
        
        db.session.commit()


# Convenience functions for common point awards
def award_diary_points(user_id: int, diary_entry_id: int, rating: int) -> PointsLog:
    """Award points for a diary entry.
    
    Args:
        user_id: User who wrote the entry
        diary_entry_id: ID of the diary entry
        rating: Entry rating (1 for encouraged, -1 for growth opportunity)
        
    Returns:
        The created PointsLog entry
    """
    if rating == 1:
        points = 5
        description = "Encouraged Behavior Diary"
    else:  # rating == -1
        points = 2
        description = "Growth Opportunity Diary"
    
    return PointsService.award_points(
        user_id=user_id,
        points=points,
        source_type=PointsSourceType.DIARY_ENTRY,
        description=description,
        source_id=diary_entry_id
    )


def award_goal_completion_points(user_id: int, goal_id: int, goal_title: str) -> PointsLog:
    """Award points for completing a goal.
    
    Args:
        user_id: User who completed the goal
        goal_id: ID of the completed goal
        goal_title: Title of the goal for description
        
    Returns:
        The created PointsLog entry
    """
    return PointsService.award_points(
        user_id=user_id,
        points=10,
        source_type=PointsSourceType.GOAL_COMPLETED,
        description=f"Goal Completed: '{goal_title}'",
        source_id=goal_id
    )


def award_goal_failure_points(user_id: int, goal_id: int, goal_title: str) -> PointsLog:
    """Award points for a failed goal (effort recognition).
    
    Args:
        user_id: User whose goal failed
        goal_id: ID of the failed goal
        goal_title: Title of the goal for description
        
    Returns:
        The created PointsLog entry
    """
    return PointsService.award_points(
        user_id=user_id,
        points=1,
        source_type=PointsSourceType.GOAL_FAILED,
        description=f"Goal Failed: '{goal_title}'",
        source_id=goal_id
    )


def award_login_bonus(user_id: int) -> PointsLog:
    """Award daily login bonus points.
    
    Args:
        user_id: User who logged in
        
    Returns:
        The created PointsLog entry
    """
    return PointsService.award_points(
        user_id=user_id,
        points=1,
        source_type=PointsSourceType.DAILY_LOGIN,
        description="Daily Login Bonus"
    )