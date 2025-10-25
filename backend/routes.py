"""Flask route handlers moved into backend package.

These preserve the same endpoints and behavior as the previous monolithic
`app.py` but are grouped in a blueprint for a cleaner backend structure.
"""
from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime

from .database import get_collection

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    """Main form page"""
    day_of_week = datetime.today().strftime('%A')
    current_time = datetime.now().strftime('%H:%M:%S')
    return render_template('index.html', day_of_week=day_of_week, current_time=current_time)


@main_bp.route('/submit', methods=['POST'])
def submit():
    """Insert form data into MongoDB"""
    formdata = dict(request.form)
    try:
        collection = get_collection()
        if collection is not None:
            collection.insert_one(formdata)
            return redirect(url_for('main.success'))
        else:
            return render_template('index.html', error="Database not connected")
    except Exception as e:
        return render_template('index.html', error=f"Error inserting data: {e}")


@main_bp.route('/success')
def success():
    """Success page"""
    return render_template('success.html')


@main_bp.route('/view')
def view():
    """View all stored data from MongoDB"""
    try:
        collection = get_collection()
        if collection is not None:
            data = list(collection.find({}, {'_id': 0}))
            return render_template('view.html', data=data)
        else:
            return render_template('view.html', data=[], error="Database not connected")
    except Exception as e:
        return render_template('view.html', data=[], error=f"Error fetching data: {e}")
