"""
Aim for the Stars - Self-Reflection Web Application
Copyright 2025 Peremil Starklint Söderström

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import logging
from flask import Flask, render_template, session, g, flash, current_app
from datetime import datetime, timedelta, timezone
from config import config

# Import database and models
from models import db

# Import routes
from routes import register_blueprints

def create_app(config_name=None):
    """Application factory function"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Validate configuration
    config[config_name].validate()

    # Initialize database with app
    db.init_app(app)

    # Register blueprints (routes)
    register_blueprints(app)

    # --- Logging Setup ---
    if not app.debug and not app.testing:
        # In production, log to a file
        # For this example, we'll just use a basic console logger
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Aim for the Stars startup')

    @app.before_request
    def before_request():
        """Middleware to handle session validation and timeout"""
        session.permanent = True  # Use the lifetime from the config

        # Renew session on activity
        if session.get('user_id') and session.get('last_activity'):
            # Convert stored string time back to datetime object
            last_activity = datetime.fromisoformat(session['last_activity'])

            # Check if the session has expired
            if datetime.now(timezone.utc) - last_activity > current_app.permanent_session_lifetime:
                session.clear()  # Session expired
                flash("Your session has expired. Please log in again.", "info")
        
        # Update last activity time for the current request, making it timezone-aware
        session['last_activity'] = datetime.now(timezone.utc).isoformat()

        # Set user context for templates
        g.user = session.get('user_id')
    
    @app.route("/")
    def hello():
        return render_template("index.html")
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def internal_server_error(e):
        current_app.logger.error(f"Internal Server Error: {e}", exc_info=True)
        return render_template('errors/500.html'), 500

    return app

if __name__ == "__main__":
    # Create the app
    app = create_app()
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Run the app
    app.run(host="0.0.0.0", debug=app.config['DEBUG'])