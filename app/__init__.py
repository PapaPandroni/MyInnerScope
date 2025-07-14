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
from typing import Optional, Dict
from flask import Flask, render_template, session, g, flash, current_app
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_compress import Compress
from datetime import datetime, timedelta, timezone
from .config import config

# Import database and models
from .models import db, User

# Import routes
from .routes import register_blueprints


def create_app(config_name: Optional[str] = None) -> Flask:
    """Application factory function.
    
    Args:
        config_name: The configuration environment name (development, production, testing).
        
    Returns:
        Configured Flask application instance.
    """
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Validate configuration
    config[config_name].validate()

    # Initialize database with app
    db.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Initialize Flask-WTF for CSRF protection
    csrf = CSRFProtect(app)

    # Initialize Flask-Compress for automatic compression
    compress = Compress(app)

    # Initialize Flask-Limiter for rate limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri=os.environ.get(
            "REDIS_URL", "memory://"
        ),  # Fallback to in-memory for local dev
    )

    # Make limiter available globally
    app.limiter = limiter

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
        app.logger.info("My Inner Scope startup")

    @app.before_request
    def before_request() -> None:
        """Middleware to handle session validation and timeout"""
        session.permanent = True  # Use the lifetime from the config

        # Renew session on activity
        if session.get("user_id") and session.get("last_activity"):
            # Convert stored string time back to datetime object
            last_activity = datetime.fromisoformat(session["last_activity"])

            # Check if the session has expired
            if (
                datetime.now(timezone.utc) - last_activity
                > current_app.permanent_session_lifetime
            ):
                session.clear()  # Session expired
                flash("Your session has expired. Please log in again.", "info")

        # Update last activity time for the current request, making it timezone-aware
        session["last_activity"] = datetime.now(timezone.utc).isoformat()

        # Set user context for templates
        g.user = session.get("user_id")

    @app.context_processor
    def inject_user() -> Dict[str, Optional["User"]]:
        user = None
        if "user_id" in session:
            user = User.query.get(session["user_id"])
        return dict(current_user=user)

    @app.context_processor
    def inject_server_time() -> Dict[str, str]:
        """Inject server time and timezone into all templates"""
        now = datetime.now(timezone.utc)
        return dict(
            server_time=now.isoformat(),
            server_timezone=str(now.tzinfo)
        )

    @app.after_request
    def add_caching_headers(response):
        """Add caching headers for static assets and performance optimization"""
        from flask import request
        
        # Only add caching headers for successful responses
        if response.status_code == 200:
            # Cache static assets for 1 year
            if (request.path.startswith('/static/') or 
                request.path.endswith(('.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.woff', '.woff2', '.ttf'))):
                response.cache_control.max_age = 31536000  # 1 year
                response.cache_control.public = True
                # Add ETag for better caching
                response.add_etag()
                response.make_conditional(request)
            
            # Cache HTML pages for a short time
            elif response.content_type and response.content_type.startswith('text/html'):
                response.cache_control.max_age = 300  # 5 minutes
                response.cache_control.public = True
        
        return response

    return app
