from flask import Flask, redirect, request, url_for, send_from_directory, send_file
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
import json

app = Flask(__name__)
app.secret_key = "dev-only-change-me"

login_manager = LoginManager(app)
login_manager.login_view = "login"

users = {}  # Pure skill, We don't need no DB for logins

global blasters
blasters = {}

DEFAULT_POINTS = 10

def reset():
    global blasters
    blasters = {}

    with open("private/arsenal.json", "r") as f:
        arsenal = json.load(f)

    for side in arsenal["blasters"].keys():
        if side in blasters:
            raise LookupError("Why tf does that already exist?!?!")

        blasters[side] = []

        for blaster in arsenal["blasters"][side]:
            blaster["available"] = blaster['max_available']
            blasters[side].append(blaster)


class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.points = DEFAULT_POINTS


@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("landing"))

    if request.method == "POST":
        username = request.form["username"].strip()

        if not username:
            return "Username required", 400

        users.setdefault(username, User(username))
        login_user(users[username])

        return redirect(url_for("dashboard"))

    return send_file("public/html/login.html", "text/html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/")
def landing():
    return send_file("public/html/index.html", "text/html")

@app.route("/dashboard")
@login_required
def dashboard():
    return send_file("public/html/dashboard.html", "text/html")

# User API

@app.route("/points_available")
@login_required
def points_available():
    return {"points": current_user.points}

# Arsenal API
@app.route("/arsenal/<string:side>/blasters")
@login_required
def get_arsenal(side):
    if side not in ("breach", "bunker"):
        return {"error": "Invalid side. Must be 'breach' or 'bunker'"}

    return blasters[side]



# Everything under /public/* is intentionally unauthenticated.
@app.route("/public/<path:path>")
def public(path):
    return send_from_directory("public", path)


if __name__ == "__main__":
    reset()  # Load all the guns and stuff

    app.run(debug=True)

