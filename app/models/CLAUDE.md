# app/models/ Directory

This directory contains SQLAlchemy database models for the "Aim for the Stars" application.

## Database Models

### Core Models

#### `user.py` - User Model
- **Purpose**: User authentication and profile management
- **Key Fields**: 
  - `id` (Primary key)
  - `email` (Unique, required)
  - `password` (Hashed with Werkzeug)
  - `user_name` (Optional display name)
- **Security**: Automatic password hashing on assignment
- **Relationships**: One-to-many with DiaryEntry, DailyStats, Goal

#### `diary_entry.py` - DiaryEntry Model
- **Purpose**: Stores user diary entries and behavior ratings
- **Key Fields**:
  - `id`, `user_id` (Foreign key)
  - `entry_date`, `content`
  - `rating` (-1 for behavior to change, +1 for encouraged behavior)
- **Business Logic**: Drives the points system and progress tracking

#### `daily_stats.py` - DailyStats Model
- **Purpose**: Tracks daily aggregated statistics and streaks
- **Key Fields**:
  - `id`, `user_id`, `date`
  - `points` (Daily point total)
  - `current_streak`, `longest_streak`
- **Calculations**: Auto-computed from diary entries

#### `goal.py` - Goal Model
- **Purpose**: User-defined goals with progress tracking
- **Key Fields**:
  - `id`, `user_id`
  - `name`, `description`, `target_date`
  - `status` (active/completed/paused)
  - `points_target`

### Database Configuration

#### `database.py`
- SQLAlchemy database instance initialization
- Shared `db` object used across all models
- Configured in app factory for different environments

#### `__init__.py`
- Exports all models and database instance
- Provides centralized import point for models
- **Import pattern**: `from app.models import db, User, DiaryEntry, DailyStats, Goal`

## Database Schema Notes

- **Snake case table names**: All tables use plural snake_case naming
- **Foreign key relationships**: Proper cascading delete configurations
- **Validation**: Model-level validation for data integrity
- **Indexing**: Optimized for common query patterns (user_id, dates)

## Development Patterns

- **Model inheritance**: All models inherit from `db.Model`
- **Type hints**: Full typing support for better IDE integration
- **Property decorators**: Used for computed fields and validation
- **Relationship loading**: Configured for optimal query performance

## Migration Management

Models work with Flask-Migrate for schema versioning:
- Changes to models require new migrations: `flask db migrate -m "description"`
- Apply migrations: `flask db upgrade`
- Always review generated migrations before applying