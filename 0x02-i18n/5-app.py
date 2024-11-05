#!/usr/bin/env python3
"""
A simple Flask app that simulates user login and internationalization.
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _

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
    If a user is logged in, use their preferred locale; otherwise, fall back to the default.
    """
    if g.user and g.user.get('locale'):
        return g.user['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/')
def index():
    """
    Renders the index page with a title and a header.
    Displays a welcome message if the user is logged in.
    """
    return render_template('5-index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
