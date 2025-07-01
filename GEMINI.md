# Project Overview: Aim for the Stars

This document provides a comprehensive overview of the "Aim for the Stars" web application. It is the central source of truth for the project, designed to serve as a detailed reference for an AI assistant. It includes the project's purpose, technology stack, structure, key features, and the development roadmap.

---

## 1. Project Purpose and Core Functionality

"Aim for the Stars" is a Flask-based web application designed to help users improve themselves through daily reflection and goal setting. The core functionality revolves around users writing daily diary entries about their behaviors and categorizing them as either "encouraged" or "something to change."

The application gamifies this process by awarding points for entries and tracking daily streaks, motivating users to remain consistent with their self-reflection. A detailed progress dashboard provides visualizations and statistics about the user's journey over time. Additionally, users can set and track weekly goals, further enhancing their personal development journey.

---

## 2. Technology Stack

-   **Backend**: Python with the Flask framework.
-   **Database**: SQLAlchemy ORM, defaulting to a SQLite database (`users.db`). Database migrations are managed with `Flask-Migrate` (Alembic).
-   **Frontend**:
    -   Jinja2 for HTML templating.
    -   Bootstrap 5 for responsive styling and layout.
    -   Custom CSS for specific styling and theming (sci-fi inspired).
-   **Client-Side Scripting**:
    -   JavaScript (ES6+) for interactive components.
    -   **Chart.js** for data visualization (points over time, weekday performance).
    -   **Luxon** for robust date/time handling in charts.
    -   **chartjs-plugin-zoom** for interactive chart zooming and panning.
    -   **wordcloud2.js** for generating interactive word clouds.
-   **Forms & Validation**:
    -   **Flask-WTF** for secure form handling, validation, and CSRF protection.
    -   `wtforms` validators for email, length, equality, and custom password strength (mixed case, min length).
-   **PDF Generation**:
    -   **WeasyPrint** to convert HTML/CSS to PDF for journey export.
    -   **Matplotlib** to generate static chart images (points, weekday performance) for PDF embedding.
-   **Authentication & Session Management**:
    -   **Werkzeug** for secure password hashing (`generate_password_hash`, `check_password_hash`).
    -   Secure, server-side sessions with a 24-hour timeout, managed by a `before_request` handler in `app.py`.
    -   **Flask-Limiter** for rate limiting on sensitive endpoints (e.g., login, registration).
-   **Environment Management**: `python-dotenv` for loading environment variables (e.g., `SECRET_KEY`).
-   **Logging**: Standard Python `logging` module for application monitoring and debugging.
-   **Testing**: `pytest` for automated testing (unit, integration, functional tests).
-   **Dependency Auditing**: `safety` and `pip-audit` for checking known security vulnerabilities in dependencies.

---

## 3. Project Structure

The project follows a standard Flask application structure, separating concerns into distinct modules:

-   `app.py`: The main application entry point. It functions as a pure app factory, initializing the Flask app, database, migrations, CSRF protection, rate limiting, logging, and session management.
-   `config.py`: Defines configuration environments (Development, Production, Testing) and manages session settings and database URIs.
-   `forms.py`: Contains all `Flask-WTF` form classes for input validation (e.g., `LoginForm`, `RegisterForm`, `DiaryEntryForm`, `GoalForm`, `GoalProgressForm`, `DeleteAccountForm`).
-   `models/`: Contains SQLAlchemy database models (`User`, `DiaryEntry`, `DailyStats`, `Goal`). Database queries use SQLAlchemy 2.0 style (`db.session.get()`). Datetime handling in models uses timezone-aware objects (`datetime.now(timezone.utc)`).
    -   `database.py`: Initializes the SQLAlchemy `db` object.
-   `routes/`: Defines the application's routes using Flask Blueprints.
    -   `__init__.py`: Registers all blueprints with the Flask application and applies rate limits.
    -   `main.py`: Handles the root route (`/`) and global error handlers (`403`, `404`, `500`).
    -   `auth.py`: Manages user registration, login, and logout.
    -   `diary.py`: Handles daily diary entry creation and display.
    -   `progress.py`: Renders the user's progress dashboard and handles PDF export.
    -   `reader.py`: Provides functionality to read past diary entries, including search.
    -   `goals.py`: Manages weekly goal setting, tracking, and completion.
    -   `legal.py`: Contains routes for privacy policy and terms of service pages.
    -   `user.py`: Handles user profile management, data export (JSON/CSV), and account deletion.
