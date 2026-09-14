from flask import Flask, redirect, resp, request, url_for, send_from_directory, send_file
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user

app = Flask(__name__)
app.secret_key = "dev-only-change-me"

login_manager = LoginManager(app)
login_manager.login_view = "login"

users = {}  # Pure skill, We don't need no DB for logins

class User(UserMixin):
    def __init__(self, username):
        self.id = username

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


# Everything under /public/* is intentionally unauthenticated.
@app.route("/public/<path:path>")
def public(path):
    return send_from_directory("public", path)


if __name__ == "__main__":
    app.run(debug=True)

