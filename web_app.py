from flask import Flask, render_template
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

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True)