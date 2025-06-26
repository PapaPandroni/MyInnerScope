from flask import Blueprint, render_template, redirect, session, send_file
from datetime import date
from models import User, DiaryEntry, DailyStats, db
from utils.pdf_generator import generate_journey_pdf
from utils.progress_helpers import (
    get_display_name, get_today_stats, get_total_points, get_current_streak,
    get_longest_streak, get_total_entries, get_points_data, get_top_days_with_entries,
    get_weekday_data, get_sample_weekday_data, get_trend_message
)

progress_bp = Blueprint('progress', __name__)

@progress_bp.route("/progress")
def progress():
    if "user_id" not in session:
        return redirect("/login")
    user_id = session["user_id"]
    user = User.query.get(user_id)
    today = date.today()

    display_name = get_display_name(user)
    points_today = get_today_stats(user_id, today)
    total_points = get_total_points(user_id)
    current_streak = get_current_streak(user_id)
    longest_streak = get_longest_streak(user_id)
    total_entries = get_total_entries(user_id)
    points_data = get_points_data(user_id)
    top_days_with_entries = get_top_days_with_entries(user_id)
    weekday_data, has_sufficient_weekday_data = get_weekday_data(user_id)
    sample_weekday_data = get_sample_weekday_data()
    trend_message = get_trend_message(user_id, today)

    return render_template(
        "progress.html",
        points_today=points_today,
        total_points=total_points,
        current_streak=current_streak,
        longest_streak=longest_streak,
        total_entries=total_entries,
        points_data=points_data,
        top_days=top_days_with_entries,
        weekday_data=weekday_data,
        has_sufficient_weekday_data=has_sufficient_weekday_data,
        sample_weekday_data=sample_weekday_data,
        trend_message=trend_message,
        display_name=display_name   
    )

@progress_bp.route("/export-journey", methods=["POST"])
def export_journey():
    if "user_id" not in session:
        return "Unauthorized", 401
    user_id = session["user_id"]
    user = User.query.get(user_id)
    entries = DiaryEntry.query\
        .filter_by(user_id=user_id)\
        .order_by(DiaryEntry.entry_date.asc())\
        .options(db.joinedload(DiaryEntry.user))\
        .all()
    for entry in entries:
        _ = entry.content
        _ = entry.entry_date
        _ = entry.rating
    print(f"Total entries found: {len(entries)}")
    if entries:
        print("Entry dates:")
        for entry in entries:
            print(f"- {entry.entry_date}: {entry.content[:50]}...")
    points_data = get_points_data(user_id)
    weekday_data, _ = get_weekday_data(user_id)
    stats = {
        'total_points': get_total_points(user_id),
        'current_streak': get_current_streak(user_id),
        'longest_streak': get_longest_streak(user_id),
        'total_entries': len(entries)
    }
    pdf_buffer = generate_journey_pdf(
        user=user,
        entries=entries,
        points_data=points_data,
        weekday_data=weekday_data,
        top_days=[],
        stats=stats
    )
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'self-reflective-journey-{date.today()}.pdf'
    )