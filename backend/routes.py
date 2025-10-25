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


@main_bp.route('/todo', methods=['GET'])
def todo_page():
    """Render the To-Do creation page."""
    return render_template('todo.html')
@main_bp.route('/submittodoitem', methods=['POST'])
def submittodoitem():
    """Accept a todo item (itemName, itemDescription) and store it in MongoDB.

    Accepts form-encoded or JSON body. Returns JSON with success status.
    """
    # Accept both form fields and JSON payloads
    if request.is_json:
        payload = request.get_json() or {}
        item_name = payload.get('itemName') or payload.get('item_name')
        item_description = payload.get('itemDescription') or payload.get('item_description')
    else:
        item_name = request.form.get('itemName') or request.form.get('item_name')
        item_description = request.form.get('itemDescription') or request.form.get('item_description')

    if not item_name:
        return {"success": False, "error": "itemName is required"}, 400

    try:
        # store in a 'todos' collection (or env override)
        todos_collection_name = 'todos'
        collection = get_collection(todos_collection_name)
        if collection is None:
            # For form submissions, render the template with an error; for API return JSON
            if request.is_json:
                return {"success": False, "error": "Database not connected"}, 500
            return render_template('todo.html', error="Database not connected")

        doc = {
            'itemName': item_name,
            'itemDescription': item_description,
            'created_at': datetime.utcnow()
        }
        collection.insert_one(doc)
        # If this was a normal form submission, redirect to success page
        if request.is_json:
            return {"success": True, "message": "Todo item saved"}, 201
        return redirect(url_for('main.success'))
    except Exception as e:
        if request.is_json:
            return {"success": False, "error": str(e)}, 500
        return render_template('todo.html', error=f"Error saving todo: {e}")
