from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date


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

        new_entry = DiaryEntry(
            user_id=user_id,
            content=content,
            rating=rating
        )
        db.session.add(new_entry)
        db.session.commit()
        return redirect("/progress")

    return render_template("diary.html")



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
    return render_template("progress.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True)