from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

import requests
from helpers import login_required, city_check

# Configure application
app = Flask(__name__)
app.config["DEBUG"] = False

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Permanent session


@app.before_request
def make_session_permanent():
    session.permanent = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///weather.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    cities = db.execute("SELECT city  FROM cities WHERE user_id = ? GROUP BY city ORDER BY id DESC", user_id)

    weather_data = []

    for city in cities:
        url = "https://api.openweathermap.org/data/2.5/weather?q=" + city["city"] + "&appid=48f750b4ba7b9b8f2db9ed909f8ac51c"
        data = requests.get(url).json()
        weather = {
            'city': city["city"],
            'temp': round(data['main']['temp'] - 273),
            'des': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'humidity': data['main']['humidity'],
            'feels': round(data['main']['feels_like'] - 273),
            'wind': round(data['wind']['speed']*3.6)
        }

        weather_data.append(weather)

    return render_template("index.html", weather_data=weather_data)

# Login


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("⚠ Must provide username")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("⚠ Must provide password")
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("⚠ Invalid username or password")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# Register


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # When user clicked register
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username:
            flash("⚠ Must provide username")
            return render_template("register.html")

        if not password or not confirmation:
            flash("⚠ Must provide password")
            return render_template("register.html")

        if password != confirmation:
            flash("⚠ Password don't match")
            return render_template("register.html")

        # When everything is ok
        hash = generate_password_hash(password)
        try:
            user = db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", username, hash)
        except:
            flash("⚠ Username already exists")
            return redirect("/register")

        session["user_id"] = user
        return redirect("/")

    # When method is get
    else:
        return render_template("register.html")

# Logout


@app.route("/logout")
@login_required
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# Add_city

@app.route("/add_city", methods=["POST"])
@login_required
def add_city():

    id = session["user_id"]
    city = request.form.get("city_name")

    # If city in empty
    if not city:
        flash("⚠ Invalid city")
        return redirect("/")

    if not city.isalpha():
        flash("⚠ Invalid city")
        return redirect("/")

    check_city = city_check(city)

    # If city don't exisy
    if not check_city:
        flash("⚠ Invalid city")
        return redirect("/")

    # OK
    db.execute("INSERT INTO cities(city,user_id) VALUES(?, ?)", city.upper(), id)
    return redirect("/")


@app.route("/delete/<string:city>")
@login_required
def delete(city):
    user_id = session["user_id"]
    db.execute("DELETE FROM cities WHERE user_id = ? AND city = ?", user_id, city)
    return redirect("/")


@app.route("/contact")
@login_required
def contact():
    return render_template("contact.html")