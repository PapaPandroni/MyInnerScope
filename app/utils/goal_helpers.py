from typing import Optional, List, Dict, Any
from datetime import datetime, date
from ..models.goal import Goal, GoalCategory, GoalStatus
from ..models.database import db


def get_current_goals(user_id: int) -> List[Goal]:
    """Get all user's current active goals.
    
    Args:
        user_id: The ID of the user to get goals for.
        
    Returns:
        List of active Goal objects within their time period.
    """
    today = datetime.now().date()
    return Goal.query.filter(
        Goal.user_id == user_id,
        Goal.status == GoalStatus.ACTIVE,
        Goal.week_start <= today,
        Goal.week_end >= today,
    ).all()


def get_overdue_goals(user_id: int) -> List[Goal]:
    today = datetime.now().date()
    return Goal.query.filter(
        Goal.user_id == user_id, Goal.status == GoalStatus.ACTIVE, Goal.week_end < today
    ).all()


def create_goal(
    user_id: int, category: GoalCategory, title: str, description: Optional[str] = None
) -> Goal:
    """Create a new goal for the user.
    
    Args:
        user_id: The ID of the user creating the goal.
        category: The goal category enum.
        title: The goal title.
        description: Optional goal description.
        
    Returns:
        The created Goal object.
    """
    start, end = Goal.get_goal_dates()
    goal = Goal(
        user_id=user_id,
        category=category,
        title=title,
        description=description,
        week_start=start,
        week_end=end,
        status=GoalStatus.ACTIVE,
    )
    db.session.add(goal)
    db.session.commit()
    return goal


def update_goal_progress(goal_id: int, progress_notes: str) -> Optional[Goal]:
    goal = Goal.query.get(goal_id)
    if goal:
        goal.progress_notes = progress_notes
        db.session.commit()
    return goal


def complete_goal(goal_id: int) -> Optional[Goal]:
    goal = Goal.query.get(goal_id)
    if goal and goal.status == GoalStatus.ACTIVE:
        goal.status = GoalStatus.COMPLETED
        db.session.commit()
    return goal


def fail_goal(goal_id: int) -> Optional[Goal]:
    goal = Goal.query.get(goal_id)
    if goal and goal.status == GoalStatus.ACTIVE:
        goal.status = GoalStatus.FAILED
        db.session.commit()
    return goal


def get_goal_history(user_id: int, limit: int = 10) -> List[Goal]:
    return (
        Goal.query.filter_by(user_id=user_id)
        .order_by(Goal.created_at.desc())
        .limit(limit)
        .all()
    )


def get_goal_statistics(user_id: int) -> Dict[str, Any]:
    """Gather statistics about a user's goals.
    
    Args:
        user_id: The ID of the user to get statistics for.
        
    Returns:
        Dictionary containing goal statistics including completion rate,
        category breakdowns, and total counts.
    """
    goals = Goal.query.filter(
        Goal.user_id == user_id,
        Goal.status.in_([GoalStatus.COMPLETED, GoalStatus.FAILED]),
    ).all()

    completed_goals = sum(1 for g in goals if g.status == GoalStatus.COMPLETED)
    failed_goals = sum(1 for g in goals if g.status == GoalStatus.FAILED)
    total_past_goals = completed_goals + failed_goals

    success_rate = (
        (completed_goals / total_past_goals * 100) if total_past_goals > 0 else 0
    )

    category_stats = {
        category.value: {"completed": 0, "failed": 0} for category in GoalCategory
    }

    for goal in goals:
        if goal.status == GoalStatus.COMPLETED:
            category_stats[goal.category.value]["completed"] += 1
        elif goal.status == GoalStatus.FAILED:
            category_stats[goal.category.value]["failed"] += 1

    return {
        "total_completed": completed_goals,
        "success_rate": round(success_rate, 1),
        "category_stats": category_stats,
        "has_stats": total_past_goals > 0,
    }


def get_predefined_goals() -> Dict[GoalCategory, List[str]]:
    return {
        GoalCategory.EXERCISE: [
            "Exercise 3 times this week",
            "Go for a 30-minute walk daily",
            "Try a new workout class",
            "Complete 5 strength training sessions",
        ],
        GoalCategory.LEARNING: [
            "Read for 30 minutes daily",
            "Complete one online course module",
            "Learn a new skill or hobby",
            "Practice a language for 15 minutes daily",
        ],
        GoalCategory.MINDFULNESS: [
            "Meditate for 10 minutes daily",
            "Practice deep breathing exercises",
            "Write in a gratitude journal",
            "Take 3 mindful breaks during work",
        ],
        GoalCategory.SOCIAL: [
            "Call a friend or family member",
            "Plan a social activity",
            "Reach out to someone you haven't talked to",
            "Attend a social event or gathering",
        ],
        GoalCategory.PRODUCTIVITY: [
            "Organize your workspace",
            "Complete 3 important tasks",
            "Learn a new productivity tool",
            "Create a weekly schedule and stick to it",
        ],
        GoalCategory.PERSONAL_DEV: [
            "Set aside time for self-reflection",
            "Work on a personal project",
            "Practice a new habit",
            "Review and update your goals",
        ],
        GoalCategory.HOME: [
            "Declutter one room",
            "Organize your digital files",
            "Create a cleaning schedule",
            "Improve your living space",
        ],
        GoalCategory.CREATIVE: [
            "Work on a creative project",
            "Try a new art form",
            "Write something creative",
            "Learn to play an instrument",
        ],
    }
