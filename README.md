Aim for the Stars 🌟
A self-reflection web application that helps users track their personal growth through daily diary entries and behavioral reflection.

Overview
Aim for the Stars is a Flask-based web application designed to encourage self-improvement through daily reflection. Users write short diary entries about their actions and behaviors, then categorize them as either "encouraged behavior" or "something to change." The app gamifies the self-reflection process with points, streaks, and progress tracking.

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
Technical Stack
Backend: Flask, SQLAlchemy
Database: SQLite
Frontend: Bootstrap 5, Chart.js
Authentication: Werkzeug password hashing
Visualization: Chart.js with Luxon for time handling
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
Run the application:
bash
python web_app.py
Open your browser to http://localhost:5000
The SQLite database (users.db) will be created automatically on first run.

Database Schema
User Table
id: Primary key
email: Unique user email
password: Hashed password
user_name: Optional display name
DiaryEntry Table
id: Primary key
user_id: Foreign key to User
entry_date: Date of entry (defaults to today)
content: Text content of the diary entry
rating: Integer (-1 for "want to change", 1 for "encouraged")
DailyStats Table
id: Primary key
user_id: Foreign key to User
date: Date of the stats record
points: Points earned that day
current_streak: Current consecutive day streak
longest_streak: All-time longest streak
Project Status
🚧 Work in Progress - This is an active development project with ongoing improvements.

Planned Features
Dashboard Enhancements
Weekly/monthly comparison views
Missed days analysis (90-day lookback)
Enhanced chart styling and interactions
User Experience Improvements
Email verification and password reset
Profile customization options
Dark/light mode toggle
Password strength validation
User-friendly error handling
Onboarding tour for new users
New Functionality
Search functionality for specific diary entries
Data export capabilities
Goal setting features
Weekly reflection prompts
Advanced analytics and insights
Technical Improvements
Input validation and sanitization
Comprehensive error handling
Rate limiting
Performance optimizations
Contributing
This project is primarily for personal development and documentation purposes. The codebase serves as a learning project for Flask web development and user behavior gamification.

## License & Copyright

Aim for the Stars is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

Copyright 2025 Peremil Starklint Söderström. All rights reserved.

The unique combination of daily reflection, behavioral rating, and gamified self-improvement tracking represents the original creative work of the author.

## Supporting This Project

This project is provided free of charge. If you find it helpful for your self-improvement journey, consider supporting its development through donations at [Coming soon].


"Aim for the stars, even if you miss, you'll land among the clouds."

