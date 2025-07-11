from flask import Blueprint, jsonify, session
from datetime import date
from ..models import DailyStats, DiaryEntry, Goal

api_bp = Blueprint("api", __name__)

@api_bp.route("/api/points-breakdown")
def points_breakdown():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session["user_id"]
    today = date.today()
    point_breakdown = []

    # 1. Points from Diary Entries
    diary_entries = DiaryEntry.query.filter_by(user_id=user_id, entry_date=today).all()
    for entry in diary_entries:
        if entry.rating == 1:
            point_breakdown.append({"source": "Encouraged Behavior Diary", "points": 5})
        elif entry.rating == -1:
            point_breakdown.append({"source": "Growth Opportunity Diary", "points": 2})

    # 2. Points from Goals
    goals = Goal.query.filter_by(user_id=user_id).all() # Simplified for now
    for goal in goals:
        if goal.status == "Completed" and goal.completed_at and goal.completed_at.date() == today:
            point_breakdown.append({"source": f"Goal Completed: '{goal.title}'", "points": 10})
        elif goal.status == "Failed" and goal.completed_at and goal.completed_at.date() == today:
            point_breakdown.append({"source": f"Goal Failed: '{goal.title}'", "points": 1})

    # 3. Points from Daily Login (if other activities exist)
    if diary_entries or any(g for g in goals if g.completed_at and g.completed_at.date() == today):
        daily_stats = DailyStats.query.filter_by(user_id=user_id, date=today).first()
        if daily_stats and daily_stats.points > 0:
             # This is an approximation, as we can't isolate the single login point directly
             # But we can add it if other points were scored today.
            point_breakdown.append({"source": "Daily Login Bonus", "points": 1})

    # A simple sort to make it look organized
    point_breakdown.sort(key=lambda x: x['points'], reverse=True)

    return jsonify(point_breakdown)