-   `templates/`: Contains all Jinja2 HTML templates.
    -   `base.html`: The base template including navigation, flash messages, and global scripts (e.g., `cookie_consent.js`).
    -   `_navbar.html`: Navigation bar partial.
    -   Feature-specific templates (e.g., `diary.html`, `goals.html`, `progress.html`, `login.html`, `register.html`, `settings.html`, `privacy.html`, `terms.html`, `read_diary.html`, `delete_account_confirm.html`).
    -   `errors/`: Custom error pages (`403.html`, `404.html`, `500.html`).
    -   `pdf/`: Template for PDF export (`journey.html`).
-   `static/`: Holds all static assets.
    -   `assets/`: Images (e.g., `starry_sky.jpg`).
    -   `css/`: Custom CSS files (`custom_css.css`, `goals.css`, `pdf_journey.css`, `progress.css`).
    -   `js/`: JavaScript files, organized into feature-based subdirectories.
        -   `goals/`: `goals.js` (goal-related interactivity).
        -   `legal/`: `cookie_consent.js` (cookie consent banner logic).
        -   `progress/`: `charts.js`, `entries.js`, `entry-toggles.js`, `export.js`, `main.js` (dashboard interactivity, chart rendering, PDF export).
-   `utils/`: Contains helper modules for complex logic.
    -   `goal_helpers.py`: Functions for goal management (create, update, stats).
    -   `pdf_generator.py`: Logic for generating PDF reports using WeasyPrint and Matplotlib.
    -   `progress_helpers.py`: Functions for aggregating data for the progress dashboard (streaks, points, trends).
    -   `search_helpers.py`: Functions for searching diary entries.
-   `migrations/`: Directory managed by `Flask-Migrate` (Alembic) for database schema version control.
-   `tests/`: Contains `pytest` test suite for various components of the application.

---

## 4. Key Features and Implementation

### 4.1. User Authentication & Session Management
-   **Functionality**: Secure user registration, login, and logout. Sessions expire after 24 hours of inactivity and are renewed on activity.
-   **Implementation**:
    -   `routes/auth.py` handles authentication routes using `LoginForm` and `RegisterForm` from `forms.py` for validation.
    -   Passwords are hashed using `Werkzeug.security.generate_password_hash` and verified with `check_password_hash`.
    -   `app.py` contains a `before_request` handler that validates and renews the user's session on each request, ensuring timezone-aware `datetime` objects are used.
    -   `Flask-Limiter` is applied to login and registration endpoints to prevent brute-force attacks.
    -   Failed login attempts and other authentication-related events are logged.

### 4.2. Diary and Points System
-   **Functionality**: Users submit daily diary entries, categorizing them as "encouraged" (+5 points) or "something to change" (+2 points) to earn points and build streaks.
-   **Implementation**:
    -   `routes/diary.py` manages entry creation using `DiaryEntryForm` for validation.
    -   `models/DailyStats.py` tracks daily points, current streaks, and longest streaks.
    -   Streak logic is handled within `routes/diary.py` to update `DailyStats` based on consecutive entries.

### 4.3. Progress Dashboard & PDF Export
-   **Functionality**: Provides a comprehensive dashboard with statistics, interactive charts (points over time, weekday performance), and a word cloud. Users can export their entire journey as a PDF.
-   **Implementation**:
    -   `routes/progress.py` renders the dashboard, fetching data via `utils/progress_helpers.py`.
    -   Interactive charts are rendered client-side using Chart.js, Luxon, and chartjs-plugin-zoom.
    -   Word clouds are generated client-side using wordcloud2.js, with data aggregated from diary entries.
    -   `utils/pdf_generator.py` uses WeasyPrint and Matplotlib to create the PDF export, embedding static chart images and the word cloud.
    -   The PDF export process includes a loading overlay and captures the client-side rendered word cloud image.

### 4.4. Goal Setting and Tracking
-   **Functionality**: Users can set, track, and manage weekly goals, categorized by areas like Exercise, Learning, Mindfulness, etc.
-   **Implementation**:
    -   `routes/goals.py` handles all goal-related logic using `GoalForm` and `GoalProgressForm` for validation.
    -   `utils/goal_helpers.py` provides functions for goal creation, progress updates, completion/failure, history retrieval, and statistics.
    -   The `Goal` model (`models/goal.py`) uses timezone-aware datetimes (`datetime.now(timezone.utc)`) for `created_at` timestamps and calculates progress based on week start/end dates.
    -   Points are awarded for completing goals (+10 points) or marking them as failed (+1 point).

### 4.5. User Profile & Data Management
-   **Functionality**: Users can manage their profile, download their data (JSON/CSV), and securely delete their account.
-   **Implementation**:
    -   `routes/user.py` handles profile display, data export, and account deletion.
    -   `DeleteAccountForm` from `forms.py` is used for secure account deletion requiring password re-entry.
    -   Data export serializes user-specific information from `User`, `DiaryEntry`, `Goal`, and `DailyStats` models.
    -   Account deletion performs a cascading delete across all associated user data in the database.

