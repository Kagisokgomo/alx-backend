#!/usr/bin/env python3
"""
A simple Flask app with internationalization that allows forcing a locale through the URL query parameter.
"""
from flask import Flask, render_template, request
from flask_babel import Babel, _

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

@babel.localeselector
def get_locale():
    """
    Determine the best match for the user's preferred language.
    - First, check if there's a `locale` query parameter in the URL.
    - If it exists and is valid, use that as the locale.
    - If not, fall back to the `Accept-Language` header or the default locale.
    """
    # Check if the `locale` parameter is in the query string
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    # Otherwise, fall back to the default behavior
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/')
def index():
    """
    Renders the index page with a title and header.
    """
    return render_template('4-index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
