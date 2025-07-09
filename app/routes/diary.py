from typing import Union
from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.wrappers import Response as WerkzeugResponse
from datetime import date, timedelta
from ..models import User, DiaryEntry, DailyStats, db
from ..utils.progress_helpers import get_recent_entries
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
        today = date.today()

        stats = DailyStats.query.filter_by(user_id=user_id, date=today).first()

        if stats is None:
            yesterday = today - timedelta(days=1)
            yesterdays_stats = DailyStats.query.filter_by(
                user_id=user_id, date=yesterday
            ).first()

            new_streak = 1
            if yesterdays_stats and yesterdays_stats.current_streak > 0:
                new_streak = yesterdays_stats.current_streak + 1

            stats = DailyStats(
                user_id=user_id, date=today, current_streak=new_streak, points=0
            )

            longest = (
                DailyStats.query.filter_by(user_id=user_id)
                .order_by(DailyStats.longest_streak.desc())
                .first()
            )
            stats.longest_streak = longest.longest_streak if longest else new_streak
            if new_streak > stats.longest_streak:
                stats.longest_streak = new_streak

            db.session.add(stats)

        elif stats.current_streak == 0:
            yesterday = today - timedelta(days=1)
            yesterdays_stats = DailyStats.query.filter_by(
                user_id=user_id, date=yesterday
            ).first()

            if yesterdays_stats and yesterdays_stats.current_streak > 0:
                stats.current_streak = yesterdays_stats.current_streak + 1
            else:
                stats.current_streak = 1

            if stats.current_streak > stats.longest_streak:
                stats.longest_streak = stats.current_streak

        stats.points += 5 if rating == 1 else 2

        new_entry = DiaryEntry(user_id=user_id, content=content, rating=rating)
        db.session.add(new_entry)
        db.session.commit()

        return redirect("/diary")

    # Flash errors if validation fails
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(error, "danger")
        return (
            render_template(
                "diary.html",
                display_name=display_name,
                recent_entries=get_recent_entries(user_id),
                form=form,
            ),
            400,
        )

    recent_entries = get_recent_entries(user_id)
    return render_template(
        "diary.html",
        display_name=display_name,
        recent_entries=recent_entries,
        form=form,
    )
