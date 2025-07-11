from typing import Union, Tuple
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    flash,
    session,
    Response,
)
from werkzeug.wrappers import Response as WerkzeugResponse
from ..models.goal import GoalCategory, GoalStatus
from ..models import User, DailyStats, db
from ..utils.goal_helpers import (
    get_current_goals,
    get_overdue_goals,
    create_goal,
    update_goal_progress,
    complete_goal,
    fail_goal,
    get_goal_history,
    get_goal_statistics,
    get_predefined_goals,
)
from ..utils.progress_helpers import get_recent_entries
from ..forms import GoalForm, GoalProgressForm
from datetime import date

goals_bp = Blueprint("goals", __name__)


@goals_bp.route("/goals")
def goals_page() -> Union[str, WerkzeugResponse]:
    """Display the main goals page with current and historical goals.
    
    Returns:
        Rendered goals template or redirect to login.
    """
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    current_goals = get_current_goals(user_id)
    overdue_goals = get_overdue_goals(user_id)
    goal_history = get_goal_history(user_id, limit=10)
    goal_stats = get_goal_statistics(user_id)
    predefined_goals = get_predefined_goals()
    goal_form = GoalForm()
    progress_form = GoalProgressForm()

    # Check if user should see onboarding tour (new user with no entries)
    recent_entries = get_recent_entries(user_id)
    is_new_user = len(recent_entries) == 0

    return render_template(
        "goals/goals.html",
        current_goals=current_goals,
        overdue_goals=overdue_goals,
        goal_history=goal_history,
        goal_stats=goal_stats,
        predefined_goals=predefined_goals,
        categories=GoalCategory,
        goal_form=goal_form,
        progress_form=progress_form,
        is_new_user=is_new_user,
    )


@goals_bp.route("/goals/create", methods=["POST"])
def create_new_goal() -> Union[WerkzeugResponse, Tuple[str, int]]:
    """Create a new goal for the current week.
    
    Returns:
        Redirect to goals page or rendered template with errors.
    """
    if "user_id" not in session:
        return redirect("/login")

    form = GoalForm()

    if form.validate_on_submit():
        try:
            user_id = session["user_id"]
            category_name = form.category.data
            title = form.title.data.strip()
            description = (
                form.description.data.strip() if form.description.data else None
            )

            # Convert category name to enum
            try:
                category = GoalCategory(category_name)
            except ValueError:
                flash("Invalid goal category selected.", "danger")
                return redirect(url_for("goals.goals_page"), 400)

            # Create the goal
            goal = create_goal(
                user_id=user_id, category=category, title=title, description=description
            )

            flash(f'Goal "{goal.title}" created successfully!', "success")
            return redirect(url_for("goals.goals_page"))

        except Exception as e:
            flash("An error occurred while creating your goal.", "danger")
            return redirect(url_for("goals.goals_page"), 500)
    else:
        user_id = session["user_id"]
        current_goals = get_current_goals(user_id)
        overdue_goals = get_overdue_goals(user_id)
        goal_history = get_goal_history(user_id, limit=10)
        goal_stats = get_goal_statistics(user_id)
        predefined_goals = get_predefined_goals()

        # Check if user should see onboarding tour (new user with no entries)
        recent_entries = get_recent_entries(user_id)
        is_new_user = len(recent_entries) == 0

        # Flash validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(error, "danger")
        return (
            render_template(
                "goals/goals.html",
                current_goals=current_goals,
                overdue_goals=overdue_goals,
                goal_history=goal_history,
                goal_stats=goal_stats,
                predefined_goals=predefined_goals,
                categories=GoalCategory,
                goal_form=form,
                is_new_user=is_new_user,
            ),
            400,
        )


