# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Application Overview

"Aim for the Stars" is a Flask-based self-reflection web application that helps users track personal growth through daily diary entries and behavioral reflection. Users write diary entries, rate them as positive behavior (+5 points) or behavior to change (+2 points), and track their progress through gamification elements like points, streaks, and analytics.

## Core Architecture

### Application Structure
- **Flask Application Factory**: `app/__init__.py` uses `create_app()` factory pattern
- **Configuration**: Environment-based config in `app/config.py` (development/production/testing)
- **Database**: SQLAlchemy with Flask-Migrate for schema management
- **Authentication**: Session-based with password hashing (Werkzeug)
- **Security**: CSRF protection (Flask-WTF), rate limiting (Flask-Limiter)

### Key Components
- **Models** (`app/models/`): User, DiaryEntry, DailyStats, Goal database models
- **Routes** (`app/routes/`): Blueprint-based routing (auth, diary, goals, progress, etc.)
- **Templates** (`app/templates/`): Bootstrap 5 frontend with Chart.js visualizations
- **Utilities** (`app/utils/`): Helper functions for goals, progress, and search

## Development Commands

### Running the Application
```bash
python run.py                    # Start development server on port 5000
python -m flask run              # Alternative way to run
```

### Testing
```bash
pytest                          # Run all tests
pytest -v                       # Verbose output
pytest tests/test_models/       # Run specific test directory
pytest -m "not slow"            # Skip slow tests
pytest --cov=app                # Run with coverage
```

### Database Management
```bash
flask db init                   # Initialize migrations (first time)
flask db migrate -m "message"   # Create migration
flask db upgrade               # Apply migrations
python check_db.py             # Check database schema
```

### Security Auditing
```bash
safety check                   # Check dependencies for vulnerabilities
pip-audit                     # Alternative security audit tool
```

## Key Features & Implementation Details

### Database Schema
- **User**: id, email, password (hashed), user_name
- **DiaryEntry**: id, user_id, entry_date, content, rating (-1 or 1)
- **DailyStats**: id, user_id, date, points, current_streak, longest_streak
- **Goal**: id, user_id, name, description, target_date, status, points_target

### Authentication Flow
- Session-based authentication with 24-hour timeout
- Password hashing using Werkzeug
- CSRF protection on all forms
- Rate limiting (200/day, 50/hour default)

### Points System
- Encouraged behavior: +5 points
- Behavior to change: +2 points
- Daily stats tracking with streak calculation
- Analytics dashboard with Chart.js visualizations

### Security Features
- Environment-based configuration (requires .env with SECRET_KEY)
- Session security (secure, httponly, samesite cookies)
- Input validation and sanitization
- CSRF protection on forms
- Rate limiting on routes

## Configuration

### Environment Variables
Create `.env` file with:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///users.db  # or PostgreSQL URL for production
FLASK_ENV=development            # or production
```

### Database Configuration
- Development: SQLite (`users.db`)
- Production: PostgreSQL (via DATABASE_URL)
- Testing: In-memory SQLite

## Testing Strategy

Tests are organized by component:
- `test_models/`: Database model tests
- `test_routes/`: Route/endpoint tests
- `test_utils/`: Utility function tests
- `test_forms/`: Form validation tests

Uses pytest with Flask-testing integration and coverage reporting.

## Common Workflows

1. **Adding new features**: Create model → migration → routes → templates → tests
2. **Database changes**: Modify model → `flask db migrate` → `flask db upgrade`
3. **Security updates**: Run `safety check` and `pip-audit` regularly
4. **Testing**: Always run full test suite before commits

## Production Deployment

- Uses Gunicorn WSGI server
- Supports PostgreSQL and Redis
- Configured for Railway/Heroku deployment
- Environment-based configuration switching