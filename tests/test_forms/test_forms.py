
import unittest
from flask import Flask
from flask_wtf import CSRFProtect
from forms import LoginForm, RegisterForm, DiaryEntryForm, GoalForm, GoalProgressForm, DeleteAccountForm
from models.goal import GoalCategory
from wtforms.validators import ValidationError

class TestForms(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'testing'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()

    def test_login_form_valid(self):
        with self.app.test_request_context():
            form = LoginForm(email='test@example.com', password='password')
            self.assertTrue(form.validate())

    def test_login_form_invalid_email(self):
        with self.app.test_request_context():
            form = LoginForm(email='invalid-email', password='password')
            self.assertFalse(form.validate())

    def test_register_form_valid(self):
        with self.app.test_request_context():
            form = RegisterForm(email='test@example.com', password='Password1', password_again='Password1')
            self.assertTrue(form.validate())

    def test_register_form_password_mismatch(self):
        with self.app.test_request_context():
            form = RegisterForm(email='test@example.com', password='Password1', password_again='Password2')
            self.assertFalse(form.validate())

    def test_diary_entry_form_valid(self):
        with self.app.test_request_context():
            form = DiaryEntryForm(content='This is a diary entry.', rating=1)
            self.assertTrue(form.validate())

    def test_diary_entry_form_invalid_rating(self):
        with self.app.test_request_context():
            form = DiaryEntryForm(content='This is a diary entry.', rating=2)
            self.assertFalse(form.validate())

    def test_goal_form_valid(self):
        with self.app.test_request_context():
            form = GoalForm()
            form.category.choices = [(c.value, c.value) for c in GoalCategory]
            form.category.data = 'Exercise & Fitness'
            form.title.data = 'Run a marathon'
            self.assertTrue(form.validate())

    def test_goal_progress_form_valid(self):
        with self.app.test_request_context():
            form = GoalProgressForm(progress_notes='I ran 10 miles today.')
            self.assertTrue(form.validate())

    def test_delete_account_form_valid(self):
        with self.app.test_request_context():
            form = DeleteAccountForm(password='password')
            self.assertTrue(form.validate())

if __name__ == '__main__':
    unittest.main()
