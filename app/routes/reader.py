from typing import Union
from flask import Blueprint, render_template, redirect, session, request
from werkzeug.wrappers import Response as WerkzeugResponse
from datetime import datetime
from ..models import User, DiaryEntry, db
from ..utils import handle_search
from ..utils.progress_helpers import get_recent_entries

reader_bp = Blueprint("reader", __name__)


@reader_bp.route("/read-diary")
def read_diary() -> Union[str, WerkzeugResponse]:
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    user = User.query.get(user_id)

    # Get display name
    if user.user_name:
        display_name = user.user_name
    else:
        display_name = user.email.split("@")[0]

    # Get all dates that have diary entries (sorted chronologically)
    diary_dates = (
        db.session.query(DiaryEntry.entry_date)
        .filter_by(user_id=user_id)
        .distinct()
        .order_by(DiaryEntry.entry_date)
        .all()
    )

    # Convert to list of date objects
    diary_dates = [row.entry_date for row in diary_dates]

    if not diary_dates:
        # No entries yet - show empty state
        # Check if user should see onboarding tour (new user with no entries)
        recent_entries = get_recent_entries(user_id)
        is_new_user = len(recent_entries) == 0
        
        return render_template(
            "reader/read_diary.html", display_name=display_name, no_entries=True, is_new_user=is_new_user
        )

    # Check for search parameters
    search_text = request.args.get("search", "").strip()
    search_date = request.args.get("search_date", "").strip()
    rating_param = request.args.get("rating", "").strip()
    
    # Convert rating parameter to integer if provided
    rating = None
    if rating_param:
        try:
            rating = int(rating_param)
            if rating not in [-1, 1]:
                rating = None
        except ValueError:
            rating = None

    # Handle search functionality
    if search_text or search_date or rating is not None:
        return handle_search(
            user_id, display_name, diary_dates, search_text, search_date, rating
        )

    # Get the date parameter from URL (existing functionality)
    date_param = request.args.get("date")

    if not date_param:
        # Show front page
        first_entry_date = diary_dates[0]
        # Check if user should see onboarding tour (new user with no entries)
        recent_entries = get_recent_entries(user_id)
        is_new_user = len(recent_entries) == 0
        
        return render_template(
            "reader/read_diary.html",
            display_name=display_name,
            first_entry_date=first_entry_date,
            show_front_page=True,
            diary_dates=diary_dates,
            is_new_user=is_new_user,
        )

    # Parse the date parameter
    try:
        current_date = datetime.strptime(date_param, "%Y-%m-%d").date()
    except ValueError:
        # Invalid date format, redirect to front page
        return redirect("/read-diary")

    # Check if this date has entries
    if current_date not in diary_dates:
        # No entries for this date, redirect to front page
        return redirect("/read-diary")

    # Get entries for this date
    entries = (
        DiaryEntry.query.filter_by(user_id=user_id, entry_date=current_date)
        .order_by(DiaryEntry.id)
        .all()
    )

    # Find current date index for navigation
    current_index = diary_dates.index(current_date)

    # Determine previous and next dates
    prev_date = diary_dates[current_index - 1] if current_index > 0 else None
    next_date = (
        diary_dates[current_index + 1] if current_index < len(diary_dates) - 1 else None
    )

    # Format the date for display (e.g., "Monday, May 5th 2025")
    day_name = current_date.strftime("%A")
    month_name = current_date.strftime("%B")
    day_num = current_date.day
    year = current_date.year

    # Add ordinal suffix (1st, 2nd, 3rd, 4th, etc.)
    if 4 <= day_num <= 20 or 24 <= day_num <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day_num % 10 - 1]

    formatted_date = f"{day_name}, {month_name} {day_num}{suffix} {year}"

    # Check if user should see onboarding tour (new user with no entries)
    recent_entries = get_recent_entries(user_id)
    is_new_user = len(recent_entries) == 0
    
    return render_template(
        "reader/read_diary.html",
        display_name=display_name,
        entries=entries,
        current_date=current_date,
        formatted_date=formatted_date,
        prev_date=prev_date,
        next_date=next_date,
        diary_dates=diary_dates,
        show_day_page=True,
        is_new_user=is_new_user,
    )
