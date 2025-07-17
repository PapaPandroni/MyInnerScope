# app/ Directory

This is the main Flask application directory containing the core application code for "Aim for the Stars" - a self-reflection web application with sophisticated points tracking, user onboarding, and analytics.

## Directory Structure

```
app/
├── __init__.py          # Application factory pattern implementation
├── config.py            # Environment-based configuration settings
├── forms.py            # Flask-WTF form definitions for auth and user input
├── models/             # Database models (User, DiaryEntry, DailyStats, PointsLog, Goal)
├── routes/             # Blueprint-based route handlers (auth, diary, goals, progress, api)
├── static/             # Feature-organized static assets (CSS, JS, images)
├── templates/          # Feature-organized Jinja2 HTML templates
└── utils/              # Utility functions (points service, goal helpers, search)
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
- **Blueprint-based modular routing**: Separate blueprints for auth, diary, goals, progress, api
- **SQLAlchemy ORM**: Database operations with dual-database compatibility (SQLite/PostgreSQL)
- **Points tracking system**: Centralized PointsService with detailed transaction logging
- **Session-based authentication**: 24-hour timeout with renewal middleware
- **Rate limiting**: Flask-Limiter for security (configurable per route)
- **CSRF protection**: All forms protected via Flask-WTF
- **User onboarding**: Interactive tour system with localStorage persistence

## Security Features

- Session-based authentication with 24-hour timeout
- CSRF protection via Flask-WTF
- Rate limiting via Flask-Limiter (200/day, 50/hour default)
- Password hashing using Werkzeug
- Input validation and sanitization

## Development Notes

- **Environment configuration**: Uses `.env` file for secrets, database URLs, and HTTPS URL scheme configuration
- **Hot-reloading**: Development mode with automatic file change detection
- **Database migrations**: Flask-Migrate with PostgreSQL/SQLite compatibility patterns
- **Error handling**: Custom error pages (403, 404, 500) with user-friendly messages
- **Logging**: Comprehensive logging for authentication, errors, and security events
- **Code formatting**: Black (88-char) and isort configured via pyproject.toml
- **Performance optimization**: Flask-Compress, static asset caching, image optimization

## Recent Architecture Improvements

- **Dual database compatibility**: SQLite for development, PostgreSQL for production
- **Points logging system**: Detailed transaction history with PointsLog model
- **API endpoints**: RESTful API blueprint for frontend-backend communication
- **Frontend modularization**: Feature-based organization of templates and static assets
- **User experience**: Interactive onboarding tour and clickable analytics
- **Performance optimization**: Comprehensive performance enhancements (SEO, compression, image optimization)
- **SEO infrastructure**: Complete search engine optimization with structured data **REFOCUSED ON DAILY JOURNALING & SELF-REFLECTION**
- **Analytics integration**: Google Analytics 4 and Search Console active via environment variables
- **Authority linking**: External links to reputable sources for E-A-T signals
- **SEO Strategy Update**: Comprehensive refocus from goal-setting to daily journaling, reflective writing, and mindful introspection
- **HTTPS Configuration**: PREFERRED_URL_SCHEME=https for proper sitemap URL generation