import pytest
from flask import url_for, session
from app.models import User, DiaryEntry, Goal, DailyStats, db
from datetime import datetime


def test_delete_account_get(client, app):
    with app.app_context():
        # Create a test user
        user = User(email='test@example.com', password='password', user_name='TestUser')
        db.session.add(user)
        db.session.commit()

        # Log in the user
        with client.session_transaction() as sess:
            sess['user_id'] = user.id

        response = client.get(url_for('user.delete_account'))
        assert response.status_code == 200
        assert b'Delete Account' in response.data
        assert b'To confirm, please re-enter your password:' in response.data

def test_delete_account_post_success(client, app):
    with app.app_context():
        # Create a test user and associated data
        user = User(email='delete@example.com', password='password', user_name='DeleteUser')
        db.session.add(user)
        db.session.commit()

        diary_entry = DiaryEntry(user_id=user.id, content='Test entry', rating=1)
        goal = Goal(user_id=user.id, title='Test Goal', category='Health', week_start=datetime.utcnow().date(), week_end=datetime.utcnow().date())
        daily_stats = DailyStats(user_id=user.id, date=datetime.utcnow().date(), points=10, current_streak=1, longest_streak=1)
        db.session.add_all([diary_entry, goal, daily_stats])
        db.session.commit()

        # Log in the user
        with client.session_transaction() as sess:
            sess['user_id'] = user.id

        response = client.post(url_for('user.delete_account'), data={'password': 'password'})
        assert response.status_code == 302  # Redirect after successful deletion
        assert url_for('auth.login_page') in response.headers['Location']

        # Verify user and associated data are deleted
        assert db.session.get(User, user.id) is None
        assert DiaryEntry.query.filter_by(user_id=user.id).first() is None
        assert Goal.query.filter_by(user_id=user.id).first() is None
        assert DailyStats.query.filter_by(user_id=user.id).first() is None

        # Verify session is cleared
        with client.session_transaction() as sess:
            assert 'user_id' not in sess

def test_delete_account_post_wrong_password(client, app):
    with app.app_context():
        # Create a test user
        user = User(email='wrongpass@example.com', password='password', user_name='WrongPassUser')
        db.session.add(user)
        db.session.commit()

        # Log in the user
        with client.session_transaction() as sess:
            sess['user_id'] = user.id

        response = client.post(url_for('user.delete_account'), data={'password': 'wrong_password'})
        assert response.status_code == 200  # Should re-render the page with an error
        assert b'Incorrect password. Please try again.' in response.data
        
        # Verify user is not deleted
        assert db.session.get(User, user.id) is not None

def test_delete_account_not_logged_in(client, app):
    response = client.get(url_for('user.delete_account'))
    assert response.status_code == 302
    assert url_for('auth.login_page') in response.headers['Location']

    response = client.post(url_for('user.delete_account'), data={'password': 'password'})
    assert response.status_code == 302
    assert url_for('auth.login_page') in response.headers['Location']
