from datetime import date, timedelta
from typing import List, Dict, Tuple, Any
from ..models import User, DiaryEntry, DailyStats, db


def get_display_name(user: User) -> str:
    """Return the display name for a user.
    
    Args:
        user: The User object.
        
    Returns:
        The user's display name or email prefix if no display name is set.
    """
    return user.user_name if user.user_name else user.email.split("@")[0]


def get_today_stats(user_id: int, today: date) -> int:
    """Return today's points for the user.
    
    Args:
        user_id: The ID of the user.
        today: Today's date.
        
    Returns:
        The points earned today, or 0 if no stats exist.
    """
    stats_today = DailyStats.query.filter_by(user_id=user_id, date=today).first()
    return stats_today.points if stats_today else 0


def get_total_points(user_id: int) -> int:
    """Return the total points for the user.
    
    Args:
        user_id: The ID of the user.
        
    Returns:
        The cumulative points earned by the user.
    """
    return (
        db.session.query(db.func.sum(DailyStats.points))
        .filter_by(user_id=user_id)
        .scalar()
        or 0
    )


def get_current_streak(user_id: int) -> int:
    """Return the current streak for the user.
    
    Args:
        user_id: The ID of the user.
        
    Returns:
        The user's current daily streak count.
    """
    row = (
        DailyStats.query.filter_by(user_id=user_id)
        .order_by(DailyStats.date.desc())
        .first()
    )
    return row.current_streak if row else 0


def get_longest_streak(user_id: int) -> int:
    """Return the longest streak for the user.
    
    Args:
        user_id: The ID of the user.
        
    Returns:
        The user's longest recorded daily streak.
    """
    row = (
        DailyStats.query.filter_by(user_id=user_id)
        .order_by(DailyStats.longest_streak.desc())
        .first()
    )
    return row.longest_streak if row else 0


def get_total_entries(user_id: int) -> int:
    """Return the total number of diary entries for the user.
    
    Args:
        user_id: The ID of the user.
        
    Returns:
        The total count of diary entries.
    """
    return DiaryEntry.query.filter_by(user_id=user_id).count()


def get_points_data(user_id: int) -> List[List[Any]]:
    """Return cumulative points data for the user.
    
    Args:
        user_id: The ID of the user.
        
    Returns:
        List of [date_string, cumulative_points] pairs for charting.
    """
    raw_data = (
        DailyStats.query.filter_by(user_id=user_id)
        .order_by(DailyStats.date)
        .with_entities(DailyStats.date, DailyStats.points)
        .all()
    )
    cumulative_points = 0
    cumulative_data = []
    for row in raw_data:
        cumulative_points += row.points
        cumulative_data.append([str(row.date), cumulative_points])
    return cumulative_data


def get_top_days_with_entries(user_id: int) -> List[Dict[str, Any]]:
    """Return the top 3 days with most points and their diary entries.
    
    Args:
        user_id: The ID of the user.
        
    Returns:
        List of dictionaries containing date, points, and entries for top days.
    """
    top_days = (
        db.session.query(DailyStats)
        .filter_by(user_id=user_id)
        .filter(DailyStats.points > 0)
        .order_by(DailyStats.points.desc())
        .limit(3)
        .all()
    )
    result = []
    for day in top_days:
        entries = DiaryEntry.query.filter_by(user_id=user_id, entry_date=day.date).all()
        result.append({"date": day.date, "points": day.points, "entries": entries})
    return result


