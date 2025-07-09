import unittest
from flask import Flask
from flask_wtf import CSRFProtect
from app.forms import (
    LoginForm,
    RegisterForm,
    DiaryEntryForm,
    GoalForm,
    GoalProgressForm,
    DeleteAccountForm,
    ChangeUsernameForm,
    ChangePasswordForm,
)
from app.models.goal import GoalCategory
from wtforms.validators import ValidationError


class TestForms(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = "testing"
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.client = self.app.test_client()

    def test_login_form_valid(self):
        with self.app.test_request_context():
            form = LoginForm(email="test@example.com", password="password")
            self.assertTrue(form.validate())

    def test_login_form_invalid_email(self):
        with self.app.test_request_context():
            form = LoginForm(email="invalid-email", password="password")
            self.assertFalse(form.validate())

    def test_register_form_valid(self):
        with self.app.test_request_context():
            form = RegisterForm(
                email="test@example.com",
                password="Password1",
                password_again="Password1",
            )
            self.assertTrue(form.validate())

    def test_register_form_password_mismatch(self):
        with self.app.test_request_context():
            form = RegisterForm(
                email="test@example.com",
                password="Password1",
                password_again="Password2",
            )
            self.assertFalse(form.validate())

    def test_diary_entry_form_valid(self):
        with self.app.test_request_context():
            form = DiaryEntryForm(content="This is a diary entry.", rating=1)
            self.assertTrue(form.validate())

    def test_diary_entry_form_invalid_rating(self):
        with self.app.test_request_context():
            form = DiaryEntryForm(content="This is a diary entry.", rating=2)
            self.assertFalse(form.validate())

    def test_goal_form_valid(self):
        with self.app.test_request_context():
            form = GoalForm()
            form.category.choices = [(c.value, c.value) for c in GoalCategory]
            form.category.data = "Exercise & Fitness"
            form.title.data = "Run a marathon"
            self.assertTrue(form.validate())

    def test_goal_progress_form_valid(self):
        with self.app.test_request_context():
            form = GoalProgressForm(progress_notes="I ran 10 miles today.")
            self.assertTrue(form.validate())

    def test_delete_account_form_valid(self):
        with self.app.test_request_context():
            form = DeleteAccountForm(password="password")
            self.assertTrue(form.validate())

    # New tests for profile forms

    def test_change_username_form_valid(self):
        with self.app.test_request_context():
            form = ChangeUsernameForm(new_username="NewUsername")
            self.assertTrue(form.validate())

    def test_change_username_form_empty(self):
        with self.app.test_request_context():
            form = ChangeUsernameForm(new_username="")
            self.assertFalse(form.validate())
            self.assertIn("Username is required", str(form.errors))

    def test_change_username_form_too_long(self):
        with self.app.test_request_context():
            long_username = "a" * 201  # Exceeds 200 character limit
            form = ChangeUsernameForm(new_username=long_username)
            self.assertFalse(form.validate())
            self.assertIn(
                "Username must be between 1 and 200 characters", str(form.errors)
            )

    def test_change_password_form_valid(self):
        with self.app.test_request_context():
            form = ChangePasswordForm(
                current_password="OldPassword123",
                new_password="NewPassword123",
                confirm_password="NewPassword123",
            )
            self.assertTrue(form.validate())

    def test_change_password_form_missing_current_password(self):
        with self.app.test_request_context():
            form = ChangePasswordForm(
                current_password="",
                new_password="NewPassword123",
                confirm_password="NewPassword123",
            )
            self.assertFalse(form.validate())
            self.assertIn("Current password is required", str(form.errors))

    def test_change_password_form_missing_new_password(self):
        with self.app.test_request_context():
            form = ChangePasswordForm(
                current_password="OldPassword123",
                new_password="",
                confirm_password="NewPassword123",
            )
            self.assertFalse(form.validate())
            self.assertIn("New password is required", str(form.errors))

    def test_change_password_form_password_mismatch(self):
        with self.app.test_request_context():
            form = ChangePasswordForm(
                current_password="OldPassword123",
                new_password="NewPassword123",
                confirm_password="DifferentPassword123",
            )
            self.assertFalse(form.validate())
            self.assertIn("Passwords must match", str(form.errors))

    def test_change_password_form_weak_password_no_uppercase(self):
        with self.app.test_request_context():
            form = ChangePasswordForm(
                current_password="OldPassword123",
                new_password="weakpassword123",
                confirm_password="weakpassword123",
            )
            self.assertFalse(form.validate())
            self.assertIn(
                "Password must contain at least one uppercase letter", str(form.errors)
            )

    def test_change_password_form_weak_password_no_lowercase(self):
        with self.app.test_request_context():
            form = ChangePasswordForm(
                current_password="OldPassword123",
                new_password="WEAKPASSWORD123",
                confirm_password="WEAKPASSWORD123",
            )
            self.assertFalse(form.validate())
            self.assertIn(
                "Password must contain at least one lowercase letter", str(form.errors)
            )

    def test_change_password_form_short_password(self):
        with self.app.test_request_context():
            form = ChangePasswordForm(
                current_password="OldPassword123",
                new_password="Short1",
                confirm_password="Short1",
            )
            self.assertFalse(form.validate())
            self.assertIn(
                "Password must be at least 8 characters long", str(form.errors)
            )


if __name__ == "__main__":
    unittest.main()
