# Project Overview: Aim for the Stars

This document provides a comprehensive overview of the "Aim for the Stars" web application, a self-reflection and personal growth tracking tool. It is designed to serve as a detailed reference for an AI, minimizing misunderstandings during refactoring, restructuring, or feature development tasks.

## 1. Project Purpose and Core Functionality

"Aim for the Stars" is a Flask-based web application designed to help users improve themselves through daily reflection and goal setting. The core functionality revolves around users writing daily diary entries about their behaviors and categorizing them as either "encouraged" or "something to change."

The application gamifies this process by awarding points for entries and tracking daily streaks, motivating users to remain consistent with their self-reflection. A detailed progress dashboard provides visualizations and statistics about the user's journey over time. Additionally, users can set and track weekly goals, further enhancing their personal development journey.

## 2. Technology Stack

-   **Backend**: Python with the Flask framework (version 3.1.0).
-   **Database**: SQLAlchemy ORM (version 2.0.41), defaulting to a SQLite database (`users.db`).
-   **Frontend**:
    -   Jinja2 (version 3.1.6) for HTML templating.
    -   Bootstrap 5 for responsive styling and layout.
    -   Custom CSS (`static/css/custom_css.css`, `static/css/progress.css`, `static/css/goals.css`, `static/css/pdf_journey.css`) for specific styling and theming (sci-fi inspired).
-   **Client-Side Scripting**:
    -   JavaScript for interactive components.
    -   **Chart.js** (version 4.4.9) for data visualization (points over time, weekly performance).
    -   **Luxon** (version 3.4.0) for date/time handling in charts (via `chartjs-adapter-luxon`).
    -   **chartjs-plugin-zoom** (version 2.0.1) for interactive chart zooming and panning.
-   **PDF Generation**:
    -   **WeasyPrint** (version 52.5) to convert HTML/CSS to PDF.
    -   **Matplotlib** (version 3.8.3) to generate static chart images that are embedded into the PDF.
    -   **CairoSVG** (version 2.8.2) and **cairocffi** (version 1.7.1) for SVG rendering in PDF generation.
-   **Authentication**: Werkzeug (version 3.1.3) for password hashing (`generate_password_hash`, `check_password_hash`) and session management.
-   **Environment Management**: `python-dotenv` (version 1.1.0) for loading environment variables from a `.env` file.

## 3. Project Structure

The project follows a standard Flask application structure, separating concerns into distinct modules:

-   `web_app.py`: The main application entry point. It uses the factory pattern (`create_app`) to initialize the Flask app, database, and routes. It also defines the root (`/`) route.
-   `config.py`: Defines different configuration environments (Development, Production, Testing) using classes (`Config`, `DevelopmentConfig`, `ProductionConfig`, `TestingConfig`). It manages `SECRET_KEY` and `SQLALCHEMY_DATABASE_URI` and includes a validation method for required environment variables.
-   `models/`: Contains the SQLAlchemy database models and the database instance.
    -   `database.py`: Initializes the `SQLAlchemy` instance (`db`).
    -   `User.py`: Defines the `User` model (id, email, password, user_name).
    -   `DiaryEntry.py`: Defines the `DiaryEntry` model (id, user_id, entry_date, content, rating).
    -   `DailyStats.py`: Defines the `DailyStats` model (id, user_id, date, points, current_streak, longest_streak). This table has a unique constraint on `user_id` and `date`.
    -   `goal.py`: Defines the `Goal` model (id, user_id, category, title, description, week_start, week_end, created_at, status, progress_notes). Includes `GoalCategory` and `GoalStatus` enums, and properties/methods for goal management (e.g., `is_current`, `days_remaining`, `progress_percentage`, `get_goal_dates`).
    -   `__init__.py`: Imports all models and the `db` instance, making them easily accessible.
-   `routes/`: Defines the application's routes using Flask Blueprints.
    -   `__init__.py`: Contains `register_blueprints` function to register all route blueprints with the Flask app.
    -   `auth.py`: Handles user registration (`/register`), login (`/login`), and logout (`/logout`). Manages password hashing and session creation.
    -   `diary.py`: Manages the creation of new diary entries (`/diary`). Includes logic for updating `DailyStats` (points, streaks) based on entry rating.
    -   `progress.py`: Contains the logic for the main progress dashboard (`/progress`), including data aggregation for charts and statistics. Also handles the PDF export (`/export-journey`).
    -   `reader.py`: Powers the diary reading interface (`/read-diary`), including navigation between entries and search functionality.
    -   `goals.py`: Manages goal-related routes (`/goals`, `/goals/create`, `/goals/<int:goal_id>/update`, `/goals/<int:goal_id>/complete`, `/goals/<int:goal_id>/fail`). Includes API endpoints for goal suggestions and current goals.
