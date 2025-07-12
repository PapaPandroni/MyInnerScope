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
- **Models** (`app/models/`): User, DiaryEntry, DailyStats, Goal, PointsLog database models
- **Routes** (`app/routes/`): Blueprint-based routing (auth, diary, goals, progress, api)
- **Templates** (`app/templates/`): Bootstrap 5 frontend with Chart.js visualizations (organized by feature)
- **Utilities** (`app/utils/`): Helper functions for goals, progress, search, and points management
- **Static Assets** (`app/static/`): Feature-organized CSS/JS (goals/, progress/, shared/, etc.)

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

### Code Quality & Formatting
```bash
black .                        # Format code (88-char line length)
isort .                        # Sort imports
pytest -m "unit"               # Run unit tests only
pytest -m "integration"        # Run integration tests only
```

### Security Auditing
```bash
safety check                   # Check dependencies for vulnerabilities
pip-audit                     # Alternative security audit tool
```

### Data Maintenance
```bash
python data_integrity_check.py    # Check database consistency
python backfill_points_log.py     # Backfill historical points data
```

## Key Features & Implementation Details

### Database Schema
- **User**: id, email, password (hashed), user_name
- **DiaryEntry**: id, user_id, entry_date, content, rating (-1 or 1)
- **DailyStats**: id, user_id, date, points, current_streak, longest_streak (aggregated cache)
- **PointsLog**: id, user_id, date, points, source_type, source_id, description (detailed transactions)
- **Goal**: id, user_id, name, description, target_date, status, points_target

### Authentication Flow
- Session-based authentication with 24-hour timeout
- Password hashing using Werkzeug
- CSRF protection on all forms
- Rate limiting (200/day, 50/hour default)

### Points System
- **Point Values**: Encouraged behavior (+5), Growth opportunity (+2), Goal completion (+10), Goal failure (+1), Daily login (+1)
- **Streak Milestone Rewards**: Rolling rewards for consistency (7-day: +10 points, 30-day: +50 points)
- **Dual Tracking**: PointsLog (detailed transactions) + DailyStats (aggregated cache)
- **Points Service**: Centralized `PointsService` manages transactions and consistency
- **Point Sources**: `PointsSourceType` enum (diary_entry, goal_completed, goal_failed, daily_login, streak_7_day, streak_30_day)
- **Analytics**: Clickable breakdown modals with detailed transaction history
- **Streak Calculation**: Real-time calculation based on consecutive diary entries only

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

Tests are organized by component and type:
- `test_models/`: Database model tests
- `test_routes/`: Route/endpoint tests  
- `test_utils/`: Utility function tests
- `test_forms/`: Form validation tests

### Test Categories
- **Unit tests**: Fast, isolated component tests
- **Integration tests**: Database and service integration
- **Slow tests**: Comprehensive end-to-end scenarios

Uses pytest with Flask-testing integration, coverage reporting, and custom markers for test organization.

## Common Workflows

1. **Adding new features**: Create model → migration → routes → templates → tests
2. **Database changes**: Modify model → `flask db migrate` → `flask db upgrade`
3. **Security updates**: Run `safety check` and `pip-audit` regularly
4. **Testing**: Always run full test suite before commits

## Production Deployment

- **WSGI Server**: Gunicorn with 3 workers (`Procfile`)
- **Database**: PostgreSQL (Railway/Heroku)
- **System Dependencies**: WeasyPrint, Cairo, Pango for PDF generation (`nixpacks.toml`)
- **Environment**: Automatic Railway deployment with migrations
- **CI/CD**: GitHub Actions security audit workflow
- **Database Compatibility**: SQLite (dev) ↔ PostgreSQL (prod) using database-agnostic migrations

## Frontend Architecture

### Template Organization
- Feature-based directories: `auth/`, `diary/`, `goals/`, `main/`, `progress/`
- Shared components in `partials/`
- Custom error pages (403, 404, 500)

### JavaScript & CSS
- **Modular JS**: Feature-specific files (goals.js, charts.js, entry-toggles.js)
- **CSS Organization**: Shared components + feature-specific styles
- **User Onboarding**: Interactive tour system with localStorage persistence
- **Chart Integration**: Chart.js for analytics with clickable data points

### Diary Page Modernization
- **Growth Mindset Buttons**: "I'm Proud of This" / "I'll Grow from This" (replacing outcome-focused language)
- **Rotating Daily Prompts**: 10 thoughtful reflection questions that rotate daily for fresh engagement
- **Subtle Streak Display**: Current streak shown in header with elegant golden styling
- **Enhanced Micro-Interactions**: Smooth hover effects, gentle animations, improved visual feedback
- **Visual Polish**: Better shadows, depth, responsive design while maintaining minimal aesthetic

## Important Implementation Notes

### Database Compatibility
- **PostgreSQL vs SQLite**: Use SQLAlchemy inspector instead of `sqlite_master`
- **Enum Handling**: Store as String(20) for PostgreSQL compatibility
- **Migration Safety**: Database-agnostic patterns for production deployment

### Points System Implementation
- **Transaction Integrity**: All point awards go through `PointsService.award_points()`
- **Data Consistency**: PointsLog is source of truth, DailyStats is cache
- **Streak Calculation**: Fixed to use real-time diary entry checking instead of stored values
- **Milestone Rewards**: Rolling system with modulo logic (`streak % 7 == 0`, `streak % 30 == 0`)
- **Duplicate Prevention**: Milestone awards only given once per day via PointsLog checking
- **Enum Conversion**: Handle both enum objects and string values in queries
- **Database Agnostic**: All new features work with SQLite (dev) and PostgreSQL (prod)