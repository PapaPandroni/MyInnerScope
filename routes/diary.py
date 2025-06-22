from flask import Blueprint, render_template, request, redirect, session
from datetime import date, timedelta
from models import User, DiaryEntry, DailyStats, db

diary_bp = Blueprint('diary', __name__)

@diary_bp.route("/diary", methods=["GET", "POST"])
def diary_entry():
    if "user_id" not in session:
        return redirect("/login")

    # Fetch user for display name
    user_id = session["user_id"]
    user = User.query.get(user_id)
    if user.user_name:
        display_name = user.user_name
    else:
        display_name = user.email.split('@')[0]

    if request.method == "POST":
        content = request.form["content"]
        rating = int(request.form["rating"])
        user_id = session["user_id"]
        today = date.today()

        # Check if DailyStats exists for today
        stats = DailyStats.query.filter_by(user_id=user_id, date=today).first()

        if stats is None:
            # Check if user had an entry yesterday
            yesterday = today - timedelta(days=1)
            yesterdays_stats = DailyStats.query.filter_by(user_id=user_id, date=yesterday).first()
            
            # Start a new streak or continue it
            if yesterdays_stats and yesterdays_stats.current_streak > 0:
                new_streak = yesterdays_stats.current_streak + 1
            else:
                new_streak = 1

            # Create today's stats entry
            stats = DailyStats(
                user_id=user_id,
                date=today,
                current_streak=new_streak,
                longest_streak=new_streak,
                points=0
            )

            # Check and update longest streak
            longest = DailyStats.query.filter_by(user_id=user_id).order_by(DailyStats.longest_streak.desc()).first()
            if longest and longest.longest_streak > new_streak:
                stats.longest_streak = longest.longest_streak

            db.session.add(stats)

        elif stats.current_streak == 0:
            # This row was created by login, now update streaks
            yesterday = today - timedelta(days=1)
            yesterdays_stats = DailyStats.query.filter_by(user_id=user_id, date=yesterday).first()
    
            if yesterdays_stats and yesterdays_stats.current_streak > 0:
                stats.current_streak = yesterdays_stats.current_streak + 1
            else:
                stats.current_streak = 1

            # Update longest streak if needed
            if stats.current_streak > stats.longest_streak:
                stats.longest_streak = stats.current_streak

        # Add points based on rating
        if rating == 1:
            stats.points += 5
        elif rating == -1:
            stats.points += 2

        # Save diary entry
        new_entry = DiaryEntry(
            user_id=user_id,
            content=content,
            rating=rating
        )
        db.session.add(new_entry)
        db.session.commit()

        return redirect("/diary")

    return render_template("diary.html", display_name=display_name)