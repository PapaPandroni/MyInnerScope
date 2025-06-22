# routes/progress.py
from flask import Blueprint, render_template, redirect, session
from datetime import date, timedelta
import random
from models import User, DiaryEntry, DailyStats, db

progress_bp = Blueprint('progress', __name__)

@progress_bp.route("/progress")
def progress():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    # Fetch user for display name
    user = User.query.get(user_id)
    if user.user_name:
        display_name = user.user_name
    else:
        display_name = user.email.split('@')[0]

    today = date.today()

    # Today's stats
    stats_today = DailyStats.query.filter_by(user_id=user_id, date=today).first()
    points_today = stats_today.points if stats_today else 0

    # All-time total points
    total_points = db.session.query(db.func.sum(DailyStats.points))\
        .filter_by(user_id=user_id).scalar() or 0

    # Most recent current streak
    current_streak_row = DailyStats.query.filter_by(user_id=user_id)\
        .order_by(DailyStats.date.desc()).first()
    current_streak = current_streak_row.current_streak if current_streak_row else 0

    # All-time longest streak
    longest_streak_row = DailyStats.query.filter_by(user_id=user_id)\
        .order_by(DailyStats.longest_streak.desc()).first()
    longest_streak = longest_streak_row.longest_streak if longest_streak_row else 0
    
    # All time number of entries
    total_entries = DiaryEntry.query.filter_by(user_id=user_id).count()

    # Fetch points for graph (list of (date, points))
    raw_data = DailyStats.query \
        .filter_by(user_id=user_id) \
        .order_by(DailyStats.date) \
        .with_entities(DailyStats.date, DailyStats.points) \
        .all()

    cumulative_points = 0
    cumulative_data = []
    for row in raw_data:
        cumulative_points += row.points
        cumulative_data.append([str(row.date), cumulative_points])

    points_data = cumulative_data

    # Top 3 days with most points (including their diary entries)
    top_days = db.session.query(DailyStats)\
        .filter_by(user_id=user_id)\
        .filter(DailyStats.points > 0)\
        .order_by(DailyStats.points.desc())\
        .limit(3)\
        .all()

    # For each top day, get all diary entries
    top_days_with_entries = []
    for day in top_days:
        entries = DiaryEntry.query.filter_by(user_id=user_id, entry_date=day.date).all()
        top_days_with_entries.append({
            'date': day.date,
            'points': day.points,
            'entries': entries
        })

    # Get average points per day of the week
    day_analysis = db.session.query(
        db.func.strftime('%w', DailyStats.date).label('weekday'),
        db.func.avg(DailyStats.points).label('avg_points'),
        db.func.count(DailyStats.id).label('entry_count')
    ).filter_by(user_id=user_id)\
    .filter(DailyStats.points > 0)\
    .group_by(db.func.strftime('%w', DailyStats.date))\
    .having(db.func.count(DailyStats.id) >= 2)\
    .all()

    # Convert to list and find best/worst days
    weekday_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    best_day_text = None
    worst_day_text = None

    if len(day_analysis) >= 2:  # Need at least 2 different days to compare
        best_day = max(day_analysis, key=lambda x: x.avg_points)
        worst_day = min(day_analysis, key=lambda x: x.avg_points)
        
        best_day_name = weekday_names[int(best_day.weekday)]
        worst_day_name = weekday_names[int(worst_day.weekday)]
        
        # Random messages for best days
        best_messages = [
            f"{best_day_name}s are your power days!",
            f"You're crushing it on {best_day_name}s!",
            f"{best_day_name}s bring out your best!",
            f"{best_day_name} motivation is on fire!",
            f"You own {best_day_name}s!"
        ]
        
        # Random messages for worst days
        worst_messages = [
            f"{worst_day_name}s seem tough for you",
            f"{worst_day_name}s could use some attention",
            f"{worst_day_name} motivation needs a boost",
            f"Consider planning something special for {worst_day_name}s",
            f"{worst_day_name}s are your growth opportunity"
        ]
        
        best_day_text = random.choice(best_messages)
        worst_day_text = random.choice(worst_messages)

    # Calculate date ranges
    last_7_start = today - timedelta(days=6)  # today-6 to today (7 days including today)
    last_7_end = today
    previous_7_start = today - timedelta(days=13)  # today-13 to today-7 (7 days)
    previous_7_end = today - timedelta(days=7)

    # Check if user has enough data (at least 14 days since registration)
    user = User.query.get(user_id)
    # We'll assume registration date exists, but if not we can use first diary entry
    first_entry = DiaryEntry.query.filter_by(user_id=user_id).order_by(DiaryEntry.entry_date).first()
    days_since_start = (today - first_entry.entry_date).days if first_entry else 0

    if days_since_start < 13:  # Less than 14 days of potential data
        trend_message = "Keep writing to unlock insights about your self-improvement journey!"
    else:
        # Calculate points for each period
        last_7_points = db.session.query(db.func.sum(DailyStats.points))\
            .filter_by(user_id=user_id)\
            .filter(DailyStats.date >= last_7_start)\
            .filter(DailyStats.date <= last_7_end)\
            .scalar() or 0
        
        previous_7_points = db.session.query(db.func.sum(DailyStats.points))\
            .filter_by(user_id=user_id)\
            .filter(DailyStats.date >= previous_7_start)\
            .filter(DailyStats.date <= previous_7_end)\
            .scalar() or 0
        
        # Determine trend message
        point_difference = last_7_points - previous_7_points
        
        if point_difference > 5:
            trend_message = "You're earning more points than last week! Keep up the great self-improvement!"
        elif point_difference < -5:
            trend_message = "Let's beat last week! Keep reflecting to keep improving!"
        else:
            trend_message = "Steady progress! Consistency is key to self-improvement!"

    return render_template(
        "progress.html",
        points_today=points_today,
        total_points=total_points,
        current_streak=current_streak,
        longest_streak=longest_streak,
        total_entries=total_entries,
        points_data=points_data,
        top_days=top_days_with_entries,
        best_day_text=best_day_text,      
        worst_day_text=worst_day_text,
        trend_message=trend_message,
        display_name=display_name   
    )