-   `templates/`: Contains all Jinja2 HTML templates for rendering pages.
    -   `base.html`: The base template providing common structure (navbar, footer, Bootstrap, custom CSS).
    -   `_navbar.html`: Partial template for the navigation bar, dynamically adjusting links based on user session.
    -   `index.html`: Landing page.
    -   `login.html`: User login form.
    -   `register.html`: User registration form.
    -   `diary.html`: Page for creating new diary entries and viewing recent ones.
    -   `progress.html`: Main progress dashboard displaying statistics and charts.
    -   `read_diary.html`: Interface for reading past diary entries, with navigation and search.
    -   `goals.html`: Page for setting, tracking, and managing weekly goals.
    -   `pdf/journey.html`: A special template designed specifically for the PDF export, optimized for print.
-   `static/`: Holds all static assets.
    -   `assets/`: Contains images (e.g., `starry_sky.jpg`).
    -   `css/`: Stylesheets, including `custom_css.css` (general styling), `goals.css` (goal-specific styling), `pdf_journey.css` (PDF print styling), and `progress.css` (progress page styling with sci-fi theme).
    -   `js/`: JavaScript files, modularized for different functionalities.
        -   `goals.js`: Client-side logic for the goals page (suggestions, form validation, animations).
        -   `progress/`: Directory for progress page JavaScript.
            -   `main.js`: Main entry point for progress page JS, initializes other modules.
            -   `charts.js`: Handles Chart.js initialization for points and weekday charts.
            -   `entries.js`: Manages expanding/collapsing diary entries on the progress page.
            -   `entry-toggles.js`: Provides a global function for toggling entry visibility.
            -   `export.js`: Handles PDF export button click and loading overlay.
-   `utils/`: Utility modules for helper functions.
    -   `__init__.py`: Imports and exposes utility functions.
    -   `pdf_generator.py`: Handles the complex logic of creating the PDF report, including generating charts with Matplotlib and rendering the final file with WeasyPrint.
    -   `progress_helpers.py`: Contains functions for aggregating and retrieving data for the progress dashboard (e.g., `get_total_points`, `get_weekday_data`, `get_trend_message`).
    -   `search_helpers.py`: Implements the search functionality for the diary reader, including snippet creation and highlighting.
    -   `goal_helpers.py`: Provides helper functions for goal management (e.g., `get_current_goals`, `create_goal`, `complete_goal`, `get_predefined_goals`).

## 4. Key Features and Implementation

### 4.1. User Authentication

-   **Functionality**: Users can register, log in, and log out.
-   **Implementation**:
    -   `routes/auth.py` handles the routes.
    -   Passwords are securely hashed using `werkzeug.security.generate_password_hash` during registration and verified with `check_password_hash` during login.
    -   User sessions are managed via Flask's `session` object, storing the `user_id`.
    -   Upon successful login, a `DailyStats` entry for the current day is created if it doesn't exist, ensuring initial points for the day.

### 4.2. Diary and Points System

-   **Functionality**: Users submit daily diary entries and categorize them as "encouraged" or "want to change," earning points.
-   **Implementation**:
    -   `routes/diary.py` manages the `/diary` route.
    -   `models/DiaryEntry.py` stores the entry content and rating.
    -   `models/DailyStats.py` tracks daily points, current streak, and longest streak.
    -   **Points Calculation**: "Encouraged" behaviors award +5 points, "Want to change" behaviors award +2 points.
    -   **Streak Logic**: When a new entry is submitted, the system checks if an entry was made the previous day to continue or start a new streak. `current_streak` and `longest_streak` in `DailyStats` are updated accordingly.

### 4.3. Progress Dashboard (`/progress`)

