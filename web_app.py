from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/diary")
def diary_entry():
    return render_template("diary.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)