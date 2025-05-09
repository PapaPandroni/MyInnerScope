from flask import Flask, render_template
from log_in_info import user_info
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html", signed = user_info)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)