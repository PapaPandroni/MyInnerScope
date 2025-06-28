# Refactoring Plan: Aligning with the Flask Style Guide

This document outlines a detailed plan to refactor the "Aim for the Stars" web application to align with the provided `flask_style_guide.md`. The refactoring is broken down into sequential, reviewable parts to ensure a smooth transition without affecting functionality.

## Part 1: Project Structure and File Naming

This part focuses on restructuring the project directory and renaming files to match the style guide's recommendations.

**Tasks:**

1.  **Create `app` directory:**
    *   Create a new directory named `app` in the project root.
2.  **Move core application files into `app`:**
    *   Move the following files and directories into the `app` directory:
        *   `config.py`
        *   `models/`
        *   `routes/`
        *   `static/`
        *   `templates/`
        *   `utils/`
        *   `web_app.py` -> `app/run.py`
3.  **Rename files and directories to `snake_case`:**
    *   Rename `models/daily_stats.py` to `models/daily_stat.py`.
    *   Rename `models/diary_entry.py` to `models/diary_entry.py`.
    *   Rename `models/user.py` to `models/user.py`.
    *   Rename `routes/auth.py` to `routes/auth.py`.
    *   Rename `routes/diary.py` to `routes/diary.py`.
    *   Rename `routes/goals.py` to `routes/goals.py`.
    *   Rename `routes/progress.py` to `routes/progress.py`.
    *   Rename `routes/reader.py` to `routes/reader.py`.
    *   Rename `static/css/custom_css.css` to `static/css/main.css`.
    *   Rename `static/js/progress/` to `static/js/dashboard/`.
    *   Rename `static/js/dashboard/charts.js` to `static/js/dashboard/dashboard_charts.js`.
    *   Rename `static/js/dashboard/entries.js` to `static/js/dashboard/dashboard_entries.js`.
    *   Rename `static/js/dashboard/entry-toggles.js` to `static/js/dashboard/dashboard_entry_toggles.js`.
    *   Rename `static/js/dashboard/export.js` to `static/js/dashboard/dashboard_export.js`.
    *   Rename `static/js/dashboard/main.js` to `static/js/dashboard/dashboard_main.js`.
    *   Rename `templates/read_diary.html` to `templates/reader.html`.
    *   Rename `utils/goal_helpers.py` to `utils/goal_helper.py`.
    *   Rename `utils/pdf_generator.py` to `utils/pdf_generator.py`.
    *   Rename `utils/progress_helpers.py` to `utils/progress_helper.py`.
    *   Rename `utils/search_helpers.py` to `utils/search_helper.py`.
4.  **Update `GEMINI.md`:**
    *   Reflect the new project structure and file names in the `GEMINI.md` file.

## Part 2: Python Code Style

This part focuses on bringing the Python code in line with the style guide.

**Tasks:**

1.  **Apply Black code formatter:**
    *   Run `black .` on the entire project to enforce the 88-character line limit and other PEP 8 standards.
2.  **Refactor names to `snake_case`:**
    *   Go through all Python files and rename variables and functions from `camelCase` to `snake_case`.
3.  **Add type hints:**
    *   Add type hints to all function definitions in the application.
4.  **Update docstrings to Google-style:**
    *   Convert all existing docstrings to the Google-style format as specified in the style guide.

## Part 3: Route and Helper Organization

This part focuses on restructuring the `routes` and `utils` directories to group route-specific logic.

**Tasks:**

1.  **Create feature-based route packages:**
    *   In the `app/routes/` directory, create subdirectories for each feature: `auth`, `diary`, `goals`, `progress`, and `reader`.
    *   Each subdirectory should contain an `__init__.py`, `routes.py`, and `helpers.py`.
2.  **Move route logic:**
    *   Move the Flask Blueprint definitions and route handlers from the existing route files into the new `routes.py` files within their respective feature packages.
3.  **Move helper functions:**
    *   Move the helper functions from the `app/utils/` directory into the corresponding `helpers.py` files in each feature package. For example, `progress_helper.py` functions will go into `app/routes/progress/helpers.py`.
4.  **Update imports:**
    *   Update all imports throughout the application to reflect the new locations of routes and helpers.

## Part 4: Static and Template File Organization

This part reorganizes the `static` and `templates` directories for better structure.

**Tasks:**

1.  **Organize CSS and JS by feature:**
    *   In `app/static/css/`, create `auth.css`, `dashboard.css`, and `goals.css`.
    *   In `app/static/js/`, create `auth.js`, `dashboard.js`, and `goals.js`.
    *   Move the content of the existing CSS and JS files into the new feature-specific files.
2.  **Organize templates by feature:**
    *   In `app/templates/`, create subdirectories for `auth`, `dashboard`, `diary`, `goals`, and `reader`.
    *   Move the corresponding HTML files into these new subdirectories.
3.  **Update file paths in templates:**
    *   Update all `url_for()` calls in the HTML templates to point to the new locations of static files.
    *   Update all `render_template()` calls in the Python code to point to the new locations of the HTML templates.

## Part 5: HTML and JavaScript Style

This part applies the style guide's conventions to the HTML and JavaScript code.

**Tasks:**

1.  **Update HTML attributes:**
    *   In all HTML files, change `id` and custom `data-*` attributes from `kebab-case` or `camelCase` to `snake_case`.
2.  **Update JavaScript variables and functions:**
    *   In all JavaScript files, refactor variable and function names from `camelCase` to `snake_case`.
    *   Update references to HTML elements to use the new `snake_case` IDs.

## Part 6: Database Refactoring

This part aligns the database schema with the naming conventions in the style guide.

**Tasks:**

1.  **Update model definitions:**
    *   In the `app/models/` files, update the `__tablename__` for each model to be `snake_case` and plural (e.g., `users`, `diary_entries`).
    *   Update all column names to be `snake_case`.
2.  **Create a database migration script:**
    *   Since this is a live application, create a migration script (e.g., using Alembic, or a simple Python script) to rename the tables and columns in the `users.db` SQLite database. This will preserve the existing data.
3.  **Update database queries:**
    *   Update all SQLAlchemy queries in the application to use the new table and column names.

## Part 7: Final Review and Cleanup

This final part ensures that all changes have been applied correctly and that the application is stable.

**Tasks:**

1.  **Run tests:**
    *   If there are any tests, run them to ensure that no functionality has been broken. If not, manually test all features of the application.
2.  **Review the entire codebase:**
    *   Do a final pass over the entire codebase to check for any remaining inconsistencies with the style guide.
3.  **Remove old files:**
    *   Delete any empty or now-unused files and directories.
4.  **Update `README.md`:**
    *   Update the `README.md` file to reflect the new project structure and any changes to the setup or running of the application.
