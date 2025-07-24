My Inner Scope 🌟
A self-reflection web application that helps users track their personal growth through daily diary entries and behavioral reflection.

Overview
My Inner Scope is a Flask-based web application designed to encourage self-improvement through daily reflection. Users write short diary entries about their actions and behaviors, then categorize them as either "encouraged behavior" or "something to change." The app gamifies the self-reflection process with points, streaks, and progress tracking.

Features
Current Functionality
User Authentication: Registration and login system with password hashing
Daily Diary Entries: Users can write reflective entries about their day
Behavioral Rating: Each entry is rated as positive behavior (+5 points) or behavior to change (+2 points)
Gamification Elements:
Daily point system
Streak tracking (current and longest)
Progress visualization with interactive charts
Analytics Dashboard:
Points over time (cumulative chart with zoom/pan)
Weekly trend analysis
Day-of-week performance patterns
Top performing days with entry details
Diary Reading: Chronological diary view with navigation between entries
SEO & Analytics: ⭐ **ACTIVE**
Comprehensive search engine optimization with keyword-rich titles and optimized meta descriptions
Google Analytics 4 integration with GDPR-compliant cookie consent (live tracking)
Google Search Console integration for performance monitoring
Social media sharing optimization with Twitter Cards and Open Graph
XML sitemap and robots.txt for search engine crawling
Multi-format favicon system for all devices and platforms
External authority links for E-A-T (Expertise, Authoritativeness, Trustworthiness) signals
Technical Stack
Backend: Flask with application factory pattern, SQLAlchemy ORM, Flask-Migrate
Database: SQLite (development), PostgreSQL (production)
Frontend: Bootstrap 5, Chart.js for visualizations, wordcloud2.js
Authentication: Werkzeug password hashing with session-based auth
Security: Flask-WTF CSRF protection, Flask-Limiter rate limiting
Testing: Pytest with Flask-testing integration and coverage reporting
Deployment: Gunicorn WSGI server with Railway/Heroku support
Installation & Setup
Requirements
Python 3.x
Virtual environment (recommended)
Dependencies
blinker==1.9.0
click==8.1.8
Flask==3.1.0
Flask-SQLAlchemy==3.1.1
greenlet==3.2.2
itsdangerous==2.2.0
Jinja2==1.1.6
MarkupSafe==3.0.2
SQLAlchemy==2.0.41
typing_extensions==4.13.2
Werkzeug==3.1.3
Setup Instructions
Clone the repository
Create and activate a virtual environment:
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:
bash
pip install -r requirements.txt
Create a `.env` file for environment variables:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///users.db
FLASK_ENV=development

# Optional: Analytics Integration
GOOGLE_ANALYTICS_ID=your-google-analytics-id
GOOGLE_SEARCH_CONSOLE_ID=your-search-console-id
```

Run the application:
bash
python run.py
Open your browser to http://localhost:5000
The SQLite database (users.db) will be created automatically on first run.

Database Schema

The application uses the following SQLAlchemy models for its database schema:

### User Table (`users`)
- `id`: Primary key (Integer)
- `email`: Unique user email (String)
- `_password`: Hashed password (String, internal representation)
- `user_name`: Optional display name (String)

### DiaryEntry Table (`diary_entry`)
- `id`: Primary key (Integer)
- `user_id`: Foreign key to User (Integer)
- `entry_date`: Date of entry (Date, defaults to today)
- `content`: Text content of the diary entry (Text)
- `rating`: Integer (`-1` for "want to change", `1` for "encouraged")

### DailyStats Table (`daily_stats`)
- `id`: Primary key (Integer)
- `user_id`: Foreign key to User (Integer)
- `date`: Date of the stats record (Date)
- `points`: Points earned that day (Integer, default 0)
- `current_streak`: Current consecutive day streak (Integer, default 0)
- `longest_streak`: All-time longest streak (Integer, default 0)
- `user_date_uc`: Unique constraint on `user_id` and `date`

### Goal Table (`goals`)
- `id`: Primary key (Integer)
- `user_id`: Foreign key to User (Integer)
- `category`: Enum (`GoalCategory`: Exercise, Learning, Mindfulness, Social, Productivity, Personal Development, Home, Creative, Custom)
- `title`: Goal title (String)
- `description`: Optional goal description (Text)
- `week_start`: Start date of the goal week (Date)
- `week_end`: End date of the goal week (Date)
- `created_at`: Timestamp of goal creation (DateTime)
- `status`: Enum (`GoalStatus`: active, completed, failed, default active)
- `progress_notes`: Optional notes on goal progress (Text)
Project Status
🚧 Work in Progress - This is an active development project with ongoing improvements.


Contributing
This project is primarily for personal development and documentation purposes. The codebase serves as a learning project for Flask web development and user behavior gamification.

## License & Copyright

Aim for the Stars is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

Copyright 2025 Peremil Starklint Söderström. All rights reserved.

The unique combination of daily reflection, behavioral rating, and gamified self-improvement tracking represents the original creative work of the author.

## Supporting This Project

This project is provided free of charge. If you find it helpful for your self-improvement journey, consider supporting its development through donations at [https://buymeacoffee.com/papapandroni](https://buymeacoffee.com/papapandroni).


"Aim for the Stars"

## Dependency Security Checks

This project uses two tools to check for known security vulnerabilities in its Python dependencies:

- **safety**: Checks installed packages for known vulnerabilities.
- **pip-audit**: Audits dependencies for security issues using the Python Advisory Database.

### How to Run Security Checks Locally

1. Install dependencies (if not already):
   ```bash
   pip install -r requirements.txt
   pip install pip-audit
   ```
2. Run safety:
   ```bash
   safety check
   ```
3. Run pip-audit:
   ```bash
   pip-audit
   ```

### Automated Checks with GitHub Actions

Every time you push code or open a pull request, GitHub Actions will automatically run both `safety` and `pip-audit` to check for vulnerabilities. Results will appear in the "Checks" tab on GitHub. If issues are found, you will see a warning, but you can still merge your code. This helps you stay aware of security issues in your dependencies.

