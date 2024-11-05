#!/usr/bin/env python3
"""
A simple Flask app that simulates user login and internationalization with time zone handling.
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
import pytz
from pytz import exceptions
from datetime import datetime

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
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    
    if g.user and g.user.get('locale') and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    
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
    timezone_str = request.args.get('timezone')
    if timezone_str:
        try:
            pytz.timezone(timezone_str)
            return timezone_str
        except exceptions.UnknownTimeZoneError:
            pass
    
    if g.user and g.user.get('timezone'):
        try:
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except exceptions.UnknownTimeZoneError:
            pass
    
    return app.config['BABEL_DEFAULT_TIMEZONE']

@app.route('/')
def index():
    """
    Renders the index page with the current time based on the inferred time zone.
    """
    # Get the current time in the correct time zone
    current_time_zone = get_timezone()
    current_time = datetime.now(pytz.timezone(current_time_zone))
    
    # Format the time using Flask-Babel's format_datetime function
    formatted_time = format_datetime(current_time)
    
    # Render the template with the formatted current time
    return render_template('index.html', current_time=formatted_time)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


app = Flask(__name__)

# Config class to specify supported languages
class Config:
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

app.config.from_object(Config)

# Initialize the Babel object
babel = Babel(app)

# Locale selector function to determine which locale to use
@babel.localeselector
def get_locale():
    # Determine the best match with the supported languages
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
