#!/usr/bin/env python3
"""
A simple Flask app that serves an index page.
"""
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    """
    Renders the index page with a title and header.
    """
    return render_template('0-index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
