# GEMINI.md - Project "My Inner Scope"

This document provides a comprehensive overview of the "My Inner Scope" web application, intended to give a new lead developer a thorough understanding of the project's architecture, features, and codebase.

## 1. Project Overview

"My Inner Scope" is a Flask-based web application designed for self-reflection and personal growth. Users can write daily diary entries, categorize their behaviors, and track their progress through a gamified system of points, streaks, and visualizations.

### 1.1. Core Features

*   **User Authentication:** Secure user registration and login system with password hashing.
*   **Daily Diary Entries:** Users can create, view, and rate their daily diary entries.
*   **Gamification:** A points-based system rewards users for diary entries and completing goals. Streaks are tracked to encourage consistent engagement.
*   **Progress Dashboard:** A comprehensive dashboard visualizes user progress with interactive charts, statistics, and a word cloud of their most used words.
*   **Goal Setting:** Users can set and track weekly goals across various categories.
*   **Data Export:** Users can download their data in JSON and CSV formats.
*   **User Profile Management:** Users can change their username and password, and delete their account.

### 1.2. Technology Stack

*   **Backend:** Flask, SQLAlchemy, Flask-Migrate, Flask-WTF, Flask-Limiter
*   **Database:** SQLite (for development), with PostgreSQL as a potential production option.
*   **Frontend:** Bootstrap 5, Chart.js, wordcloud2.js
*   **Deployment:** Gunicorn, Nixpacks
*   **Testing:** Pytest, pytest-flask, pytest-mock, coverage.py

## 2. Project Structure

The project follows a modular structure, with the core application logic contained within the `app` directory.

```
/
├── app/
│   ├── __init__.py             # Application factory
│   ├── config.py               # Configuration settings
│   ├── forms.py                # Flask-WTF forms
│   ├── models/                 # SQLAlchemy models (User, DiaryEntry, Goal, etc.)
│   │   └── points_log.py       # Model for detailed point transaction logging
│   ├── routes/                 # Flask blueprints for different features
│   │   └── api.py              # Blueprint for API endpoints
│   ├── static/                 # CSS, JavaScript, and image assets
│   ├── templates/              # Jinja2 templates
│   └── utils/                  # Helper functions
│       ├── points_service.py   # Centralized service for gamification logic
│       ├── goal_helpers.py     # Functions for goal management
│       └── progress_helpers.py # Functions for dashboard data
├── tests/                      # Pytest tests
├── migrations/                 # Flask-Migrate migration scripts
├── requirements.txt            # Python dependencies
├── nixpacks.toml               # Nixpacks configuration for deployment
├── Procfile                    # Procfile for Heroku/other platforms
├── pytest.ini                  # Pytest configuration
├── run.py                      # Application entry point
└── ...
```

## 3. Detailed Component Breakdown

### 3.1. Application Factory (`app/__init__.py`)

The application is initialized using the factory pattern in `create_app()`. This function:

*   Loads the appropriate configuration based on the `FLASK_ENV` environment variable.
*   Initializes Flask extensions: `db` (SQLAlchemy), `migrate` (Flask-Migrate), `csrf` (Flask-WTF CSRFProtect), and `limiter` (Flask-Limiter).
*   Registers all blueprints from the `app/routes` directory.
*   Sets up logging for production environments.
*   Includes a `before_request` hook to manage session timeouts and set the `g.user` context variable.
*   Uses a context processor to inject the `current_user` object into all templates.

### 3.2. Configuration (`app/config.py`)

The application uses a class-based configuration structure to separate settings for different environments (development, production, testing). Key configuration options include:

*   `SECRET_KEY`: Loaded from an environment variable.
*   `SQLALCHEMY_DATABASE_URI`: Configured for SQLite by default, but can be overridden for other databases.
*   `PERMANENT_SESSION_LIFETIME`: Sets the session timeout.
*   `WTF_CSRF_ENABLED`: Enables or disables CSRF protection.

### 3.3. Database Models (`app/models/`)

