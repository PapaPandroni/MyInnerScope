from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from models.goal import GoalCategory, GoalStatus
from models import User, DailyStats, db
from utils.goal_helpers import (
    get_current_goals, get_overdue_goals, create_goal, update_goal_progress, 
    complete_goal, fail_goal, get_goal_history, get_goal_stats, get_predefined_goals
)
from forms import GoalForm, GoalProgressForm
from datetime import date

goals_bp = Blueprint('goals', __name__)

@goals_bp.route('/goals')
def goals_page():
    """Main goals page showing current goal and history"""
    if "user_id" not in session:
        return redirect("/login")
    
    user_id = session["user_id"]
    current_goals = get_current_goals(user_id)
    overdue_goals = get_overdue_goals(user_id)
    goal_history = get_goal_history(user_id, limit=10)
    goal_stats = get_goal_stats(user_id)
    predefined_goals = get_predefined_goals()
    goal_form = GoalForm()
    
    return render_template('goals.html', 
                         current_goals=current_goals,
                         overdue_goals=overdue_goals,
                         goal_history=goal_history,
                         goal_stats=goal_stats,
                         predefined_goals=predefined_goals,
                         categories=GoalCategory,
                         goal_form=goal_form)

@goals_bp.route('/goals/create', methods=['POST'])
def create_new_goal():
    """Create a new goal for the current week"""
    if "user_id" not in session:
        return redirect("/login")
    
    form = GoalForm()
    
    if form.validate_on_submit():
        try:
            user_id = session["user_id"]
            category_name = form.category.data
            title = form.title.data.strip()
            description = form.description.data.strip() if form.description.data else None
            
            # Convert category name to enum
            try:
                category = GoalCategory(category_name)
            except ValueError:
                flash('Invalid goal category selected.', 'error')
                return redirect(url_for('goals.goals_page'))
            
            # Create the goal
            goal = create_goal(
                user_id=user_id,
                category=category,
                title=title,
                description=description
            )
            
            flash(f'Goal "{goal.title}" created successfully!', 'success')
            return redirect(url_for('goals.goals_page'))
            
        except Exception as e:
            flash('An error occurred while creating your goal.', 'error')
            return redirect(url_for('goals.goals_page'))
    else:
        # Flash validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(error, 'error')
        return redirect(url_for('goals.goals_page'))

@goals_bp.route('/goals/<int:goal_id>/update', methods=['POST'])
def update_goal(goal_id):
    """Update goal progress notes"""
    if "user_id" not in session:
        return redirect("/login")
    
    form = GoalProgressForm()
    
    if form.validate_on_submit():
        try:
            progress_notes = form.progress_notes.data.strip() if form.progress_notes.data else None
            
            goal = update_goal_progress(goal_id, progress_notes)
            
            if goal:
                flash('Goal progress updated successfully!', 'success')
            else:
                flash('Goal not found.', 'error')
                
            return redirect(url_for('goals.goals_page'))
            
        except Exception as e:
            flash('An error occurred while updating your goal.', 'error')
            return redirect(url_for('goals.goals_page'))
    else:
        # Flash validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(error, 'error')
        return redirect(url_for('goals.goals_page'))

@goals_bp.route('/goals/<int:goal_id>/complete', methods=['POST'])
def mark_goal_complete(goal_id):
    """Mark a goal as completed"""
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
            flash(f'Congratulations! You completed your goal: "{goal.title}" (+10 points)', 'success')
        else:
            flash('Goal not found.', 'error')
            
        return redirect(url_for('goals.goals_page'))
        
    except Exception as e:
        flash('An error occurred while completing your goal.', 'error')
        return redirect(url_for('goals.goals_page'))

@goals_bp.route('/goals/<int:goal_id>/fail', methods=['POST'])
def mark_goal_failed(goal_id):
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
            flash(f'Goal marked as failed: "{goal.title}" (+1 point)', 'warning')
        else:
            flash('Goal not found.', 'error')
        return redirect(url_for('goals.goals_page'))
    except Exception as e:
        flash('An error occurred while failing your goal.', 'error')
        return redirect(url_for('goals.goals_page'))

@goals_bp.route('/api/goals/suggestions/<category>')
def get_goal_suggestions(category):
    """Get goal suggestions for a specific category"""
    if "user_id" not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        predefined_goals = get_predefined_goals()
        category_enum = GoalCategory(category)
        suggestions = predefined_goals.get(category_enum, [])
        
        return jsonify({'suggestions': suggestions})
        
    except ValueError:
        return jsonify({'suggestions': []}), 400

@goals_bp.route('/api/goals/current')
def get_current_goal_api():
    """Get current goal data for AJAX requests"""
    if "user_id" not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_id = session["user_id"]
    current_goals = get_current_goals(user_id)
    goals_data = [
        {
            'id': g.id,
            'title': g.title,
            'category': g.category.value,
            'description': g.description,
            'status': g.status.value,
            'progress_notes': g.progress_notes,
            'days_remaining': g.days_remaining,
            'progress_percentage': g.progress_percentage,
            'week_start': g.week_start.strftime('%Y-%m-%d'),
            'week_end': g.week_end.strftime('%Y-%m-%d')
        }
        for g in current_goals
    ]
    return jsonify({'goals': goals_data}) 