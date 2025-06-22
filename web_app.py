"""
Aim for the Stars - Self-Reflection Web Application
Copyright 2025 Peremil Starklint Söderström

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, timedelta, datetime
from dotenv import load_dotenv

# Import database and models
from models import db, User, DiaryEntry, DailyStats

load_dotenv()
app = Flask(__name__)

# Get secret key from environment variable
app.secret_key = os.environ.get('SECRET_KEY')
if not app.secret_key:
    raise ValueError("No SECRET_KEY environment variable set. Please create a .env file with SECRET_KEY=your-secret-key")

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database with app
db.init_app(app)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/diary", methods=["GET", "POST"])
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

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Try to find a user with that email
        user = User.query.filter_by(email=email).first()

        if not user:
            return "No user found with that email."

        if not check_password_hash(user.password, password):
            return "Incorrect password."

        # Success! Session!
        session["user_id"] = user.id

        # Inside login route, after login is successful
        today = date.today()
        user_id = user.id

        stats = DailyStats.query.filter_by(user_id=user_id, date=today).first()

        if not stats:
            stats = DailyStats(user_id=user_id, date=today, points=1)
            db.session.add(stats)
            db.session.commit()

        return redirect("/diary")

    # If GET request, show login form
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        password_again = request.form["password_again"]
        user_name = request.form.get("user_name", None)

        if password != password_again:
            return "Passwords do not match!"

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            return "Email already registered."

        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password, user_name=user_name)

        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")

    return render_template("register.html")

@app.route("/progress")
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

    # Top 5 days with most points (including their diary entries)
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

    import random

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

@app.route("/read-diary")
def read_diary():
    if "user_id" not in session:
        return redirect("/login")
    
    user_id = session["user_id"]
    user = User.query.get(user_id)
    
    # Get display name
    if user.user_name:
        display_name = user.user_name
    else:
        display_name = user.email.split('@')[0]
    
    # Get all dates that have diary entries (sorted chronologically)
    diary_dates = db.session.query(DiaryEntry.entry_date)\
        .filter_by(user_id=user_id)\
        .distinct()\
        .order_by(DiaryEntry.entry_date)\
        .all()
    
    # Convert to list of date objects
    diary_dates = [row.entry_date for row in diary_dates]
    
    if not diary_dates:
        # No entries yet - show empty state
        return render_template("read_diary.html", 
                             display_name=display_name, 
                             no_entries=True)
    
    # Check for search parameters
    search_text = request.args.get('search', '').strip()
    search_date = request.args.get('search_date', '').strip()
    
    # Handle search functionality
    if search_text or search_date:
        return handle_search(user_id, display_name, diary_dates, search_text, search_date)
    
    # Get the date parameter from URL (existing functionality)
    date_param = request.args.get('date')
    
    if not date_param:
        # Show front page
        first_entry_date = diary_dates[0]
        return render_template("read_diary.html", 
                             display_name=display_name,
                             first_entry_date=first_entry_date,
                             show_front_page=True,
                             diary_dates=diary_dates)
    
    # Parse the date parameter
    try:
        current_date = datetime.strptime(date_param, '%Y-%m-%d').date()
    except ValueError:
        # Invalid date format, redirect to front page
        return redirect("/read-diary")
    
    # Check if this date has entries
    if current_date not in diary_dates:
        # No entries for this date, redirect to front page
        return redirect("/read-diary")
    
    # Get entries for this date
    entries = DiaryEntry.query.filter_by(user_id=user_id, entry_date=current_date)\
        .order_by(DiaryEntry.id)\
        .all()
    
    # Find current date index for navigation
    current_index = diary_dates.index(current_date)
    
    # Determine previous and next dates
    prev_date = diary_dates[current_index - 1] if current_index > 0 else None
    next_date = diary_dates[current_index + 1] if current_index < len(diary_dates) - 1 else None
    
    # Format the date for display (e.g., "Monday, May 5th 2025")
    day_name = current_date.strftime('%A')
    month_name = current_date.strftime('%B')
    day_num = current_date.day
    year = current_date.year
    
    # Add ordinal suffix (1st, 2nd, 3rd, 4th, etc.)
    if 4 <= day_num <= 20 or 24 <= day_num <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day_num % 10 - 1]
    
    formatted_date = f"{day_name}, {month_name} {day_num}{suffix} {year}"
    
    return render_template("read_diary.html",
                         display_name=display_name,
                         entries=entries,
                         current_date=current_date,
                         formatted_date=formatted_date,
                         prev_date=prev_date,
                         next_date=next_date,
                         diary_dates=diary_dates,
                         show_day_page=True)

def handle_search(user_id, display_name, diary_dates, search_text, search_date):
    # If only date is provided (no search text), redirect to that date
    if search_date and not search_text:
        return redirect(f"/read-diary?date={search_date}")

    # Build the search query
    query = DiaryEntry.query.filter_by(user_id=user_id)

    # Add date filter if specified
    if search_date:
        try:
            target_date = datetime.strptime(search_date, '%Y-%m-%d').date()
            query = query.filter(DiaryEntry.entry_date == target_date)
        except ValueError:
            # Invalid date, ignore the date filter
            pass

    # Add text search if specified
    if search_text:
        query = query.filter(DiaryEntry.content.ilike(f'%{search_text}%'))

    # Execute the search
    search_results = query.order_by(DiaryEntry.entry_date.desc()).all()

    # Create search result snippets with highlighting
    result_data = []
    for entry in search_results:
        snippet = create_search_snippet(entry.content, search_text)
        formatted_date = entry.entry_date.strftime('%A, %B %d, %Y')
        
        result_data.append({
            'date': entry.entry_date,
            'formatted_date': formatted_date,
            'snippet': snippet
        })

    return render_template("read_diary.html",
                            display_name=display_name,
                            diary_dates=diary_dates,
                            search_results=result_data,
                            show_search_results=True)

def create_search_snippet(content, search_text, context_chars=20):
    if not search_text:
        return content[:80] + "..." if len(content) > 80 else content
    
    # Find the search text (case insensitive)
    content_lower = content.lower()
    search_lower = search_text.lower()
    
    match_index = content_lower.find(search_lower)
    if match_index == -1:
        return content[:80] + "..." if len(content) > 80 else content
    
    # Calculate snippet boundaries
    start = max(0, match_index - context_chars)
    end = min(len(content), match_index + len(search_text) + context_chars)
    
    # Extract snippet
    snippet = content[start:end]
    
    # Add ellipsis if we're not at the beginning/end
    if start > 0:
        snippet = "..." + snippet
    if end < len(content):
        snippet = snippet + "..."
    
    # Highlight the search term (case insensitive replacement)
    import re
    snippet = re.sub(re.escape(search_text), f'<mark>{search_text}</mark>', snippet, flags=re.IGNORECASE)
    
    return snippet

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True)