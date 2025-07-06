from flask import Blueprint, render_template, redirect, session, request
from datetime import datetime
from ..models import User, DiaryEntry, db
from ..utils import handle_search

reader_bp = Blueprint('reader', __name__)

@reader_bp.route("/read-diary")
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
