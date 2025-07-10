# app/ Directory

This is the main Flask application directory containing the core application code for "Aim for the Stars" - a self-reflection web application.

## Directory Structure

```
app/
├── __init__.py          # Application factory pattern implementation
├── config.py            # Environment-based configuration settings
├── forms.py            # Flask-WTF form definitions
├── models/             # Database models (SQLAlchemy)
├── routes/             # Blueprint-based route handlers
├── static/             # Static assets (CSS, JS, images)
├── templates/          # Jinja2 HTML templates
└── utils/              # Utility functions and helpers
```

## Key Files

### `__init__.py` - Application Factory
- Contains `create_app()` factory function
- Initializes Flask extensions (SQLAlchemy, Migrate, CSRF, Rate Limiting)
- Configures session handling and user context
- Sets up middleware for session timeout and renewal

### `config.py` - Configuration Management
- Environment-based configuration (development/production/testing)
- Database configuration (SQLite for dev, PostgreSQL for production)
- Security settings (SECRET_KEY, session configuration)

### `forms.py` - Form Definitions
- Flask-WTF form classes for user input validation
- CSRF protection integration
- Form validation rules and error messages

## Application Architecture

This Flask application follows the **Application Factory Pattern** with:
- Blueprint-based modular routing
- SQLAlchemy ORM for database operations
- Session-based authentication
- Rate limiting for security
- CSRF protection on all forms

## Security Features

- Session-based authentication with 24-hour timeout
- CSRF protection via Flask-WTF
- Rate limiting via Flask-Limiter (200/day, 50/hour default)
- Password hashing using Werkzeug
- Input validation and sanitization

## Development Notes

- Uses environment variables for configuration
- Supports hot-reloading in development mode
- Comprehensive error handling and logging
- Database migrations via Flask-Migrate