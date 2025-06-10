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

#from datetime import date  # add this at the top if it's not there already

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

        if stats is None:
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
                longest_streak=new_streak,
                points=0
            )

            # Check and update longest streak
            longest = DailyStats.query.filter_by(user_id=user_id).order_by(DailyStats.longest_streak.desc()).first()
            if longest and longest.longest_streak > new_streak:
                stats.longest_streak = longest.longest_streak

            db.session.add(stats)

        elif stats.current_streak == 0:
            # This row was created by login, now update streaks
            yesterday = today - timedelta(days=1)
            yesterdays_stats = DailyStats.query.filter_by(user_id=user_id, date=yesterday).first()
    
            if yesterdays_stats and yesterdays_stats.current_streak > 0:
                stats.current_streak = yesterdays_stats.current_streak + 1
            else:
                stats.current_streak = 1

            # Update longest streak if needed
            if stats.current_streak > stats.longest_streak:
                stats.longest_streak = stats.current_streak


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

        # Fetch points for graph (list of (date, points))
    raw_data = DailyStats.query \
        .filter_by(user_id=user_id) \
        .order_by(DailyStats.date) \
        .with_entities(DailyStats.date, DailyStats.points) \
        .all()

    cumulative_points = 0
    cumulative_data = []
    for row in raw_data:
        cumulative_points += row.points
        cumulative_data.append([str(row.date), cumulative_points])

    
    points_data = cumulative_data

        # Top 5 days with most points (including their diary entries)
    top_days = db.session.query(DailyStats)\
        .filter_by(user_id=user_id)\
        .filter(DailyStats.points > 0)\
        .order_by(DailyStats.points.desc())\
        .limit(3)\
        .all()

    # For each top day, get all diary entries
    top_days_with_entries = []
    for day in top_days:
        entries = DiaryEntry.query.filter_by(user_id=user_id, entry_date=day.date).all()
        top_days_with_entries.append({
            'date': day.date,
            'points': day.points,
            'entries': entries
        })

    import random
    from datetime import datetime

    # Get average points per day of the week
    day_analysis = db.session.query(
        db.func.strftime('%w', DailyStats.date).label('weekday'),
        db.func.avg(DailyStats.points).label('avg_points'),
        db.func.count(DailyStats.id).label('entry_count')
    ).filter_by(user_id=user_id)\
    .filter(DailyStats.points > 0)\
    .group_by(db.func.strftime('%w', DailyStats.date))\
    .having(db.func.count(DailyStats.id) >= 2)\
    .all()

    # Convert to list and find best/worst days
    weekday_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    best_day_text = None
    worst_day_text = None

    if len(day_analysis) >= 2:  # Need at least 2 different days to compare
        best_day = max(day_analysis, key=lambda x: x.avg_points)
        worst_day = min(day_analysis, key=lambda x: x.avg_points)
        
        best_day_name = weekday_names[int(best_day.weekday)]
        worst_day_name = weekday_names[int(worst_day.weekday)]
        
        # Random messages for best days
        best_messages = [
            f"{best_day_name}s are your power days!",
            f"You're crushing it on {best_day_name}s!",
            f"{best_day_name}s bring out your best!",
            f"{best_day_name} motivation is on fire!",
            f"You own {best_day_name}s!"
        ]
        
        # Random messages for worst days
        worst_messages = [
            f"{worst_day_name}s seem tough for you",
            f"{worst_day_name}s could use some attention",
            f"{worst_day_name} motivation needs a boost",
            f"Consider planning something special for {worst_day_name}s",
            f"{worst_day_name}s are your growth opportunity"
        ]
        
        best_day_text = random.choice(best_messages)
        worst_day_text = random.choice(worst_messages)



    return render_template(
        "progress.html",
        points_today=points_today,
        total_points=total_points,
        current_streak=current_streak,
        longest_streak=longest_streak,
        total_entries=total_entries,
        points_data=points_data,
        top_days=top_days_with_entries,
        best_day_text=best_day_text,      
        worst_day_text=worst_day_text  
    )



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True)