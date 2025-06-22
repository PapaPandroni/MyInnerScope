from .auth import auth_bp
from .diary import diary_bp
from .progress import progress_bp
from .reader import reader_bp

def register_blueprints(app):
    """Register all blueprints with the Flask app"""
    app.register_blueprint(auth_bp)
    app.register_blueprint(diary_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(reader_bp)