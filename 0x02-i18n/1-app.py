#!/usr/bin/env python3
"""
A simple Flask app that serves an index page with internationalization support.
"""
from flask import Flask, render_template
from flask_babel import Babel

class Config:
    """
    Config class for setting up language and timezone configurations for the app.
    """
    LANGUAGES = ["en", "fr"]
    # Set default locale to English (en) and timezone to UTC
    LANGUAGES = ["en", "fr"]
    # Default locale (language) for the app
    BABEL_DEFAULT_LOCALE = "en"
    # Default timezone for the app
    BABEL_DEFAULT_TIMEZONE = "UTC"

app = Flask(__name__)
# Load the configuration from Config class
app.config.from_object(Config)

# Instantiate Babel
babel = Babel(app)

@app.route('/')
def index():
    """
    Renders the index page with a title and header.
    """
    return render_template('1-index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
