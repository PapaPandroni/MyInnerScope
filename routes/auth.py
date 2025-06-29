from flask import Blueprint, render_template, request, redirect, session, flash, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from models import User, DailyStats, db
from forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Try to find a user with that email
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("No user found with that email.", "danger")
            current_app.logger.warning(f"Failed login attempt for email: {email}")
            return render_template("login.html", form=form), 401

        if not check_password_hash(user.password, password):
            flash("Incorrect password.", "danger")
            current_app.logger.warning(f"Incorrect password for user: {email}")
            return render_template("login.html", form=form), 401

        # Success! Session!
        session["user_id"] = user.id
        current_app.logger.info(f"User {email} logged in successfully.")

        # Inside login route, after login is successful
        today = date.today()
        user_id = user.id

        stats = DailyStats.query.filter_by(user_id=user_id, date=today).first()

        if not stats:
            stats = DailyStats(user_id=user_id, date=today, points=1)
            db.session.add(stats)
            db.session.commit()

        return redirect("/diary")

    # If GET request or validation fails, show login form
    return render_template("login.html", form=form)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        password_again = form.password_again.data
        user_name = form.user_name.data or None

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "danger")
            current_app.logger.warning(f"Registration attempt with existing email: {email}")
            return render_template("register.html", form=form), 400

        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password, user_name=user_name)

        db.session.add(new_user)
        db.session.commit()
        current_app.logger.info(f"New user registered: {email}")
        flash("Registration successful! Please log in.", "success")
        return redirect("/login")

    # If GET request or validation fails, show registration form
    return render_template("register.html", form=form)

@auth_bp.route("/logout")
def logout():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            current_app.logger.info(f"User {user.email} logged out.")
    session.clear()
    flash("You have been logged out.", "info")
    return redirect("/")