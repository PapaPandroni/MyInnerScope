from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, timedelta


app = Flask(__name__)
app.secret_key = "AgjkAGaoi)&%!909!)!?#=9751"

# Tell Flask where the database is
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Creates users.db in your folder
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids warning

# Connect SQLAlchemy to your app
db = SQLAlchemy(app)

# Define a User model (a table)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Auto-increment ID
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    user_name = db.Column(db.String(200), nullable = True)

from datetime import date  # add this at the top if it's not there already

class DiaryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    entry_date = db.Column(db.Date, default=date.today, nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref='entries')


@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/diary", methods=["GET", "POST"])
def diary_entry():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        content = request.form["content"]
        rating = int(request.form["rating"])
        user_id = session["user_id"]
        today = date.today()

        # Check if DailyStats exists for today
        stats = DailyStats.query.filter_by(user_id=user_id, date=today).first()

        if stats is None or (stats.current_streak == 0 and not DiaryEntry.query.filter_by(user_id=user_id, entry_date=today).first()):

            # Check if user had an entry yesterday
            yesterday = today - timedelta(days=1)
            yesterdays_stats = DailyStats.query.filter_by(user_id=user_id, date=yesterday).first()
            
            # Start a new streak or continue it
            if yesterdays_stats and yesterdays_stats.current_streak > 0:
                new_streak = yesterdays_stats.current_streak + 1
            else:
                new_streak = 1

            # Create today's stats entry
            stats = DailyStats(
                user_id=user_id,
                date=today,
                current_streak=new_streak,
                longest_streak=new_streak,  # May be overwritten below
                points=0  # We'll add below
            )

            # Check and update longest streak
            longest = DailyStats.query.filter_by(user_id=user_id).order_by(DailyStats.longest_streak.desc()).first()
            if longest and longest.longest_streak > new_streak:
                stats.longest_streak = longest.longest_streak

            db.session.add(stats)

        # Add points based on rating
        if rating == 1:
            stats.points += 5
        elif rating == -1:
            stats.points += 2

        # Save diary entry
        new_entry = DiaryEntry(
            user_id=user_id,
            content=content,
            rating=rating
        )
        db.session.add(new_entry)
        db.session.commit()

        return redirect("/diary")

    return render_template("diary.html")


class DailyStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)

    points = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)

    user = db.relationship('User', backref='daily_stats')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'date', name='user_date_uc'),
    )


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Try to find a user with that email
        user = User.query.filter_by(email=email).first()

        if not user:
            return "No user found with that email."

        if not check_password_hash(user.password, password):
            return "Incorrect password."


        # Success! Session!
        session["user_id"] = user.id

        # Inside login route, after login is successful
        today = date.today()
        user_id = user.id

        stats = DailyStats.query.filter_by(user_id=user_id, date=today).first()

        if not stats:
            stats = DailyStats(user_id=user_id, date=today, points=1)
            db.session.add(stats)
            db.session.commit()

        return redirect("/diary")


    # If GET request, show login form
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        password_again = request.form["password_again"]
        user_name = request.form.get("user_name", None)

        if password != password_again:
            return "Passwords do not match!"

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            return "Email already registered."

        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password, user_name=user_name)

        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")

    return render_template("register.html")

@app.route("/progress")
def progress():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    today = date.today()

    # Today's stats
    stats_today = DailyStats.query.filter_by(user_id=user_id, date=today).first()
    points_today = stats_today.points if stats_today else 0

    # All-time total points
    total_points = db.session.query(db.func.sum(DailyStats.points))\
        .filter_by(user_id=user_id).scalar() or 0

    # Most recent current streak
    current_streak_row = DailyStats.query.filter_by(user_id=user_id)\
        .order_by(DailyStats.date.desc()).first()
    current_streak = current_streak_row.current_streak if current_streak_row else 0

    # All-time longest streak
    longest_streak_row = DailyStats.query.filter_by(user_id=user_id)\
        .order_by(DailyStats.longest_streak.desc()).first()
    longest_streak = longest_streak_row.longest_streak if longest_streak_row else 0
    
    # All time numnber of entries
    total_entries = DiaryEntry.query.filter_by(user_id=user_id).count()

    return render_template(
        "progress.html",
        points_today=points_today,
        total_points=total_points,
        current_streak=current_streak,
        longest_streak=longest_streak,
        total_entries=total_entries
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True)