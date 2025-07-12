from typing import Union
from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.wrappers import Response as WerkzeugResponse
from datetime import date, timedelta
from ..models import User, DiaryEntry, DailyStats, db
from ..utils.progress_helpers import get_recent_entries, get_current_streak, get_total_points
from ..utils.points_service import award_diary_points
from ..forms import DiaryEntryForm

diary_bp = Blueprint("diary", __name__)


@diary_bp.route("/diary", methods=["GET", "POST"])
def diary_entry() -> Union[str, tuple[str, int], WerkzeugResponse]:
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    user = db.session.get(User, user_id)

    if user.user_name:
        display_name = user.user_name
    else:
        display_name = user.email.split("@")[0]

    form = DiaryEntryForm()

    if form.validate_on_submit():
        content = form.content.data
        rating = form.rating.data

        # Create diary entry first
        new_entry = DiaryEntry(user_id=user_id, content=content, rating=rating)
        db.session.add(new_entry)
        db.session.flush()  # Flush to get the ID for points service

        # Award points through the points service (this will also update DailyStats)
        award_diary_points(user_id, new_entry.id, rating)

        # Commit all changes
        db.session.commit()

        # Clear the form for the next entry
        form = DiaryEntryForm(formdata=None)

        recent_entries = get_recent_entries(user_id)
        is_new_user = len(recent_entries) == 0
        
        # Get updated user stats for header
        current_streak = get_current_streak(user_id)
        total_points = get_total_points(user_id)

        return render_template(
            "diary/diary.html",
            display_name=display_name,
            recent_entries=recent_entries,
            form=form,
            is_new_user=is_new_user,
            entry_saved=True,
            current_streak=current_streak,
            total_points=total_points,
        )

    # Flash errors if validation fails
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(error, "danger")
        recent_entries = get_recent_entries(user_id)
        is_new_user = len(recent_entries) == 0
        
        # Get user stats for header
        current_streak = get_current_streak(user_id)
        total_points = get_total_points(user_id)
        
        return (
            render_template(
                "diary/diary.html",
                display_name=display_name,
                recent_entries=recent_entries,
                form=form,
                is_new_user=is_new_user,
                current_streak=current_streak,
                total_points=total_points,
            ),
            400,
        )

    recent_entries = get_recent_entries(user_id)
    
    # Check if user should see onboarding tour (new user with no entries)
    is_new_user = len(recent_entries) == 0
    
    # Get user stats for header
    current_streak = get_current_streak(user_id)
    total_points = get_total_points(user_id)
    
    return render_template(
        "diary/diary.html",
        display_name=display_name,
        recent_entries=recent_entries,
        form=form,
        is_new_user=is_new_user,
        current_streak=current_streak,
        total_points=total_points,
    )
