from .auth import auth_bp
from .diary import diary_bp
from .progress import progress_bp
from .reader import reader_bp
from .goals import goals_bp
from .legal import legal_bp
from .user import user_bp
from .main import main_bp

def register_blueprints(app):
    """Register all blueprints with the Flask app"""
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(diary_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(reader_bp)
    app.register_blueprint(goals_bp)
    app.register_blueprint(legal_bp)
    app.register_blueprint(user_bp)

    # Apply rate limiting to blueprints
    limiter = getattr(app, 'limiter', None)
    if limiter:
        limiter.limit("20 per minute;60 per hour")(auth_bp)
        limiter.limit("30 per minute;120 per hour")(diary_bp)
        limiter.limit("30 per minute;120 per hour")(goals_bp)
        limiter.limit("20 per minute;60 per hour")(user_bp)
        limiter.limit("20 per minute;60 per hour")(progress_bp)
        limiter.limit("60 per minute;300 per hour")(reader_bp)