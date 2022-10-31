import requests
from flask import redirect, session
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Check for valid city


def city_check(city):
    try:
        url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=48f750b4ba7b9b8f2db9ed909f8ac51c"
        r = requests.get(url).json()
        temp = round(r['main']['temp'] - 273)
        if temp:
            return True
        return False
    except:
        return False