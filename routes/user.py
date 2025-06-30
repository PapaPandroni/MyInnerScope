from flask import Blueprint, render_template, session, redirect, url_for, send_file, flash, jsonify, make_response
from models import User, DiaryEntry, Goal, DailyStats, db
import io, csv, json

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login_page'))
    return render_template('settings.html')

@user_bp.route('/download-data/json')
def download_data_json():
    if 'user_id' not in session:
        return redirect(url_for('auth.login_page'))
    user_id = session['user_id']
    user = User.query.get(user_id)
    diary_entries = DiaryEntry.query.filter_by(user_id=user_id).all()
    goals = Goal.query.filter_by(user_id=user_id).all()
    stats = DailyStats.query.filter_by(user_id=user_id).all()
    data = {
        'user': {'email': user.email, 'user_name': user.user_name},
        'diary_entries': [
            {'date': e.entry_date.isoformat(), 'content': e.content, 'rating': e.rating} for e in diary_entries
        ],
        'goals': [
            {
                'title': g.title,
                'category': g.category.value if hasattr(g.category, 'value') else str(g.category),
                'status': g.status.value if hasattr(g.status, 'value') else str(g.status),
                'created_at': g.created_at.isoformat() if g.created_at else None
            } for g in goals
        ],
        'stats': [
            {'date': s.date.isoformat(), 'points': s.points, 'current_streak': s.current_streak, 'longest_streak': s.longest_streak} for s in stats
        ]
    }
    response = make_response(json.dumps(data, indent=2))
    response.headers['Content-Disposition'] = 'attachment; filename=user_data.json'
    response.mimetype = 'application/json'
    return response

@user_bp.route('/download-data/csv')
def download_data_csv():
    if 'user_id' not in session:
        return redirect(url_for('auth.login_page'))
    user_id = session['user_id']
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Diary Entries'])
    writer.writerow(['Date', 'Content', 'Rating'])
    for e in DiaryEntry.query.filter_by(user_id=user_id).all():
        writer.writerow([e.entry_date, e.content, e.rating])
    writer.writerow([])
    writer.writerow(['Goals'])
    writer.writerow(['Title', 'Category', 'Status', 'Created At'])
    for g in Goal.query.filter_by(user_id=user_id).all():
        writer.writerow([g.title, g.category, g.status, g.created_at])
    writer.writerow([])
    writer.writerow(['Stats'])
    writer.writerow(['Date', 'Points', 'Current Streak', 'Longest Streak'])
    for s in DailyStats.query.filter_by(user_id=user_id).all():
        writer.writerow([s.date, s.points, s.current_streak, s.longest_streak])
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=user_data.csv'
    response.mimetype = 'text/csv'
    return response

@user_bp.route('/delete-account', methods=['GET', 'POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('auth.login_page'))
    # Placeholder: show confirmation UI, no delete logic yet
    if 'POST' == 'POST':
        flash('Account deletion is not yet implemented.', 'warning')
    return render_template('delete_account_placeholder.html') 