The database schema is defined using SQLAlchemy models with plural, snake_case table names (e.g., `users`, `diary_entries`).

*   **`User`:** Stores user information, including email, hashed password, and an optional username.
*   **`DiaryEntry`:** Represents a single diary entry, linked to a user, with content and a rating.
*   **`DailyStats`:** Tracks daily user statistics, including points, current streak, and longest streak. This serves as an aggregated cache for performance.
*   **`Goal`:** Defines user goals, with categories, status, and progress tracking.
*   **`PointsLog`:** A detailed, transactional log of every point-earning activity for accuracy and auditability.

### 3.4. Routes (`app/routes/`)

The application's routes are organized into blueprints based on functionality:

*   **`auth_bp`:** Handles user login, registration, and logout.
*   **`diary_bp`:** Manages the creation of diary entries.
*   **`goals_bp`:** Implements all goal-related functionality.
*   **`legal_bp`:** Serves the privacy policy and terms of service pages.
*   **`main_bp`:** Contains the main landing page and error handlers.
*   **`progress_bp`:** Powers the progress dashboard.
*   **`reader_bp`:** Allows users to read and search their past diary entries.
*   **`user_bp`:** Manages user profile settings, data downloads, and account deletion.
*   **`api_bp`:** Provides API endpoints, such as the daily points breakdown.

### 3.5. Utility Functions (`app/utils/`)

Helper functions are organized into modules to support the application's business logic:

*   **`points_service.py`:** A centralized service that manages all point-earning activities, ensuring consistency between `PointsLog` and `DailyStats`.
*   **`goal_helpers.py`:** Contains functions for creating, updating, and retrieving goal-related data.
*   **`progress_helpers.py`:** Provides functions for calculating and formatting data for the progress dashboard.
*   **`search_helpers.py`:** Implements the search functionality for diary entries.

### 3.6. Frontend (`app/static/` and `app/templates/`)

The frontend is built with Bootstrap 5 and uses Jinja2 for templating. Key frontend components include:

*   **`base.html`:** A base template that all other pages extend.
*   **Interactive Charts:** Chart.js is used to create interactive charts on the progress dashboard.
*   **Word Cloud:** `wordcloud2.js` generates a word cloud from the user's diary entries.
*   **Onboarding Tour:** A multi-page, card-based tour guides new users through the application's features.

## 4. Key Implementation Details

### 4.1. Gamification Logic

The points system is managed by the `PointsService` to ensure transactional integrity.

*   **Points:** Users earn points for various actions:
    *   +5 points for an "encouraged behavior" diary entry.
    *   +2 points for a "something to change" diary entry.
    *   +10 points for completing a goal.
    *   +1 point for a failed goal (recognizing effort).
    *   +1 point for a daily login.
*   **Streaks:** The `DailyStats` model tracks the current and longest streaks of consecutive days with at least one diary entry.

### 4.2. Security

*   **Password Hashing:** Passwords are hashed using `werkzeug.security`.
*   **CSRF Protection:** Flask-WTF is used to protect against Cross-Site Request Forgery attacks.
*   **Rate Limiting:** Flask-Limiter is used to prevent brute-force attacks on authentication and other key routes.
*   **Secure Session Management:** Secure session cookies are used with a 24-hour timeout.

### 4.3. Testing

The project has a comprehensive test suite using Pytest. Tests are organized into `unit` and `integration` directories. The suite includes specific tests for frontend regression (`test_frontend_regression.py`) and HTML structure (`test_html_structure.py`) to prevent recurring bugs and ensure template integrity.

## 5. Getting Started

To run the application locally, follow these steps:

1.  **Clone the repository.**
2.  **Create and activate a virtual environment.**
3.  **Install the dependencies:** `pip install -r requirements.txt`
4.  **Create a `.env` file** with a `SECRET_KEY`.
5.  **Run database migrations:** `flask db upgrade`
6.  **Run the application:** `python run.py`

The application will be available at `http://localhost:5000`.