-   **Functionality**: Provides a comprehensive overview of the user's activity, including statistics, cumulative points chart, and weekday performance chart.
-   **Implementation**:
    -   `routes/progress.py` renders the `progress.html` template.
    -   `utils/progress_helpers.py` contains functions to fetch and process data:
        -   `get_today_stats`, `get_total_points`, `get_current_streak`, `get_longest_streak`, `get_total_entries`.
        -   `get_points_data`: Returns cumulative points over time for the Chart.js line graph.
        -   `get_weekday_data`: Calculates average points per day of the week for the Chart.js bar chart. It also determines if there's "sufficient data" (at least 2 days with entries) to display meaningful insights, otherwise a placeholder is shown.
        -   `get_trend_message`: Provides a textual trend analysis based on points earned in the last two weeks.
        -   `get_top_days_with_entries`: Fetches the top 3 days with the highest points and their associated diary entries.
    -   `static/js/progress/main.js` initializes the progress page.
    -   `static/js/progress/charts.js` uses Chart.js, Luxon, and chartjs-plugin-zoom to render interactive charts.
    -   `static/js/progress/entries.js` and `static/js/progress/entry-toggles.js` handle the "Show more/less" functionality for long diary entries in the "Top Days" section.
    -   `static/css/progress.css` provides a sci-fi themed visual design for the dashboard elements.

### 4.4. Diary Reader (`/read-diary`)

-   **Functionality**: Allows users to read their past entries chronologically, navigate between days, and search for specific content or dates.
-   **Implementation**:
    -   `routes/reader.py` handles the `/read-diary` route.
    -   It fetches all dates with entries for navigation.
    -   **Navigation**: Users can move to the previous or next day with entries.
    -   **Search**:
        -   `utils/search_helpers.py` contains `handle_search` and `create_search_snippet`.
        -   `handle_search` filters entries by text content (case-insensitive) and/or specific dates.
        -   `create_search_snippet` generates short excerpts of matching entries, highlighting the search term.
    -   The `read_diary.html` template dynamically renders either a front page, search results, or a specific day's entries.

### 4.5. PDF Export

-   **Functionality**: Users can export their entire self-reflective journey as a downloadable PDF from the progress page.
-   **Implementation**:
    -   `routes/progress.py` handles the `/export-journey` POST request.
    -   `utils/pdf_generator.py` orchestrates the PDF creation:
        -   It uses `matplotlib` to generate static PNG images of the "Points Over Time" and "Average Points by Day" charts. These images are Base64-encoded and embedded into the HTML.
        -   It renders the `templates/pdf/journey.html` template, which is specifically designed for print layout.
        -   `WeasyPrint` converts the rendered HTML (with embedded images and `static/css/pdf_journey.css`) into a PDF document.
        -   The PDF is served as an attachment to the user.
    -   `static/js/progress/export.js` manages the client-side interaction, showing a loading overlay during PDF generation and handling the download.

### 4.6. Goal Setting and Tracking

-   **Functionality**: Users can set weekly goals, track their progress, and mark goals as completed or failed.
-   **Implementation**:
    -   `routes/goals.py` handles all goal-related routes and API endpoints.
    -   `models/goal.py` defines the `Goal` model, `GoalCategory` enum (e.g., Exercise, Learning, Mindfulness), and `GoalStatus` enum (Active, Completed, Failed). It also includes methods for calculating goal duration and progress.
    -   `utils/goal_helpers.py` provides helper functions:
        -   `create_goal`: Creates a new goal, defaulting to a 7-day period from the creation date.
        -   `get_current_goals`: Retrieves active goals for the current week.
        -   `get_overdue_goals`: Identifies active goals whose `week_end` date has passed.
        -   `update_goal_progress`: Allows updating notes for a goal.
        -   `complete_goal`, `fail_goal`: Change the status of a goal. Completing a goal awards +10 points, failing awards +1 point (recorded in `DailyStats`).
        -   `get_goal_history`: Fetches recent past goals.
        -   `get_goal_stats`: Provides overall statistics on goals (total, completed, failed, completion rate).
        -   `get_predefined_goals`: Returns a dictionary of suggested goal titles for each category.
    -   `templates/goals.html` provides the user interface for goal management.
    -   `static/js/goals.js` handles client-side interactions like dynamic goal suggestions based on category, form validation, and basic animations.
    -   The progress page (`progress.html`) displays the user's primary active goal (the one ending soonest) or prompts them to create one.

## 5. How to Run the Application