### 4.6. Legal & Compliance
-   **Functionality**: Provides Privacy Policy and Terms of Service pages, and implements a cookie consent banner.
-   **Implementation**:
    -   `routes/legal.py` serves the static `privacy.html` and `terms.html` pages.
    -   `static/js/legal/cookie_consent.js` manages the display and acceptance of the cookie consent banner, loaded globally via `base.html`.

---

## 5. How to Run the Application

1.  **Set up a virtual environment**: `python -m venv env && source env/bin/activate`
2.  **Install dependencies**: `pip install -r requirements.txt`
3.  **Create a `.env` file** in the project root with a `SECRET_KEY` (e.g., `SECRET_KEY='your_super_secret_key_here'`).
4.  **Initialize database migrations**:
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```
5.  **Run the application**: `python app.py`
6.  The application will be available at `http://localhost:5000`.

---

## 6. Development Roadmap (SPMP_250701.md)

This project follows a prioritized roadmap to ensure stability and security before launch. The full plan is detailed in `SPMP_250701.md`.

### 6.1. Foundational Tooling & Infrastructure
-   **Database Migrations**: Ensure all future database schema modifications are managed via `flask db migrate` and `flask db upgrade`.
-   **Testing Framework**: Continuously write comprehensive unit, integration, and functional tests for new and existing features.

### 6.2. Security Hardening & Compliance
-   **CSRF Protection for AJAX Requests**: Implement CSRF protection for all JavaScript-driven POST requests.
-   **Rate Limiting**: Apply rate limiting to all sensitive endpoints.
-   **Dependency Security Audit**: Regularly review audit reports and address identified vulnerabilities.
-   **Privacy Policy and Cookie Consent**: Review and complete content for full GDPR compliance.
-   **User Data Deletion (Right to Erasure)**: Thoroughly test and ensure the "Delete Account" feature securely and completely removes all associated user data.
-   **Data Portability**: Verify the completeness and accuracy of exported data.

### 6.3. Feature Enhancements & New Functionality
-   **Dashboard Enhancements**: Implement weekly/monthly comparison views, missed days analysis, and enhanced chart styling.
-   **User Experience Improvements**: Implement email verification, password reset, profile customization, dark/light mode toggle, and onboarding tour.
-   **New Functionality**: Enhance diary search capabilities, develop a system for weekly reflection prompts, and implement advanced analytics and insights.

### 6.4. Code Quality & Refactoring
-   **Project Structure and File Naming**:
    -   Create an `app` directory and move core application files into it. Rename `app.py` to `run.py` in the root.
    -   Complete renaming of all files and directories to `snake_case`.
    -   Update `GEMINI.md` to reflect the final project structure and file names.
-   **Python Code Style**: Apply `black` formatter, refactor `camelCase` to `snake_case`, add type hints, and convert docstrings to Google-style.
-   **Route and Helper Organization**: Create feature-based route packages with `routes.py` and `helpers.py` files, and update all imports.
-   **Static and Template File Organization**: Organize CSS/JS and HTML templates more granularly by feature.
-   **HTML and JavaScript Style**: Update HTML `id` and custom `data-*` attributes to `snake_case`, and refactor JavaScript variable/function names to `snake_case`.
-   **Database Refactoring**: Update SQLAlchemy model definitions for `snake_case` table and column names, and create a migration script for renaming.
-   **Final Review and Cleanup**: Run tests, review codebase for consistency, remove unused files, and update `README.md`.

### 6.5. Technical Debt & Performance
-   **Database Performance**: Add explicit database indexes to frequently queried columns.
-   **Centralize Flash Message Handling**: Centralize `flash` message logic for consistency.
-   **Review Datetime Usage for Consistency**: Ensure consistent and appropriate timezone-aware datetime usage.

---

## 7. Coding Style Guide

The project adheres to a strict set of coding standards to ensure consistency and maintainability. The full guide can be found in `flask_style_guide.md`.

-   **Python**: Follows PEP 8, uses `snake_case` for variables/functions/modules, and Google-style docstrings with type hints.
-   **HTML**: Uses semantic HTML5 elements and `snake_case` for custom IDs and attributes.
-   **JavaScript**: Uses modern ES6+ features and `snake_case` for variables and functions.
-   **CSS**: Follows BEM methodology for custom components and uses CSS custom properties for theming.
-   **Naming Conventions**: `snake_case` for files/directories, `snake_case` and plural for database tables.