def get_weekday_data(user_id: int) -> Tuple[List[Dict[str, Any]], bool]:
    """Return weekday analysis data and data sufficiency indicator.
    
    Args:
        user_id: The ID of the user.
        
    Returns:
        Tuple of (weekday_data_list, has_sufficient_data_boolean).
    """
    day_analysis = (
        db.session.query(
            db.func.extract("dow", DailyStats.date).label("weekday"),
            db.func.avg(DailyStats.points).label("avg_points"),
            db.func.count(DailyStats.id).label("entry_count"),
        )
        .filter_by(user_id=user_id)
        .filter(DailyStats.points > 0)
        .group_by(db.func.extract("dow", DailyStats.date))
        .all()
    )
    weekday_names = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
    ]
    weekday_data = []
    for i in range(7):
        day_data = next((d for d in day_analysis if int(d.weekday) == i), None)
        if day_data:
            weekday_data.append(
                {"name": weekday_names[i], "avg_points": round(day_data.avg_points, 1)}
            )
        else:
            weekday_data.append({"name": weekday_names[i], "avg_points": 0})
    
    # Chart unlocks based on diary entries on different weekdays, not daily stats
    has_sufficient_weekday_data = get_unique_weekdays_with_entries(user_id) >= 2
    return weekday_data, has_sufficient_weekday_data


def get_sample_weekday_data() -> List[Dict[str, Any]]:
    """Return sample weekday data for placeholder purposes.
    
    Returns:
        List of sample weekday statistics for demonstration.
    """
    return [
        {"name": "Sunday", "avg_points": 3.2},
        {"name": "Monday", "avg_points": 5.8},
        {"name": "Tuesday", "avg_points": 7.1},
        {"name": "Wednesday", "avg_points": 4.5},
        {"name": "Thursday", "avg_points": 6.3},
        {"name": "Friday", "avg_points": 2.9},
        {"name": "Saturday", "avg_points": 8.4},
    ]


def get_trend_message(user_id: int, today: date) -> str:
    """Return the trend message for the user based on recent activity.
    
    Args:
        user_id: The ID of the user.
        today: Today's date.
        
    Returns:
        Motivational message based on the last 14 days of activity.
    """
    last_7_start = today - timedelta(days=6)
    last_7_end = today
    previous_7_start = today - timedelta(days=13)
    previous_7_end = today - timedelta(days=7)
    first_entry = (
        DiaryEntry.query.filter_by(user_id=user_id)
        .order_by(DiaryEntry.entry_date)
        .first()
    )
    days_since_start = (today - first_entry.entry_date).days if first_entry else 0
    if days_since_start < 13:
        return "Keep writing to unlock insights about your self-improvement journey!"
    last_7_points = (
        db.session.query(db.func.sum(DailyStats.points))
        .filter_by(user_id=user_id)
        .filter(DailyStats.date >= last_7_start)
        .filter(DailyStats.date <= last_7_end)
        .scalar()
        or 0
    )
    previous_7_points = (
        db.session.query(db.func.sum(DailyStats.points))
        .filter_by(user_id=user_id)
        .filter(DailyStats.date >= previous_7_start)
        .filter(DailyStats.date <= previous_7_end)
        .scalar()
        or 0
    )
    point_difference = last_7_points - previous_7_points
    if point_difference > 5:
        return "You're earning more points than last week! Keep up the great self-improvement!"
    elif point_difference < -5:
        return "Let's beat last week! Keep reflecting to keep improving!"
    else:
        return "Steady progress! Consistency is key to self-improvement!"


def get_unique_weekdays_with_entries(user_id: int) -> int:
    """Get the count of unique weekdays that have diary entries.
    
    Args:
        user_id: The ID of the user.
        
    Returns:
        Count of unique weekdays (0-7) that have at least one diary entry.
    """
    unique_weekdays = (
        db.session.query(db.func.extract("dow", DiaryEntry.entry_date))
        .filter_by(user_id=user_id)
        .distinct()
        .count()
    )
    return unique_weekdays


def get_recent_entries(user_id: int, limit: int = 3) -> List[DiaryEntry]:
    """Get the most recent diary entries for the user.
    
    Args:
        user_id: The ID of the user.
        limit: Maximum number of entries to return.
        
    Returns:
        List of the most recent DiaryEntry objects.
    """
    return (
        DiaryEntry.query.filter_by(user_id=user_id)
        .order_by(DiaryEntry.id.desc())
        .limit(limit)
        .all()
    )
