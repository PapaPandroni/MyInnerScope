from .auth import auth_bp
from .diary import diary_bp
from .progress import progress_bp
from .reader import reader_bp
from .goals import goals_bp

def register_blueprints(app):
    """Register all blueprints with the Flask app"""
    app.register_blueprint(auth_bp)
    app.register_blueprint(diary_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(reader_bp)
    app.register_blueprint(goals_bp)

    # Apply rate limiting to login and register routes
    limiter = getattr(app, 'limiter', None)
    if limiter:
        limiter.limit("5 per minute")(app.view_functions['auth.login_page'])
        limiter.limit("3 per hour")(app.view_functions['auth.register'])