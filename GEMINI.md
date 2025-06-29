# Project Overview: Aim for the Stars

This document provides a comprehensive overview of the "Aim for the Stars" web application. It is the central source of truth for the project, designed to serve as a detailed reference for an AI assistant. It includes the project's purpose, technology stack, structure, key features, and the development roadmap.

---

## 1. Project Purpose and Core Functionality

"Aim for the Stars" is a Flask-based web application designed to help users improve themselves through daily reflection and goal setting. The core functionality revolves around users writing daily diary entries about their behaviors and categorizing them as either "encouraged" or "something to change."

The application gamifies this process by awarding points for entries and tracking daily streaks, motivating users to remain consistent with their self-reflection. A detailed progress dashboard provides visualizations and statistics about the user's journey over time. Additionally, users can set and track weekly goals, further enhancing their personal development journey.

---

## 2. Technology Stack

-   **Backend**: Python with the Flask framework.
-   **Database**: SQLAlchemy ORM, defaulting to a SQLite database (`users.db`).
-   **Frontend**:
    -   Jinja2 for HTML templating.
    -   Bootstrap 5 for responsive styling and layout.
    -   Custom CSS for specific styling and theming (sci-fi inspired).
-   **Client-Side Scripting**:
    -   JavaScript for interactive components.
    -   **Chart.js** for data visualization.
    -   **Luxon** for date/time handling in charts.
    -   **chartjs-plugin-zoom** for interactive chart zooming.
-   **Forms & Validation**:
    -   **Flask-WTF** for secure form handling, validation, and CSRF protection.
-   **PDF Generation**:
    -   **WeasyPrint** to convert HTML/CSS to PDF.
    -   **Matplotlib** to generate static chart images for PDF embedding.
-   **Authentication & Session Management**:
    -   Werkzeug for password hashing (`generate_password_hash`, `check_password_hash`).
    -   Secure, server-side sessions with a 24-hour timeout.
-   **Environment Management**: `python-dotenv` for loading environment variables.
-   **Logging**: Standard Python `logging` module for application monitoring.

---

## 3. Project Structure

The project follows a standard Flask application structure, separating concerns into distinct modules:

-   `web_app.py`: The main application entry point. It uses the factory pattern (`create_app`) to initialize the Flask app, database, routes, logging, and session management.
-   `config.py`: Defines configuration environments (Development, Production, Testing) and manages session settings.
-   `forms.py`: Contains all `Flask-WTF` form classes for input validation (e.g., `LoginForm`, `RegisterForm`, `DiaryEntryForm`).
-   `models/`: Contains SQLAlchemy database models (`User`, `DiaryEntry`, `DailyStats`, `Goal`).
-   `routes/`: Defines the application's routes using Flask Blueprints (`auth`, `diary`, `progress`, `reader`, `goals`).
-   `templates/`: Contains all Jinja2 HTML templates, including custom error pages (`403.html`, `404.html`, `500.html`).
-   `static/`: Holds all static assets (CSS, JavaScript, images).
-   `utils/`: Contains helper modules for complex logic (`pdf_generator`, `progress_helpers`, etc.).

---

## 4. Key Features and Implementation

### 4.1. User Authentication & Session Management
-   **Functionality**: Secure user registration, login, and logout. Sessions expire after 24 hours of inactivity.
-   **Implementation**:
    -   `routes/auth.py` handles the routes using `Flask-WTF` forms for validation.
    -   Passwords are hashed using Werkzeug.
    -   `web_app.py` contains a `before_request` handler that validates and renews the user's session on each request.
    -   Failed login attempts and other auth-related events are logged.

### 4.2. Diary and Points System
-   **Functionality**: Users submit daily diary entries and categorize them to earn points and build streaks.
-   **Implementation**:
    -   `routes/diary.py` manages entry creation using the `DiaryEntryForm` for validation.
    -   `models/DailyStats.py` tracks daily points and streaks.

### 4.3. Progress Dashboard & PDF Export
-   **Functionality**: Provides a comprehensive dashboard with statistics and charts. Users can export their journey as a PDF.
-   **Implementation**:
    -   `routes/progress.py` renders the dashboard.
    -   `utils/progress_helpers.py` aggregates data for charts.
    -   `utils/pdf_generator.py` uses WeasyPrint and Matplotlib to create the PDF.

### 4.4. Goal Setting and Tracking
-   **Functionality**: Users can set, track, and manage weekly goals.
-   **Implementation**:
    -   `routes/goals.py` handles all goal-related logic using the `GoalForm` for validation.
    -   `utils/goal_helpers.py` provides functions for goal management.

---

## 5. How to Run the Application

1.  **Set up a virtual environment**: `python -m venv env && source env/bin/activate`
2.  **Install dependencies**: `pip install -r requirements.txt`
3.  **Create a `.env` file** with a `SECRET_KEY`.
4.  **Run the application**: `python web_app.py`
5.  The application will be available at `http://localhost:5000`.

---

## 6. Development Roadmap

This project follows a prioritized roadmap to ensure stability and security before launch. The full plan can be found in `@250629_suggestions.md`.

-   **Phase 1: Foundational Tooling (Current Focus)**
    -   **1.1. Implement Database Migrations**: Set up `Flask-Migrate` to manage database schema changes safely.
    -   **1.2. Establish a Testing Framework**: Set up `pytest` to create a suite of automated tests.
-   **Phase 2: Hardening & Compliance**
    -   **2.1. Security Hardening**: Implement rate limiting, CSRF protection for AJAX, and run dependency audits.
    -   **2.2. Legal & Compliance (GDPR)**: Add a privacy policy, cookie consent, and data export/deletion features.
-   **Phase 3: Final Polish**
    -   **3.1. Code & File Structure Refinements**: Refactor `web_app.py` to a pure app factory and standardize JS file structure.
    -   **3.2. Database Performance**: Add indexes to frequently queried columns.

---

## 7. Coding Style Guide

The project adheres to a strict set of coding standards to ensure consistency and maintainability. The full guide can be found in `@flask_style_guide.md`.

-   **Python**:
    -   Follows **PEP 8**.
    -   Uses `snake_case` for variables, functions, and modules.
    -   Uses Google-style docstrings and type hints.
-   **HTML**:
    -   Uses semantic HTML5 elements.
    -   Uses `snake_case` for custom IDs and attributes.
-   **JavaScript**:
    -   Uses modern ES6+ features.
    -   Uses `snake_case` for variables and functions to maintain consistency with the Flask backend.
-   **CSS**:
    -   Follows **BEM** (Block, Element, Modifier) methodology for custom components.
    -   Uses CSS custom properties for theming.
-   **Naming Conventions**:
    -   **Files and Directories**: `snake_case`.
    -   **Database Tables**: `snake_case` and plural (e.g., `diary_entries`).
