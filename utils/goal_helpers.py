from typing import Optional, List, Dict, Any
from datetime import datetime, date
from models.goal import Goal, GoalCategory, GoalStatus
from models.database import db

def get_current_goals(user_id: int) -> List[Goal]:
    """
    Get all user's current active goals (not completed/failed, and within their period)
    """
    today = datetime.now().date()
    return Goal.query.filter(
        Goal.user_id == user_id,
        Goal.status == GoalStatus.ACTIVE,
        Goal.week_start <= today,
        Goal.week_end >= today
    ).all()

def get_overdue_goals(user_id: int) -> List[Goal]:
    today = datetime.now().date()
    return Goal.query.filter(
        Goal.user_id == user_id,
        Goal.status == GoalStatus.ACTIVE,
        Goal.week_end < today
    ).all()

def create_goal(
    user_id: int, 
    category: GoalCategory, 
    title: str, 
    description: Optional[str] = None
) -> Goal:
    """
    Create a new goal for the user, starting today for 7 days
    """
    start, end = Goal.get_goal_dates()
    goal = Goal(
        user_id=user_id,
        category=category,
        title=title,
        description=description,
        week_start=start,
        week_end=end,
        status=GoalStatus.ACTIVE
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
    return Goal.query.filter_by(user_id=user_id)\
        .order_by(Goal.created_at.desc())\
        .limit(limit)\
        .all()

def get_goal_stats(user_id: int) -> Dict[str, Any]:
    goals = Goal.query.filter_by(user_id=user_id).all()
    total_goals = len(goals)
    completed_goals = len([g for g in goals if g.status == GoalStatus.COMPLETED])
    failed_goals = len([g for g in goals if g.status == GoalStatus.FAILED])
    active_goals = len([g for g in goals if g.status == GoalStatus.ACTIVE and g.week_end >= datetime.now().date()])
    completion_rate = (completed_goals / total_goals * 100) if total_goals > 0 else 0
    return {
        'total_goals': total_goals,
        'completed_goals': completed_goals,
        'failed_goals': failed_goals,
        'active_goals': active_goals,
        'completion_rate': round(completion_rate, 1)
    }

def get_predefined_goals() -> Dict[GoalCategory, List[str]]:
    return {
        GoalCategory.EXERCISE: [
            "Exercise 3 times this week",
            "Go for a 30-minute walk daily",
            "Try a new workout class",
            "Complete 5 strength training sessions"
        ],
        GoalCategory.LEARNING: [
            "Read for 30 minutes daily",
            "Complete one online course module",
            "Learn a new skill or hobby",
            "Practice a language for 15 minutes daily"
        ],
        GoalCategory.MINDFULNESS: [
            "Meditate for 10 minutes daily",
            "Practice deep breathing exercises",
            "Write in a gratitude journal",
            "Take 3 mindful breaks during work"
        ],
        GoalCategory.SOCIAL: [
            "Call a friend or family member",
            "Plan a social activity",
            "Reach out to someone you haven't talked to",
            "Attend a social event or gathering"
        ],
        GoalCategory.PRODUCTIVITY: [
            "Organize your workspace",
            "Complete 3 important tasks",
            "Learn a new productivity tool",
            "Create a weekly schedule and stick to it"
        ],
        GoalCategory.PERSONAL_DEV: [
            "Set aside time for self-reflection",
            "Work on a personal project",
            "Practice a new habit",
            "Review and update your goals"
        ],
        GoalCategory.HOME: [
            "Declutter one room",
            "Organize your digital files",
            "Create a cleaning schedule",
            "Improve your living space"
        ],
        GoalCategory.CREATIVE: [
            "Work on a creative project",
            "Try a new art form",
            "Write something creative",
            "Learn to play an instrument"
        ]
    } 