@goals_bp.route("/goals/<int:goal_id>/update", methods=["POST"])
def update_goal(goal_id: int) -> Union[WerkzeugResponse, Tuple[str, int]]:
    """Update goal progress notes.
    
    Args:
        goal_id: The ID of the goal to update.
        
    Returns:
        Redirect to goals page or rendered template with errors.
    """
    if "user_id" not in session:
        return redirect("/login")

    form = GoalProgressForm()

    if form.validate_on_submit():
        try:
            progress_notes = (
                form.progress_notes.data.strip() if form.progress_notes.data else None
            )

            goal = update_goal_progress(goal_id, progress_notes)

            if goal:
                flash("Goal progress updated successfully!", "success")
            else:
                flash("Goal not found.", "danger")

            return redirect(url_for("goals.goals_page"))

        except Exception as e:
            flash("An error occurred while updating your goal.", "danger")
            return redirect(url_for("goals.goals_page"), 500)
    else:
        user_id = session["user_id"]
        current_goals = get_current_goals(user_id)
        overdue_goals = get_overdue_goals(user_id)
        goal_history = get_goal_history(user_id, limit=10)
        goal_stats = get_goal_statistics(user_id)
        predefined_goals = get_predefined_goals()

        # Flash validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(error, "danger")
        return (
            render_template(
                "goals/goals.html",
                current_goals=current_goals,
                overdue_goals=overdue_goals,
                goal_history=goal_history,
                goal_stats=goal_stats,
                predefined_goals=predefined_goals,
                categories=GoalCategory,
                goal_form=GoalForm(),  # Pass a new GoalForm for the create section
                progress_form=form,
            ),
            400,
        )  # Pass the progress form with errors


@goals_bp.route("/goals/<int:goal_id>/complete", methods=["POST"])
def mark_goal_complete(goal_id: int) -> Tuple[str, int]:
    """Mark a goal as completed and award points.
    
    Args:
        goal_id: The ID of the goal to mark as complete.
        
    Returns:
        Rendered goals template with status message.
    """
    if "user_id" not in session:
        return redirect("/login")

    try:
        user_id = session["user_id"]
        goal = complete_goal(goal_id)

        if goal:
            # Award 10 points for completed goal
            today = date.today()
            stats = DailyStats.query.filter_by(user_id=user_id, date=today).first()
            if not stats:
                stats = DailyStats(user_id=user_id, date=today, points=0)
                db.session.add(stats)
            stats.points += 10
            db.session.commit()
            flash(
                f'Congratulations! You completed your goal: "{goal.title}"', "success"
            )
            # Re-render the page with a 200 OK status for success
            user_id = session["user_id"]
            current_goals = get_current_goals(user_id)
            overdue_goals = get_overdue_goals(user_id)
            goal_history = get_goal_history(user_id, limit=10)
            goal_stats = get_goal_statistics(user_id)
            predefined_goals = get_predefined_goals()
            goal_form = GoalForm()
            progress_form = GoalProgressForm()

            return (
                render_template(
                    "goals/goals.html",
                    current_goals=current_goals,
                    overdue_goals=overdue_goals,
                    goal_history=goal_history,
                    goal_stats=goal_stats,
                    predefined_goals=predefined_goals,
                    categories=GoalCategory,
                    goal_form=goal_form,
                    progress_form=progress_form,
                ),
                200,
            )
        else:
            flash("Goal not found.", "danger")

        user_id = session["user_id"]
        current_goals = get_current_goals(user_id)
        overdue_goals = get_overdue_goals(user_id)
        goal_history = get_goal_history(user_id, limit=10)
        goal_stats = get_goal_statistics(user_id)
        predefined_goals = get_predefined_goals()
        goal_form = GoalForm()
        progress_form = GoalProgressForm()

        return (
            render_template(
                "goals/goals.html",
                current_goals=current_goals,
                overdue_goals=overdue_goals,
                goal_history=goal_history,
                goal_stats=goal_stats,
                predefined_goals=predefined_goals,
                categories=GoalCategory,
                goal_form=goal_form,
                progress_form=progress_form,
            ),
            404,
        )

    except Exception as e:
        flash("An error occurred while completing your goal.", "danger")
        user_id = session["user_id"]
        current_goals = get_current_goals(user_id)
        overdue_goals = get_overdue_goals(user_id)
        goal_history = get_goal_history(user_id, limit=10)
        goal_stats = get_goal_statistics(user_id)
        predefined_goals = get_predefined_goals()
        goal_form = GoalForm()
        progress_form = GoalProgressForm()

        return (
            render_template(
                "goals/goals.html",
                current_goals=current_goals,
                overdue_goals=overdue_goals,
                goal_history=goal_history,
                goal_stats=goal_stats,
                predefined_goals=predefined_goals,
                categories=GoalCategory,
                goal_form=goal_form,
                progress_form=progress_form,
            ),
            500,
        )


