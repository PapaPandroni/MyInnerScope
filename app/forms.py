"""
Flask-WTF form classes for Aim for the Stars application
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange
from .models.goal import GoalCategory
import re

class LoginForm(FlaskForm):
    """Form for user login"""
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required')
    ])

class RegisterForm(FlaskForm):
    """Form for user registration"""
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address'),
        Length(max=120, message='Email must be less than 120 characters')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    password_again = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ])
    user_name = StringField('Display Name (Optional)', validators=[
        Length(max=200, message='Display name must be less than 200 characters')
    ])

    def validate_password(self, password):
        """Custom validation for password strength"""
        if password.data:
            # Check for mixed case
            if not re.search(r'[A-Z]', password.data):
                raise ValidationError('Password must contain at least one uppercase letter')
            if not re.search(r'[a-z]', password.data):
                raise ValidationError('Password must contain at least one lowercase letter')

class DiaryEntryForm(FlaskForm):
    """Form for diary entry creation"""
    content = TextAreaField('Diary Entry', validators=[
        DataRequired(message='Diary entry content is required'),
        Length(min=1, max=2000, message='Diary entry must be between 1 and 2000 characters')
    ])
    rating = IntegerField('Rating', validators=[
        NumberRange(min=-1, max=1, message='Rating must be either -1 (want to change) or 1 (encouraged)')
    ])

    def validate_rating(self, field):
        if field.data not in [-1, 1]:
            raise ValidationError('Rating must be either -1 (want to change) or 1 (encouraged)')

class GoalForm(FlaskForm):
    """Form for goal creation"""
    category = SelectField('Category', validators=[
        DataRequired(message='Please select a goal category')
    ], choices=[
        (category.value, category.value) for category in GoalCategory
    ])
    title = StringField('Goal Title', validators=[
        DataRequired(message='Goal title is required'),
        Length(min=1, max=200, message='Goal title must be between 1 and 200 characters')
    ])
    description = TextAreaField('Description (Optional)', validators=[
        Length(max=1000, message='Description must be less than 1000 characters')
    ])

class GoalProgressForm(FlaskForm):
    """Form for updating goal progress"""
    progress_notes = TextAreaField('Progress Notes', validators=[
        Length(max=1000, message='Progress notes must be less than 1000 characters')
    ])

class DeleteAccountForm(FlaskForm):
    """Form for confirming account deletion"""
    password = PasswordField('Password', validators=[
        DataRequired(message='Please enter your password to confirm deletion')
    ])
    submit = SubmitField('Delete My Account Permanently') 