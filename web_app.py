from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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



@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/diary")
def diary_entry():
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

        if user.password != password:
            return "Incorrect password."

        # Success! You could later set a session here.
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

        new_user = User(email=email, password=password, user_name=user_name)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")

    return render_template("register.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True)