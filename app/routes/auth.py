from typing import Union
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    flash,
    url_for,
    current_app,
    Response,
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.wrappers import Response as WerkzeugResponse
from datetime import date, datetime, timezone
from ..models import User, DailyStats, PointsLog, db
from ..models.points_log import PointsSourceType
from ..utils.points_service import award_login_bonus
from ..forms import LoginForm, RegisterForm

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login_page() -> Union[str, tuple[str, int], WerkzeugResponse]:
    """Handle user login with email and password.
    
    Returns:
        Rendered login template or redirect to diary page.
    """
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Try to find a user with that email
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Invalid email or password.", "danger")
            current_app.logger.warning(f"Failed login attempt.")
            return render_template("auth/login.html", form=form), 401

        # Success! Session!
        session["user_id"] = user.id
        current_app.logger.info(f"User {email} logged in successfully.")

        # Award daily login bonus if not already awarded today
        today = datetime.now(timezone.utc).date()
        existing_login_bonus = PointsLog.query.filter_by(
            user_id=user.id,
            date=today,
            source_type=PointsSourceType.DAILY_LOGIN.value
        ).first()

        if not existing_login_bonus:
            award_login_bonus(user.id)

        return redirect("/diary")

    # If GET request or validation fails, show login form
    return render_template("auth/login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register() -> Union[str, tuple[str, int], WerkzeugResponse]:
    """Handle user registration with validation.
    
    Returns:
        Rendered registration template or redirect to login page.
    """
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        password_again = form.password_again.data
        user_name = form.user_name.data or None

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "danger")
            current_app.logger.warning(
                f"Registration attempt with existing email: {email}"
            )
            return render_template("auth/register.html", form=form), 400

        # Create user with automatic password hashing
        new_user = User(email=email, password=password, user_name=user_name)

        db.session.add(new_user)
        db.session.commit()
        current_app.logger.info(f"New user registered: {email}")
        flash("Registration successful! Please log in.", "success")
        return redirect("/login")

    # If GET request or validation fails, show registration form
    return render_template("auth/register.html", form=form)


@auth_bp.route("/logout")
def logout() -> WerkzeugResponse:
    """Log out the current user and clear session.
    
    Returns:
        Redirect to home page.
    """
    user_id = session.get("user_id")
    if user_id:
        user = db.session.get(User, user_id)
        if user:
            current_app.logger.info(f"User {user.email} logged out.")
    session.clear()
    flash("You have been logged out.", "info")
    return redirect("/")
