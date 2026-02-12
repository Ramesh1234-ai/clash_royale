"""
WSGI entry point for Gunicorn
This file is used by Gunicorn to run the Flask application in production
"""
import os
from app import create_app

# Create the app instance for Gunicorn
app = create_app(config_name=os.getenv('FLASK_ENV', 'production'))

if __name__ == "__main__":
    app.run()
