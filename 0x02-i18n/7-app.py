#!/usr/bin/env python3
"""
A simple Flask app that simulates user login and internationalization with time zone handling.
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
import pytz
from pytz import timezone, exceptions

# Mock database of users
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

class Config:
    """
    Config class for setting up language and timezone configurations for the app.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app = Flask(__name__)
# Load the configuration from Config class
app.config.from_object(Config)

# Instantiate Babel
babel = Babel(app)

def get_user():
    """
    Get the user dictionary based on the `login_as` URL parameter.
    If `login_as` is not provided or the ID is invalid, return None.
    """
    user_id = request.args.get('login_as', type=int)
    if user_id is not None and user_id in users:
        return users[user_id]
    return None

@app.before_request
def before_request():
    """
    Before each request, get the user from the `login_as` parameter.
    Store the user in the `flask.g` object to make it accessible globally in the request.
    """
    user = get_user()
    g.user = user

@babel.localeselector
def get_locale():
    """
    Determine the best match for the user's preferred language.
    The order of priority is:
    1. Locale from URL parameters (`locale`)
    2. Locale from user settings
    3. Locale from the Accept-Language header
    4. Default locale
    """
    # Check if a `locale` parameter is passed in the URL and is valid
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    
    # If a user is logged in, use their preferred locale (if valid)
    if g.user and g.user.get('locale') and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    
    # Fallback to the Accept-Language header
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@babel.timezoneselector
def get_timezone():
    """
    Determine the best match for the user's preferred time zone.
    The order of priority is:
    1. Time zone from URL parameters (`timezone`)
    2. Time zone from user settings
    3. Default to UTC
    """
    # Check if a `timezone` parameter is passed in the URL and is valid
    timezone_str = request.args.get('timezone')
    if timezone_str:
        try:
            # Try to validate the timezone using pytz
            pytz.timezone(timezone_str)
            return timezone_str
        except exceptions.UnknownTimeZoneError:
            pass  # Invalid timezone, will fallback to user timezone or UTC
    
    # If a user is logged in, use their preferred timezone (if valid)
    if g.user and g.user.get('timezone'):
        try:
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except exceptions.UnknownTimeZoneError:
            pass  # Invalid user timezone, will fallback to UTC
    
    # Fallback to default timezone (UTC)
    return app.config['BABEL_DEFAULT_TIMEZONE']

@app.route('/')
def index():
    """
    Renders the index page with a title, header, and the user's time zone.
    Displays a welcome message if the user is logged in.
    """
    return render_template('7-index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
