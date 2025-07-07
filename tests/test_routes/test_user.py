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


# New tests for profile functionality

def test_profile_page_get(client, app):
    """Test accessing the profile page when logged in"""
    with app.app_context():
        # Create a test user
        user = User(email='profile@example.com', password='password', user_name='ProfileUser')
        db.session.add(user)
        db.session.commit()

        # Log in the user
        with client.session_transaction() as sess:
            sess['user_id'] = user.id

        response = client.get(url_for('user.profile'))
        assert response.status_code == 200
        assert b"Captain's Cabin" in response.data
        assert b'Profile Settings' in response.data
        assert b'ProfileUser' in response.data  # Current username should be displayed

def test_profile_page_not_logged_in(client, app):
    """Test accessing profile page when not logged in"""
    response = client.get(url_for('user.profile'))
    assert response.status_code == 302
    assert url_for('auth.login_page') in response.headers['Location']

def test_change_username_success(client, app):
    """Test successful username change"""
    with app.app_context():
        # Create a test user
        user = User(email='username@example.com', password='password', user_name='OldUsername')
        db.session.add(user)
        db.session.commit()

        # Log in the user
        with client.session_transaction() as sess:
            sess['user_id'] = user.id

        # Get CSRF token
        response = client.get(url_for('user.profile'))
        csrf_token = None
        if b'csrf-token' in response.data:
            import re
            match = re.search(b'<meta[^>]*name="csrf-token"[^>]*content="([^"]+)"', response.data)
            if match:
                csrf_token = match.group(1).decode('utf-8')

        # Change username
        data = {'new_username': 'NewUsername', 'submit': 'Change Username'}
        if csrf_token:
            data['csrf_token'] = csrf_token

        response = client.post(url_for('user.change_username'), data=data)
        assert response.status_code == 302  # Redirect after success
        assert url_for('user.profile') in response.headers['Location']

        # Verify username was updated in database
        db.session.refresh(user)
        assert user.user_name == 'NewUsername'

def test_change_username_empty(client, app):
    """Test username change with empty username"""
    with app.app_context():
        user = User(email='empty@example.com', password='password', user_name='TestUser')
        db.session.add(user)
        db.session.commit()

        with client.session_transaction() as sess:
            sess['user_id'] = user.id

        # Get CSRF token
        response = client.get(url_for('user.profile'))
        csrf_token = None
        if b'csrf-token' in response.data:
            import re
            match = re.search(b'<meta[^>]*name="csrf-token"[^>]*content="([^"]+)"', response.data)
            if match:
                csrf_token = match.group(1).decode('utf-8')

        # Try to change username with empty value
        data = {'new_username': '', 'submit': 'Change Username'}
        if csrf_token:
            data['csrf_token'] = csrf_token

        response = client.post(url_for('user.change_username'), data=data)
        assert response.status_code == 302  # Redirect with validation error

        # Verify username was not changed
        db.session.refresh(user)
        assert user.user_name == 'TestUser'

def test_change_username_too_long(client, app):
    """Test username change with too long username"""
    with app.app_context():
        user = User(email='long@example.com', password='password', user_name='TestUser')
        db.session.add(user)
        db.session.commit()

        with client.session_transaction() as sess:
            sess['user_id'] = user.id

        # Get CSRF token
        response = client.get(url_for('user.profile'))
        csrf_token = None
        if b'csrf-token' in response.data:
            import re
            match = re.search(b'<meta[^>]*name="csrf-token"[^>]*content="([^"]+)"', response.data)
            if match:
                csrf_token = match.group(1).decode('utf-8')

        # Try to change username with too long value
        long_username = 'a' * 201  # Exceeds 200 character limit
        data = {'new_username': long_username, 'submit': 'Change Username'}
        if csrf_token:
            data['csrf_token'] = csrf_token

        response = client.post(url_for('user.change_username'), data=data)
        assert response.status_code == 302  # Redirect with validation error

        # Verify username was not changed
        db.session.refresh(user)
        assert user.user_name == 'TestUser'

def test_change_username_not_logged_in(client, app):
    """Test username change when not logged in"""
    response = client.post(url_for('user.change_username'), data={'new_username': 'NewUsername'})
    assert response.status_code == 302
    assert url_for('auth.login_page') in response.headers['Location']

def test_change_password_success(client, app):
    """Test successful password change"""
    with app.app_context():
        user = User(email='password@example.com', password='OldPassword123', user_name='PasswordUser')
        db.session.add(user)
        db.session.commit()

        with client.session_transaction() as sess:
            sess['user_id'] = user.id

        # Get CSRF token
        response = client.get(url_for('user.profile'))
        csrf_token = None
        if b'csrf-token' in response.data:
            import re
            match = re.search(b'<meta[^>]*name="csrf-token"[^>]*content="([^"]+)"', response.data)
            if match:
                csrf_token = match.group(1).decode('utf-8')

        # Change password
        data = {
            'current_password': 'OldPassword123',
            'new_password': 'NewPassword123',
            'confirm_password': 'NewPassword123',
            'submit': 'Change Password'
        }
        if csrf_token:
            data['csrf_token'] = csrf_token

        response = client.post(url_for('user.change_password'), data=data)
        assert response.status_code == 302  # Redirect after success
        assert url_for('user.profile') in response.headers['Location']

        # Verify password was updated
        db.session.refresh(user)
        assert user.check_password('NewPassword123')
        assert not user.check_password('OldPassword123')

