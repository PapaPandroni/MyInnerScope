# Project Overview: Aim for the Stars

This document provides a comprehensive overview of the "Aim for the Stars" web application, a self-reflection and personal growth tracking tool.

## 1. Project Purpose and Core Functionality

"Aim for the Stars" is a Flask-based web application designed to help users improve themselves through daily reflection. The core functionality revolves around users writing daily diary entries about their behaviors and categorizing them as either "encouraged" or "something to change."

The application gamifies this process by awarding points for entries and tracking daily streaks, motivating users to remain consistent with their self-reflection. A detailed progress dashboard provides visualizations and statistics about the user's journey over time.

## 2. Technology Stack

-   **Backend**: Python with the Flask framework.
-   **Database**: SQLAlchemy ORM, defaulting to a SQLite database (`users.db`).
-   **Frontend**:
    -   Jinja2 for HTML templating.
    -   Bootstrap 5 for styling and layout.
    -   Custom CSS for specific styling.
-   **Client-Side Scripting**:
    -   JavaScript for interactive components on the progress page.
    -   **Chart.js** for data visualization (points over time, weekly performance).
    -   **Luxon** for date/time handling in charts.
-   **PDF Generation**:
    -   **WeasyPrint** to convert HTML/CSS to PDF.
    -   **Matplotlib** to generate static chart images that are embedded into the PDF.
-   **Authentication**: Werkzeug for password hashing and session management.

## 3. Project Structure

The project follows a standard Flask application structure, separating concerns into distinct modules:

-   `web_app.py`: The main application entry point. It uses the factory pattern (`create_app`) to initialize the Flask app, database, and routes.
-   `config.py`: Defines different configuration environments (Development, Production, Testing) and manages secret keys and database URIs.
-   `models/`: Contains the SQLAlchemy database models.
    -   `User`: Stores user credentials.
    -   `DiaryEntry`: Stores the content and rating of each diary entry.
    -   `DailyStats`: A crucial table that tracks daily points, current streak, and longest streak for each user.
-   `routes/`: Defines the application's routes using Flask Blueprints.
    -   `auth.py`: Handles user registration, login, and logout.
    -   `diary.py`: Manages the creation of new diary entries.
    -   `progress.py`: Contains the logic for the main progress dashboard, including data aggregation for charts and statistics.
    -   `reader.py`: Powers the diary reading interface, including navigation and search.
-   `templates/`: Contains all Jinja2 HTML templates for rendering pages.
    -   `pdf/journey.html`: A special template designed specifically for the PDF export.
-   `static/`: Holds all static assets.
    -   `css/`: Stylesheets, including one for the main app and one for the PDF.
    -   `js/`: JavaScript files, modularized for the progress page (`charts.js`, `export.js`, etc.).
-   `utils/`: Utility modules for helper functions.
    -   `pdf_generator.py`: Handles the complex logic of creating the PDF report, including generating charts with Matplotlib and rendering the final file with WeasyPrint.
    -   `search_helpers.py`: Implements the search functionality for the diary reader.

## 4. Key Features and Implementation

### User Authentication
-   Users can register, log in, and log out.
-   Passwords are securely hashed using `werkzeug.security`.
-   User sessions are managed via Flask's session object, storing the `user_id`.

### Diary and Points System
-   The main interaction page (`/diary`) allows users to submit a diary entry and rate it as "encouraged" (+5 points) or "want to change" (+2 points).
-   The system calculates and updates the user's `DailyStats` (points, streaks) with each entry.
-   Streak logic correctly handles consecutive days. If a user writes an entry, the system checks if they wrote one the previous day to decide whether to continue the streak or start a new one.

### Progress Dashboard (`/progress`)
-   This is the most data-rich page, providing a comprehensive overview of the user's activity.
-   **Statistics**: Displays key metrics like "Points Today," "Total Points," "Current Streak," and "Longest Streak."
-   **Points Over Time Chart**: A cumulative line graph showing total points earned over time. The chart is interactive, allowing zoom and pan functionality.
-   **Weekday Performance Chart**: A bar chart showing the average points earned for each day of the week, helping users identify patterns. This chart is only displayed when enough data is available.
-   **Top Days**: Shows the top 3 days with the most points, along with the corresponding diary entries for that day.

### Diary Reader (`/read-diary`)
-   Allows users to read their past entries in a chronological, book-like format.
-   Users can navigate between days with "Previous" and "Next" buttons.
-   **Search**: A robust search feature allows filtering entries by text content and/or a specific date. Search results are displayed with highlighted keywords.

### PDF Export
-   Users can export their entire journey as a downloadable PDF from the progress page.
-   The `pdf_generator.py` utility first creates the charts as PNG images using Matplotlib.
-   These images are Base64-encoded and embedded into the `pdf/journey.html` template.
-   The template is then rendered to a PDF in memory using WeasyPrint and served to the user for download.

## 5. How to Run the Application

1.  **Set up a virtual environment**:
    ```bash
    python -m venv env
    source env/bin/activate
    ```
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Create a `.env` file** in the root directory with a `SECRET_KEY`:
    ```
    SECRET_KEY='your-super-secret-key'
    ```
4.  **Run the application**:
    ```bash
    python web_app.py
    ```
5.  The application will be available at `http://localhost:5000`. The SQLite database (`users.db`) is created automatically on the first run.