@goals_bp.route("/goals/<int:goal_id>/fail", methods=["POST"])
def mark_goal_failed(goal_id: int) -> Tuple[str, int]:
    if "user_id" not in session:
        return redirect("/login")
    try:
        user_id = session["user_id"]
        goal = fail_goal(goal_id)
        if goal:
            # Award 1 point for failed goal
            today = date.today()
            stats = DailyStats.query.filter_by(user_id=user_id, date=today).first()
            if not stats:
                stats = DailyStats(user_id=user_id, date=today, points=0)
                db.session.add(stats)
            stats.points += 1
            db.session.commit()
            flash(f'Goal marked as failed: "{goal.title}"', "warning")
            # Re-render the page with a 200 OK status for success
            user_id = session["user_id"]
            current_goals = get_current_goals(user_id)
            overdue_goals = get_overdue_goals(user_id)
            goal_history = get_goal_history(user_id, limit=10)
            goal_stats = get_goal_statistics(user_id)
            predefined_goals = get_predefined_goals()
            goal_form = GoalForm()
            progress_form = GoalProgressForm()

            return (
                render_template(
                    "goals/goals.html",
                    current_goals=current_goals,
                    overdue_goals=overdue_goals,
                    goal_history=goal_history,
                    goal_stats=goal_stats,
                    predefined_goals=predefined_goals,
                    categories=GoalCategory,
                    goal_form=goal_form,
                    progress_form=progress_form,
                ),
                200,
            )
        else:
            flash("Goal not found.", "danger")
            user_id = session["user_id"]
            current_goals = get_current_goals(user_id)
            overdue_goals = get_overdue_goals(user_id)
            goal_history = get_goal_history(user_id, limit=10)
            goal_stats = get_goal_statistics(user_id)
            predefined_goals = get_predefined_goals()
            goal_form = GoalForm()
            progress_form = GoalProgressForm()

            return (
                render_template(
                    "goals/goals.html",
                    current_goals=current_goals,
                    overdue_goals=overdue_goals,
                    goal_history=goal_history,
                    goal_stats=goal_stats,
                    predefined_goals=predefined_goals,
                    categories=GoalCategory,
                    goal_form=goal_form,
                    progress_form=progress_form,
                ),
                404,
            )
    except Exception as e:
        flash("An error occurred while failing your goal.", "danger")
        user_id = session["user_id"]
        current_goals = get_current_goals(user_id)
        overdue_goals = get_overdue_goals(user_id)
        goal_history = get_goal_history(user_id, limit=10)
        goal_stats = get_goal_statistics(user_id)
        predefined_goals = get_predefined_goals()
        goal_form = GoalForm()
        progress_form = GoalProgressForm()

        return (
            render_template(
                "goals/goals.html",
                current_goals=current_goals,
                overdue_goals=overdue_goals,
                goal_history=goal_history,
                goal_stats=goal_stats,
                predefined_goals=predefined_goals,
                categories=GoalCategory,
                goal_form=goal_form,
                progress_form=progress_form,
            ),
            500,
        )


@goals_bp.route("/api/goals/suggestions/<category>")
def get_goal_suggestions(category: str) -> Tuple[Response, int]:
    """Get goal suggestions for a specific category.
    
    Args:
        category: The goal category to get suggestions for.
        
    Returns:
        JSON response with goal suggestions or error.
    """
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        predefined_goals = get_predefined_goals()
        category_enum = GoalCategory(category)
        suggestions = predefined_goals.get(category_enum, [])

        return jsonify({"suggestions": suggestions})

    except ValueError:
        return jsonify({"suggestions": []}), 400


@goals_bp.route("/api/goals/current")
def get_current_goal_api() -> Union[Tuple[Response, int], Response]:
    """Get current goal data for AJAX requests.
    
    Returns:
        JSON response with current goals data or error.
    """
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session["user_id"]
    current_goals = get_current_goals(user_id)
    goals_data = [
        {
            "id": g.id,
            "title": g.title,
            "category": g.category.value,
            "description": g.description,
            "status": g.status.value,
            "progress_notes": g.progress_notes,
            "days_remaining": g.days_remaining,
            "progress_percentage": g.progress_percentage,
            "week_start": g.week_start.strftime("%Y-%m-%d"),
            "week_end": g.week_end.strftime("%Y-%m-%d"),
        }
        for g in current_goals
    ]
    return jsonify({"goals": goals_data})