def test_change_password_wrong_current_password(client, app):
    """Test password change with wrong current password"""
    with app.app_context():
        user = User(email='wrongpass@example.com', password='CorrectPassword123', user_name='WrongPassUser')
        db.session.add(user)
        db.session.commit()

        with client.session_transaction() as sess:
            sess['user_id'] = user.id

        # Get CSRF token
        response = client.get(url_for('user.profile'))
        csrf_token = None
        if b'csrf-token' in response.data:
            import re
            match = re.search(b'<meta[^>]*name="csrf-token"[^>]*content="([^"]+)"', response.data)
            if match:
                csrf_token = match.group(1).decode('utf-8')

        # Try to change password with wrong current password
        data = {
            'current_password': 'WrongPassword123',
            'new_password': 'NewPassword123',
            'confirm_password': 'NewPassword123',
            'submit': 'Change Password'
        }
        if csrf_token:
            data['csrf_token'] = csrf_token

        response = client.post(url_for('user.change_password'), data=data)
        assert response.status_code == 302  # Redirect with error

        # Verify password was not changed
        db.session.refresh(user)
        assert user.check_password('CorrectPassword123')
        assert not user.check_password('NewPassword123')

def test_change_password_weak_password(client, app):
    """Test password change with weak password"""
    with app.app_context():
        user = User(email='weak@example.com', password='OldPassword123', user_name='WeakPassUser')
        db.session.add(user)
        db.session.commit()

        with client.session_transaction() as sess:
            sess['user_id'] = user.id

        # Get CSRF token
        response = client.get(url_for('user.profile'))
        csrf_token = None
        if b'csrf-token' in response.data:
            import re
            match = re.search(b'<meta[^>]*name="csrf-token"[^>]*content="([^"]+)"', response.data)
            if match:
                csrf_token = match.group(1).decode('utf-8')

        # Try to change password with weak password (no uppercase)
        data = {
            'current_password': 'OldPassword123',
            'new_password': 'weakpassword123',
            'confirm_password': 'weakpassword123',
            'submit': 'Change Password'
        }
        if csrf_token:
            data['csrf_token'] = csrf_token

        response = client.post(url_for('user.change_password'), data=data)
        assert response.status_code == 302  # Redirect with validation error

        # Verify password was not changed
        db.session.refresh(user)
        assert user.check_password('OldPassword123')

def test_change_password_mismatch(client, app):
    """Test password change with mismatched confirmation"""
    with app.app_context():
        user = User(email='mismatch@example.com', password='OldPassword123', user_name='MismatchUser')
        db.session.add(user)
        db.session.commit()

        with client.session_transaction() as sess:
            sess['user_id'] = user.id

        # Get CSRF token
        response = client.get(url_for('user.profile'))
        csrf_token = None
        if b'csrf-token' in response.data:
            import re
            match = re.search(b'<meta[^>]*name="csrf-token"[^>]*content="([^"]+)"', response.data)
            if match:
                csrf_token = match.group(1).decode('utf-8')

        # Try to change password with mismatched confirmation
        data = {
            'current_password': 'OldPassword123',
            'new_password': 'NewPassword123',
            'confirm_password': 'DifferentPassword123',
            'submit': 'Change Password'
        }
        if csrf_token:
            data['csrf_token'] = csrf_token

        response = client.post(url_for('user.change_password'), data=data)
        assert response.status_code == 302  # Redirect with validation error

        # Verify password was not changed
        db.session.refresh(user)
        assert user.check_password('OldPassword123')

def test_change_password_not_logged_in(client, app):
    """Test password change when not logged in"""
    response = client.post(url_for('user.change_password'), data={
        'current_password': 'OldPassword123',
        'new_password': 'NewPassword123',
        'confirm_password': 'NewPassword123'
    })
    assert response.status_code == 302
    assert url_for('auth.login_page') in response.headers['Location']

def test_profile_page_with_no_username(client, app):
    """Test profile page when user has no username set"""
    with app.app_context():
        user = User(email='nousername@example.com', password='password')  # No user_name
        db.session.add(user)
        db.session.commit()

        with client.session_transaction() as sess:
            sess['user_id'] = user.id

        response = client.get(url_for('user.profile'))
        assert response.status_code == 200
        assert b'Not set' in response.data  # Should show "Not set" for empty username
