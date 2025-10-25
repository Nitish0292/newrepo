"""Backend package - provides application factory for the project.

This factory exports `create_app()` which configures the Flask app, wires the
database helper and registers the routes blueprint. Templates and static files
are served from the `frontend/` folder at the repository root.
"""
import os
from flask import Flask
from dotenv import load_dotenv


def create_app() -> Flask:
    load_dotenv()
    # Resolve frontend paths relative to the repository root (one level above backend/)
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    templates_path = os.path.join(repo_root, 'frontend', 'templates')
    static_path = os.path.join(repo_root, 'frontend', 'static')

    app = Flask(__name__, template_folder=templates_path, static_folder=static_path)

    # Initialize DB (backend.database will read MONGO_URL from env)
    try:
        from . import database
        database.init_db()
    except Exception:
        # keep the app running even if DB init fails; handlers will show errors
        pass

    # Register routes blueprint
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
