"""Project runner.

This file provides a minimal entry point. The backend logic has been moved to
the `backend` package; we simply create the app via its factory and run it.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Import factory from backend package
from backend import create_app


app = create_app()


if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true')