1.  **Set up a virtual environment**:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows: `env\Scripts\activate`
    ```
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Create a `.env` file** in the root directory (`/home/peremil/Documents/repos/web_server/web_server/`) with a `SECRET_KEY`:
    ```
    SECRET_KEY='your-super-secret-key-here'
    # Optional: For development, you can specify a dev database
    # DEV_DATABASE_URL='sqlite:///dev_users.db'
    # Optional: For production, you can specify a production database
    # DATABASE_URL='sqlite:///prod_users.db'
    ```
4.  **Run the application**:
    ```bash
    python web_app.py
    ```
5.  The application will be available at `http://localhost:5000`. The SQLite database (`users.db`) is created automatically on the first run if it doesn't exist.

## 6. Database Schema

The application uses the following SQLAlchemy models, which map to tables in the SQLite database (`users.db`):

### `User` Table

-   `id` (Integer, Primary Key): Unique identifier for the user.
-   `email` (String, 120 chars, Unique, Not Null): User's email address, used for login.
-   `password` (String, 120 chars, Not Null): Hashed password.
-   `user_name` (String, 200 chars, Nullable): Optional display name for the user.

### `DiaryEntry` Table

-   `id` (Integer, Primary Key): Unique identifier for the diary entry.
-   `user_id` (Integer, Foreign Key to `User.id`, Not Null): Links the entry to a specific user.
-   `entry_date` (Date, Default: `date.today()`, Not Null): The date the entry was made.
-   `content` (Text, Not Null): The actual text content of the diary entry.
-   `rating` (Integer, Not Null): The rating of the entry (-1 for "want to change", 1 for "encouraged").

### `DailyStats` Table

-   `id` (Integer, Primary Key): Unique identifier for the daily statistics record.
-   `user_id` (Integer, Foreign Key to `User.id`, Not Null): Links the stats to a specific user.
-   `date` (Date, Not Null): The date for which these statistics apply.
-   `points` (Integer, Default: 0): Total points earned on this specific day.
-   `current_streak` (Integer, Default: 0): The current consecutive day streak ending on this date.
-   `longest_streak` (Integer, Default: 0): The longest streak achieved by the user up to this date.
-   **Unique Constraint**: (`user_id`, `date`): Ensures only one stats record per user per day.

### `Goal` Table

-   `id` (Integer, Primary Key): Unique identifier for the goal.
-   `user_id` (Integer, Foreign Key to `User.id`, Not Null): Links the goal to a specific user.
-   `category` (Enum `GoalCategory`, Not Null): The category of the goal (e.g., EXERCISE, LEARNING).
-   `title` (String, 200 chars, Not Null): A concise title for the goal.
-   `description` (Text, Nullable): A more detailed description of the goal.
-   `week_start` (Date, Not Null): The start date of the goal's tracking period.
-   `week_end` (Date, Not Null): The end date of the goal's tracking period (typically 6 days after `week_start`).
-   `created_at` (DateTime, Default: `datetime.utcnow`): Timestamp when the goal was created.
-   `status` (Enum `GoalStatus`, Default: `ACTIVE`): The current status of the goal (ACTIVE, COMPLETED, FAILED).
-   `progress_notes` (Text, Nullable): Notes on the user's progress towards the goal.

## 7. Planned Features (Future Enhancements)

The following features are planned for future development:

-   **Dashboard Enhancements**:
    -   Weekly/monthly comparison views for points and activity.
    -   Analysis of missed days (e.g., 90-day lookback).
    -   Enhanced chart styling and interactions.
-   **User Experience Improvements**:
    -   Email verification and password reset functionality.
    -   Profile customization options.
    -   Dark/light mode toggle.
    -   Password strength validation during registration.
    -   More user-friendly error handling.
    -   Onboarding tour for new users.
-   **New Functionality**:
    -   More advanced search functionality for diary entries.
    -   Data export capabilities beyond PDF (e.g., CSV).
    -   More sophisticated goal setting features (e.g., recurring goals, long-term goals).
    -   Weekly reflection prompts.
    -   Advanced analytics and insights based on user data.
-   **Technical Improvements**:
    -   Input validation and sanitization across all forms.
    -   Comprehensive error handling and logging.
    -   Rate limiting for API endpoints.
    -   Performance optimizations for database queries and rendering.