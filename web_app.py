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
from flask import Flask, render_template
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