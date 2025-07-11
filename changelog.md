# Changelog

## 76f698752134b464f8194b7045ffd5f9babe0422
**Author**: Peremil
**Date**: Fri Jul 11 15:59:37 2025 +0200
**Message**: added tests specifically the JavaScript-HTML integration, DOM element validation, and user interface components like forms, charts, and interactive elements.
**Summary**: Major template reorganization moving files into categorized subdirectories, reorganized static assets, and added comprehensive frontend testing suite including `tests/test_frontend_regression.py`, `tests/test_html_structure.py`, `tests/test_template_integration.py`, and `tests/test_routes/test_goals.py`.
**Detailed Description**: This commit represents a significant architectural improvement with two main components. First, it reorganizes the entire template and static file structure by moving templates into categorized subdirectories (auth/, diary/, goals/, main/, etc.) and reorganizing static assets similarly. This improves code organization and maintainability. Second, it introduces a comprehensive frontend testing strategy with over 1,500 lines of new test code covering JavaScript-HTML integration, DOM element validation, template rendering, and user interface components. The testing suite includes regression tests, HTML structure validation, template integration tests, and comprehensive goal functionality testing. This change significantly enhances code quality and ensures UI consistency across the application.

## 2e2a9a51e2696b2329d0e4e10396654de9418975
**Author**: Peremil
**Date**: Thu Jul 10 12:40:59 2025 +0200
**Message**: fix: Correct weekday chart unlock logic to require diary entries
**Summary**: Modified `app/utils/progress_helpers.py` and `tests/test_utils/test_progress_helpers.py`.
**Detailed Description**: This commit fixes a logic issue in the weekday insights chart where the unlock condition was based on daily stats rather than actual diary entries. The chart now properly unlocks when users have diary entries on 2 or more different weekdays, which aligns better with the application's core functionality of diary writing. This change ensures that users who write diary entries but may not have accumulated daily stats (due to system changes or data migration) can still access the weekday insights feature. The fix maintains comprehensive point data display once unlocked and includes thorough testing for edge cases.

## 1f96ba2e66705ddb5628f441645322b2a35ef748
**Author**: Peremil
**Date**: Thu Jul 10 12:23:29 2025 +0200
**Message**: fix: Fix weekday insights progress tracking
**Summary**: Modified `app/routes/progress.py`, `app/templates/progress.html`, `app/utils/progress_helpers.py`, and `tests/test_utils/test_progress_helpers.py`.
**Detailed Description**: This commit addresses an issue where the weekday insights feature showed a hardcoded "0/2 days completed" message regardless of actual user progress. The fix introduces a new helper function `get_unique_weekdays_with_entries()` that accurately counts how many different weekdays have diary entries, and updates the progress template to display dynamic progress like "1/2 days completed". The change also relaxes the requirement from 2+ entries per day to 1+ entry per day, making the feature more accessible to users. Comprehensive tests ensure the function works correctly across all scenarios, improving the user experience by providing accurate progress feedback.

## 54bf8f2fef5b8d8e953a8fe8318e8af434a5dcf1
**Author**: Peremil
**Date**: Thu Jul 10 11:57:06 2025 +0200
**Message**: reordered the progress page
**Summary**: Modified `app/templates/progress.html`.
**Detailed Description**: This commit reorganizes the layout of the progress page to improve user experience and information hierarchy. The sections were reordered to create a more logical flow, likely moving the most important or frequently accessed information to more prominent positions on the page. This type of UX improvement helps users find key information more efficiently and creates a better overall experience when reviewing their progress and statistics.

## a13278b4e2ded17aeda7bdc9f26bf5730c9f86b9
**Author**: Peremil
**Date**: Thu Jul 10 11:50:26 2025 +0200
**Message**: feat: Add post-submission UI to diary
**Summary**: Modified `app/routes/diary.py` and `app/templates/diary.html`.
**Detailed Description**: This commit enhances the user experience by adding a post-submission success interface to the diary entry page. After users submit a diary entry, they now see a confirmation message or updated UI state that acknowledges their submission. This improvement provides immediate feedback to users, confirming that their diary entry was successfully saved to the database. The feature helps users understand that their action was completed successfully and improves the overall user experience by providing clear interaction feedback.

## 3a16ccd2686adfdaf590cbfd41229834f93d76c3
**Author**: Peremil
**Date**: Thu Jul 10 11:43:12 2025 +0200
**Message**: feat: Add rating filter to diary search
**Summary**: Modified `app/templates/read_diary.html`.
**Detailed Description**: This commit adds filtering capability to the diary reading interface, allowing users to filter their diary entries by rating (positive behaviors vs. behaviors to change). This feature enhances the diary search functionality by enabling users to focus on specific types of entries based on their behavioral ratings. Users can now easily review all their positive behaviors or areas for improvement separately, making the diary more useful for self-reflection and progress tracking. This aligns with the application's core mission of behavioral self-improvement and goal tracking.

## 269ff06835f8a670262909001d4e15a5e3a772e0
**Author**: Peremil
**Date**: Thu Jul 10 11:29:54 2025 +0200
**Message**: Merge branch 'feature/onboarding-tour' into main
**Summary**: Merged the onboarding tour feature branch with extensive changes including tour controller, CSS, and template modifications.
**Detailed Description**: This commit merges the completed onboarding tour feature into the main branch. The merge brings together all the components of an interactive user onboarding system, including the tour controller JavaScript, custom CSS styling, and template modifications across multiple pages. This represents the completion of a significant feature that helps new users understand and navigate the application effectively. The onboarding tour likely guides users through key features like writing diary entries, setting goals, and viewing progress, improving user adoption and engagement.

## c0635013f8b9fa28a995c4dfd793eb00948d6a31
**Author**: Peremil
**Date**: Thu Jul 10 10:36:46 2025 +0200
**Message**: changed two tests to assert correct card text
**Summary**: Modified `tests/test_routes/test_progress.py`.
**Detailed Description**: This commit fixes test assertions to match the actual text content displayed in the progress page cards. This type of change typically occurs when the UI text has been updated but the corresponding tests weren't updated to match. By correcting these test assertions, the commit ensures that the test suite accurately validates the current user interface text, maintaining test reliability and preventing false failures. This demonstrates good testing hygiene and ensures the test suite remains accurate and useful for catching real issues.

## d749fa035943b2b1abe3d1ea0c432bdb5fec7235
**Author**: Peremil
**Date**: Thu Jul 10 10:12:43 2025 +0200
**Message**: added onboarding tour
**Summary**: Modified multiple files including `app/static/css/tour.css`, `app/static/js/tour/tour-controller.js`, templates across multiple pages, and updated SPMP documentation.
**Detailed Description**: This commit implements the core onboarding tour functionality, creating an interactive guide system for new users. The tour system includes custom CSS for visual styling, a comprehensive JavaScript tour controller that manages the tour flow across different pages, and template modifications to support tour integration. The tour helps new users understand the application's key features and how to use them effectively. This is a significant user experience enhancement that reduces the learning curve for new users and increases user engagement by providing guided discovery of the application's features. The tour likely covers diary writing, goal setting, and progress tracking workflows.

## 15899971b43da2479cee81e6557917bd30c67d0d
**Author**: Peremil
**Date**: Thu Jul 10 07:54:00 2025 +0200
**Message**: added claude files in all subdirectories
**Summary**: Added 20 CLAUDE.md documentation files across all major subdirectories of the application.
**Detailed Description**: This commit creates comprehensive documentation for AI-assisted development by adding CLAUDE.md files throughout the codebase. Each subdirectory now contains detailed documentation explaining its purpose, structure, and key components. This includes documentation for models (database schema), routes (API endpoints), static assets (frontend resources), templates (UI components), utilities (helper functions), tests (testing strategy), and migrations (database changes). These documentation files serve as a knowledge base for AI assistants working on the codebase, providing context about each component's role and implementation patterns. This documentation strategy significantly improves code maintainability and helps maintain consistency in AI-assisted development.

## 4c557d92a65827448e1f07f8dbe5d1d00df4331d
**Author**: Peremil
**Date**: Wed Jul 9 20:36:55 2025 +0200
**Message**: amll about page change
**Summary**: Modified `app/templates/about.html`.
**Detailed Description**: This commit makes a small textual adjustment to the about page content. While the specific change is minor, it demonstrates ongoing refinement of the user-facing content to improve clarity, accuracy, or presentation. These types of incremental content improvements help ensure the application provides clear and accurate information to users about its purpose and functionality.

## 3990a36a1ef4f1e9e0420d73c8958e392905a2ac
**Author**: Peremil
**Date**: Wed Jul 9 20:31:37 2025 +0200
**Message**: small change in about
**Summary**: Modified `app/templates/about.html`.
**Detailed Description**: Another minor content update to the about page, continuing the refinement of user-facing information. This type of iterative improvement shows attention to detail in ensuring the application presents clear and polished information to users about its features and purpose.

## 86af893f5e85a128b18173ef6f4f3973b0cf06a1
**Author**: Peremil
**Date**: Wed Jul 9 20:29:21 2025 +0200
**Message**: added about page
**Summary**: Modified `app/routes/main.py`, `app/templates/_navbar.html`, `app/templates/about.html`, and `app/templates/index.html`.
**Detailed Description**: This commit introduces a new about page to the application, providing users with information about the application's purpose, features, and functionality. The implementation includes creating the new about page template, adding the corresponding route in the main blueprint, and updating the navigation bar to include a link to the about page. This enhancement improves user experience by providing clear information about what the application does and how users can benefit from it. The about page likely explains the self-reflection and goal-tracking features, helping users understand the application's value proposition.

## c8a95c546cf1095ffb405fd7489dd7eff4ab6984
**Author**: Peremil
**Date**: Wed Jul 9 20:17:21 2025 +0200
**Message**: updated readme
**Summary**: Modified `README.md`.
**Detailed Description**: This commit updates the project's README file to improve documentation quality and project presentation. README updates typically include clearer setup instructions, updated feature descriptions, improved formatting, or corrections to outdated information. A well-maintained README is crucial for project understanding, onboarding new developers, and providing clear guidance for installation and usage. This update likely improves the overall documentation quality and makes the project more accessible to new contributors or users.

## 0c1da2cbec0d09569d6cabd15e515aa85107dccf
**Author**: Peremil
**Date**: Wed Jul 9 18:38:37 2025 +0200
**Message**: Implement interactive onboarding tour for new users
**Summary**: Added comprehensive onboarding tour system with `app/static/css/tour.css`, `app/static/js/tour/tour-controller.js`, template modifications, and supporting documentation.
**Detailed Description**: This commit introduces a sophisticated 3-phase cosmic-themed onboarding tour designed to welcome and guide new users through the application. The tour system includes a welcome modal, interactive first entry guidance, and progress discovery features. It uses localStorage for tour completion tracking and sessionStorage for cross-page state management, ensuring the tour only appears for new users with zero diary entries. The implementation includes responsive design with accessibility features, reduced motion support for users with accessibility needs, and a "Take Tour Again" option in the navigation bar. The tour celebrates completion with animations and provides a comprehensive introduction to diary writing, goal setting, and progress tracking. All 120 tests pass, confirming the tour doesn't interfere with existing functionality.

## 3d9bdefa5c71ddb2ad26395cd4453ff789e7dc86
**Author**: Peremil
**Date**: Wed Jul 9 18:08:26 2025 +0200
**Message**: Fix: Implement clickable behavior cards on progress page
**Summary**: Modified `app/routes/reader.py`, `app/static/css/progress.css`, `app/templates/diary.html`, and `app/templates/progress.html`.
**Detailed Description**: This commit enhances user interaction by making the "Opportunities for Growth" and "Positive Behaviors" cards clickable on the progress page. When clicked, these cards redirect users to the diary reader with appropriate rating filters (rating=-1 for behaviors to change, rating=1 for positive behaviors). The implementation adds onclick handlers and enhanced CSS hover effects to indicate the cards are interactive. The solution uses URL parameters rather than dedicated routes, providing a clean and efficient approach. Updated tooltips inform users about the clickable functionality, and all tests pass confirming the feature works correctly. This improvement makes it easier for users to quickly access specific types of diary entries from the progress dashboard.

## e29801f7bdb3c1aaee6863ab0ae6ef2181a6911e
**Author**: Peremil
**Date**: Wed Jul 9 17:59:21 2025 +0200
**Message**: Add clickable behavior categories feature
**Summary**: Modified `app/routes/reader.py`, `app/templates/diary.html`, `app/utils/search_helpers.py`, and added new documentation.
**Detailed Description**: This commit implements a new feature that allows users to click on behavior category links directly from the diary entry page. The implementation modifies the search helpers to accept an optional rating parameter for filtering diary entries by behavior type. New routes `/diary-entries/keep-doing` and `/diary-entries/change-this` provide behavior-specific filtering capabilities. The diary template is enhanced with clickable links under the behavior rating buttons, making it easy for users to quickly review all entries of a specific type. The existing search functionality is enhanced to support rating-based filtering via URL parameters, maintaining backward compatibility while adding new functionality. This feature improves user experience by providing quick access to categorized diary entries, supporting better self-reflection and progress tracking.

## 40e8c7fc2804bb2addc6b2b168fc58ec2743d69f
**Author**: Peremil
**Date**: Wed Jul 9 13:53:56 2025 +0200
**Message**: updated code style
**Summary**: Comprehensive code style refactoring across 42 files throughout the entire application including models, routes, templates, tests, and configuration.
**Detailed Description**: This commit represents a major code quality improvement initiative, applying consistent coding standards across the entire codebase. The refactoring touches every major component of the application including the Flask app initialization, configuration management, form definitions, database models, route handlers, utility functions, and the complete test suite. The changes include improved type hints, better variable naming, consistent formatting, enhanced docstrings, and adherence to Python best practices. A new `pyproject.toml` file is added to define project configuration and dependencies. This extensive refactoring significantly improves code maintainability, readability, and consistency, making the codebase more professional and easier to work with. The changes maintain all existing functionality while establishing a solid foundation for future development.

## 3112d1209619210be9d3a794b5307174b7460d62
**Author**: Peremil
**Date**: Wed Jul 9 13:03:06 2025 +0200
**Message**: refactored database
**Summary**: Modified database models and created a new migration `033faf89f4e5_rename_tables_to_snake_case_plural.py` along with updating related files.
**Detailed Description**: This commit implements a significant database schema refactoring by renaming all tables to follow snake_case plural naming conventions. The database tables are renamed from their previous format to `users`, `diary_entries`, `daily_stats`, and `goals`, providing better consistency with Python and Flask naming conventions. A comprehensive migration script handles the table renaming process, ensuring data integrity during the transition. The refactoring also includes updates to all model files to reflect the new table names and maintains all existing relationships and constraints. This change improves database schema consistency and follows industry best practices for naming conventions. The database backup created during this process ensures data safety during the migration.

## c32d84979a327507f08f417a457cc188db32edbf
**Author**: Peremil
**Date**: Wed Jul 9 11:00:35 2025 +0200
**Message**: added features to SPMP and updated the tab name
**Summary**: Modified `SPMP_250701.md` and `app/templates/base.html`.
**Detailed Description**: This commit updates the Software Project Management Plan (SPMP) documentation to reflect newly completed features and ongoing development progress. The SPMP is updated to track the current state of development milestones and feature implementation. Additionally, the browser tab title is updated in the base template to better reflect the application's current branding or functionality. These changes help maintain accurate project documentation and improve the user experience with a more descriptive browser tab title that helps users identify the application when multiple tabs are open.

## 8319e11123b9b2a3dff6e717a61bae57049e40cd
**Author**: Peremil
**Date**: Sun Jul 6 20:27:22 2025 +0200
**Message**: added profile link and greet message to navbar
**Summary**: Modified `app/__init__.py` and `app/templates/_navbar.html`.
**Detailed Description**: This commit adds a context processor in `app/__init__.py` to inject the `current_user` object into all templates. The `_navbar.html` template is updated to display a "Hello, [username]" message and a link to the user's profile in the navigation bar when a user is logged in.

## a510a2153f69fc738f783c0db43842a69fb0c328
**Author**: Peremil
**Date**: Sun Jul 6 20:19:56 2025 +0200
**Message**: minor front end updates
**Summary**: Modified `app/static/js/progress/charts.js`, `app/templates/diary.html`, `app/templates/goals.html`, and `app/templates/pdf/journey.html`.
**Detailed Description**: This commit contains minor front-end text and styling changes. It updates the label for "Failed" goals to "Not Completed" in the goal performance chart and on the goals page for better clarity. It also rephrases the rating buttons on the diary entry page to be more descriptive ("Keep Doing This" and "Change This").

## e6d967a62fbe83af0bf333ebf20423b273eb8cf6
**Author**: Peremil
**Date**: Sun Jul 6 20:03:10 2025 +0200
**Message**: redid the landing page
**Summary**: Modified `app/templates/base.html` and `app/templates/index.html`.
**Detailed Description**: This commit completely redesigns the application's landing page (`index.html`). It introduces a new layout with a fixed starry background, a gradient overlay, and a central content area. The new design features a prominent title, a subtitle, clear call-to-action buttons for registration/login or accessing the dashboard, and a section highlighting the core features with icons. It also adds a motivational quote. FontAwesome is also added to `base.html` to support the new icons.

## fc36fcc41062b1eb3861df263515943a6e305221
**Author**: Peremil
**Date**: Sun Jul 6 19:42:54 2025 +0200
**Message**: added the donate page
**Summary**: Added `app/templates/donate.html` and modified `app/routes/legal.py`, `app/static/css/custom_css.css`, `app/templates/_navbar.html`, and `tests/test_routes/test_progress.py`.
**Detailed Description**: This commit introduces a new "Donate" page. A new route `/donate` is added in `app/routes/legal.py` to render the `donate.html` template. The template includes a "Buy Me a Coffee" button and widget. The navigation bar is updated to include a link to the new page. Custom CSS is added for styling the donate card, and a new test is added to ensure the donate page loads correctly.

## f5af484a67144552f3a52a4ceea8827a6dfc6399
**Author**: Peremil
**Date**: Sun Jul 6 19:18:57 2025 +0200
**Message**: cleaned up my git tracking
**Summary**: Deleted numerous files from the root directory that were moved into the `app/` directory in a previous refactoring.
**Detailed Description**: This commit cleans up the project's root directory by deleting files that were made redundant by the recent refactoring which moved the core application into an `app` directory. This includes deleting old `routes`, `models`, `utils`, `static`, and `templates` directories and files from the root, resulting in a much cleaner and more organized project structure.

## 52ced21ed88c45fa0346448d5a81bebd38be298f
**Author**: Peremil
**Date**: Sun Jul 6 17:25:19 2025 +0200
**Message**: refactored the code
**Summary**: Modified the complete app structure, moving all files into a new `app/` directory.
**Detailed Description**: This commit refactors the entire application structure by moving all core files and directories into a new `app/` directory. This includes the `models`, `routes`, `static`, `templates`, and `utils` directories, as well as the main application files. The `run.py` file is now the main entry point for the application. This change improves the project's organization and modularity, making it easier to manage and scale in the future.

## 3fda552f0d6c164a09ca1051e4fb96b07552edef
**Author**: Peremil
**Date**: Sat Jul 5 19:58:36 2025 +0200
**Message**: urecommit
**Summary**: Modified `goal_stats.md`.
**Detailed Description**: This commit updates the `goal_stats.md` file to include considerations for data export. It outlines the need to include goal statistics in both JSON/CSV and PDF exports to ensure data portability for the user.

## f6d75e536a2f4808bd772d808c9627d16e247dfd
**Author**: Peremil
**Date**: Sat Jul 5 19:26:51 2025 +0200
**Message**: changed the layout of progress.html and grouped different categorys
**Summary**: Modified `templates/progress.html`.
**Detailed Description**: This commit reorganizes the `progress.html` template by grouping related statistics into different categories. The "Exploration Overview" and "Goals Overview" sections now have their own headers, and the "Goal Performance by Category" chart has been moved under the "Goals Overview" section. This improves the layout and readability of the progress page.

## 247181dc8ae53caa6ab3d49773bd8a5fb4c27f7d
**Author**: Peremil
**Date**: Sat Jul 5 19:19:39 2025 +0200
**Message**: added information about golas to the progress route. including completed, success rate and a stacked barplot for completed/failed goals
**Summary**: Modified `routes/progress.py`, `routes/goals.py`, `static/js/progress/charts.js`, `static/js/progress/main.js`, `templates/progress.html`, `tests/test_utils/test_goal_helpers.py`, and `utils/goal_helpers.py`.
**Detailed Description**: This commit adds goal-related statistics to the progress page. It introduces a new `get_goal_statistics` function in `utils/goal_helpers.py` to calculate the total number of completed goals, the success rate, and a breakdown of completed and failed goals by category. The `routes/progress.py` and `routes/goals.py` were updated to use this new function and pass the statistics to the `progress.html` template. The template was updated to display these new statistics in new cards and a stacked bar chart. The `static/js/progress/charts.js` and `static/js/progress/main.js` were updated to render the new chart. The tests in `tests/test_utils/test_goal_helpers.py` were also updated to reflect the changes in the `get_goal_statistics` function.

## 23432ecc1e29e67a51cf7f9cf74964211f137c5c
**Author**: Peremil
**Date**: Fri Jul 4 22:00:46 2025 +0200
**Message**: updated spmp with work
**Summary**: Modified `SPMP_250701.md`.
**Detailed Description**: This commit updates the project management plan to reflect the completion of the rate limiting implementation. It details that rate
limits have been applied to all sensitive blueprints and that a new test file has been added to verify the implementation.


## f6017858631ce36cfbc595a4882fd94d03f1dfcd
**Author**: Peremil
**Date**: Fri Jul 4 21:58:52 2025 +0200
**Message**: added rate limiting to all sensitive end points
**Summary**: Modified `routes/__init__.py and added tests/test_security.py`.
Detailed Description: This commit implements rate limiting across all sensitive endpoints of the application. It applies various rate limits to the auth,
diary, goals, user, progress, and reader blueprints. A new test file, tests/test_security.py, was added to ensure the rate limiting is working as expected.

## 02fcada72dd86cafc59bee7c46bc00d03f20ad96
**Author**: Peremil
**Date**: Fri Jul 4 09:03:06 2025 +0200
**Message**: recommit with deletions
**Summary**: Deleted several markdown files and `web_app.py`. Added a GitHub Actions workflow for security.
**Detailed Description**: This commit removes several outdated markdown files that were used for planning and suggestions. It also removes the old `web_app.py`
file, which has been replaced by the app factory pattern. A new GitHub Actions workflow, security.yml, has been added to automate dependency security audits.
The .gitignore file was also updated.


## 9bc0dead6b56884d6f13cb60340a27be6af73dee
**Author**: Peremil
**Date**: Fri Jul 4 08:46:45 2025 +0200
**Message**: added a changelog files with description of my commits
**Summary**: Added `changelog.md`.
**Detailed Description**: This commit adds the `changelog.md` file to the project. The file is pre-populated with a detailed history of all previous commits, their
descriptions, and summaries.


## ca8a2c20cbd1f136ab2c24e9cf71370fff112234
**Author:** Peremil
**Date:** Thu Jul 3 21:25:16 2025 +0200
**Message:** added tests for the forms
**Summary:** Added 65 lines to `tests/test_forms/test_forms.py`.
**Detailed Description:** This commit introduces a new test file `tests/test_forms/test_forms.py` which contains comprehensive unit tests for all the application's forms. These tests validate the correct behavior of `LoginForm`, `RegisterForm`, `DiaryEntryForm`, `GoalForm`, `GoalProgressForm`, and `DeleteAccountForm` under both valid and invalid input conditions.

## 5ff6933214c096176e968299d1cb95ab8ac88465
**Author:** Peremil
**Date:** Wed Jul 2 00:54:25 2025 +0200
**Message:** added tests for diary entries
**Summary:** Modified `forms.py`, `routes/diary.py`, and `tests/test_routes/test_diary.py`. Overall, 7 insertions and 8 deletions.
**Detailed Description:** This commit refines the diary entry form validation. A custom `validate_rating` method was added to `DiaryEntryForm` in `forms.py` to ensure the rating is strictly -1 or 1. Consequently, the manual rating assignment in `routes/diary.py` was removed, allowing the form to handle the rating directly. The corresponding test in `tests/test_routes/test_diary.py` was updated to assert the presence of a danger alert message for invalid ratings and to expect a direct 400 response instead of a redirect.

## bd70bf0af1afcb7b3a44a9228690661940df86ab
**Author:** Peremil
**Date:** Wed Jul 2 00:43:41 2025 +0200
**Message:** cleaned up the mds
**Summary:** Modified `GEMINI.md`, `SPMP_250701.md`, `forms.py`, `routes/diary.py`, and `tests/test_routes/test_diary.py`. Overall, 490 insertions and 79 deletions.
**Detailed Description:** This commit primarily focuses on refining project documentation and introducing comprehensive testing for diary entries. The `GEMINI.md` file has been significantly expanded and restructured to provide a more detailed overview of the project's technology stack, structure, and features. A new `SPMP_250701.md` file was created to centralize the development roadmap, security hardening, and code quality plans, which were previously less detailed or scattered. Additionally, extensive unit and integration tests for diary entry functionality were added in `tests/test_routes/test_diary.py`, covering various scenarios including valid/invalid inputs and streak calculations. A minor adjustment was made to `forms.py` regarding the `DiaryEntryForm`'s rating validation, and some debugging print statements were added to `routes/diary.py`.

## 64d3360794813d6991c02a23967087520a70efb9
**Author:** Peremil
**Date:** Tue Jul 1 23:57:27 2025 +0200
**Message:** added deletion logic and tests
**Summary:** Modified multiple files including `250629_suggestions.md`, `GEMINI.md`, `forms.py`, `migrations/env.py`, `migrations/versions/1a2b3c4d5e6f_create_initial_tables.py`, `migrations/versions/8d44538eef95_baseline.py`, `routes/user.py`, `templates/delete_account_confirm.html`, `templates/delete_account_placeholder.html`, `templates/settings.html`, `tests/test_migrations.py`, and `tests/test_routes/test_user.py`. Overall, 352 insertions and 143 deletions.
**Detailed Description:** This commit introduces significant changes related to user account deletion and database migrations. A `DeleteAccountForm` was added to `forms.py` to handle password confirmation for deletion. The `routes/user.py` now includes the full logic for account deletion, which cascades to remove all associated `DailyStats`, `Goal`, and `DiaryEntry` records before deleting the user. A new `delete_account_confirm.html` template was created for the confirmation page, replacing a placeholder. The `migrations/env.py` was updated to a more modern Alembic configuration, and a new initial migration script (`1a2b3c4d5e6f_create_initial_tables.py`) was added, replacing the previous baseline. Comprehensive tests for account deletion and database migrations were added in `tests/test_routes/test_user.py` and `tests/test_migrations.py` respectively. Documentation in `250629_suggestions.md` and `GEMINI.md` was updated to reflect these changes, particularly regarding GDPR compliance and the completion of certain roadmap items.

## 418d766f480d003834517c788527b1583fb1379f
**Author:** Peremil
**Date:** Mon Jun 30 23:47:39 2025 +0200
**Message:** fixed some deprecated warnings
**Summary:** Modified `models/goal.py`, `routes/auth.py`, and `routes/diary.py`. Overall, 4 insertions and 4 deletions.
**Detailed Description:** This commit addresses deprecated warnings and updates datetime handling for better consistency. In `models/goal.py`, the `created_at` timestamp for goals was updated to use timezone-aware UTC datetimes (`datetime.now(timezone.utc)`) instead of naive UTC datetimes (`datetime.utcnow`), which is a more robust approach for handling timestamps. Additionally, in `routes/auth.py` and `routes/diary.py`, the method for fetching user objects by ID was updated from the older `User.query.get()` to the SQLAlchemy 2.0 recommended `db.session.get()`, aligning with modern SQLAlchemy practices and resolving potential deprecation warnings.

## 4efa6c914e4a5f9054794768842572302ab416f1
**Author:** Peremil
**Date:** Mon Jun 30 23:41:27 2025 +0200
**Message:** finished the refactoring of the main app struture
**Summary:** Modified multiple files including `250629_suggestions.md`, `GEMINI.md`, `README.md`, `app.py`, `routes/__init__.py`, `routes/main.py`, `static/js/{ => goals}/goals.js`, `static/js/{ => legal}/cookie_consent.js`, `templates/base.html`, `templates/errors/404.html`, `templates/goals.html`, `tests/README.md`, `tests/conftest.py`, and `tests/test_basic.py`. Overall, 150 insertions and 14 deletions.
**Detailed Description:** This commit completes the refactoring of the main application structure. The primary change is the renaming of `web_app.py` to `app.py` and its transformation into a pure app factory, which now handles the initialization of Flask extensions like `Flask-Migrate`, `CSRFProtect`, and `Flask-Limiter`. The main route (`/`) and error handlers (`403`, `404`, `500`) were moved from `app.py` to a new `routes/main.py` blueprint, which is registered in `routes/__init__.py`. JavaScript files in `static/js` were reorganized into feature-based subdirectories (`static/js/goals/goals.js` and `static/js/legal/cookie_consent.js`). The `base.html` template was updated to load the `cookie_consent.js` globally. Various references to `web_app.py` were updated to `app.py` across `README.md`, `GEMINI.md`, and test files (`tests/README.md`, `tests/conftest.py`, `tests/test_basic.py`). The `250629_suggestions.md` was also updated to reflect the completion of these refactoring tasks and to introduce new suggestions for further improvements.

## 68f6e4a30bb64bc3394aec37edcbcccbe7c43126
**Author:** Peremil
**Date:** Mon Jun 30 16:02:20 2025 +0200
**Message:** added terms of service, privacy policy and user page.
**Summary:** Modified multiple files including `gdpr.md`, `routes/__init__.py`, `routes/legal.py`, `routes/user.py`, `static/js/cookie_consent.js`, `templates/_navbar.html`, `templates/base.html`, `templates/delete_account_placeholder.html`, `templates/privacy.html`, `templates/settings.html`, and `templates/terms.html`. Overall, 314 insertions and 1 deletion.
**Detailed Description:** This commit introduces a suite of new features focused on user profile management, legal compliance, and data privacy. A new `user` blueprint (`routes/user.py`) was added to handle user profiles, data export (JSON/CSV), and a placeholder for account deletion. Dedicated `legal` routes (`routes/legal.py`) were created for Privacy Policy (`privacy.html`) and Terms of Service (`terms.html`) pages. A cookie consent banner (`static/js/cookie_consent.js`) was implemented to address GDPR requirements, and its loading was integrated into `base.html`. The navigation bar (`_navbar.html`) was updated to include a link to the new user profile page. A `gdpr.md` document was added to outline the plan for these compliance features. The `delete_account_placeholder.html` was created as a temporary page for the account deletion feature.

## a5903788179fa3e1960589dbb3cd6dec3f56abfe
**Author:** Peremil
**Date:** Mon Jun 30 15:25:06 2025 +0200
**Message:** added security.yml and updated security audits workflow
**Summary:** Modified `README.md` and `requirements.txt`. Overall, 28 insertions.
**Detailed Description:** This commit integrates dependency security auditing into the project. The `README.md` was updated to include a new section detailing how to run `safety` and `pip-audit` locally to check for known vulnerabilities in Python dependencies. The `requirements.txt` file was updated to include `pip-audit` as a dependency. This change also implies an update to the GitHub Actions workflow (though `security.yml` is not directly shown in this diff, the commit message indicates its addition) to automate these security checks on pushes and pull requests, enhancing the project's security posture.

## 042145b9632988089d3c1e3d8015fbfaed9cf434
**Author:** Peremil
**Date:** Sun Jun 29 22:32:24 2025 +0200
**Message:** added csrf tokens and furhter testing
**Summary:** Modified multiple files including `models/user.py`, `requirements.txt`, `routes/__init__.py`, `routes/auth.py`, `static/js/goals.js`, `static/js/progress/export.js`, `templates/base.html`, `templates/goals.html`, `tests/README.md`, `tests/conftest.py`, `tests/test_basic.py`, `tests/test_csrf.py`, `tests/test_models/test_user.py`, `tests/test_routes/test_auth.py`, `tests/test_utils/test_goal_helpers.py`, and `web_app.py`. Overall, 556 insertions and 167 deletions.
**Detailed Description:** This commit significantly enhances the application's security by implementing CSRF (Cross-Site Request Forgery) protection and expands the test suite. CSRF tokens are now generated and included in `templates/base.html` via a meta tag, and are used in JavaScript-driven POST requests (e.g., in `static/js/goals.js` and `static/js/progress/export.js`) and form submissions (`templates/goals.html`). The `User` model in `models/user.py` was updated to include password hashing and verification methods, moving away from direct password storage. `Flask-Limiter` was integrated into `web_app.py` (now `app.py`) and applied to login and registration routes in `routes/__init__.py` to prevent brute-force attacks. The `requirements.txt` was updated to include new dependencies for these features. Extensive new tests were added, including `tests/test_csrf.py` to verify CSRF token presence, and updates to `tests/test_basic.py`, `tests/test_models/test_user.py`, `tests/test_routes/test_auth.py`, and `tests/test_utils/test_goal_helpers.py` to cover the new authentication logic, form submissions, and general application behavior with CSRF enabled. The `conftest.py` was also updated to include a helper function for extracting CSRF tokens in tests.

## 69e210e2cd697fe177541d567ccc56edaa474ddd
**Author:** Peremil
**Date:** Sun Jun 29 21:25:38 2025 +0200
**Message:** added test framework
**Summary:** Modified multiple files including `pytest.ini`, `requirements.txt`, `routes/progress.py`, `tests/README.md`, `tests/__init__.py`, `tests/conftest.py`, `tests/test_basic.py`, `tests/test_models/__init__.py`, `tests/test_models/test_user.py`, `tests/test_routes/__init__.py`, `tests/test_routes/test_auth.py`, `tests/test_utils/__init__.py`, and `tests/test_utils/test_goal_helpers.py`. Overall, 561 insertions and 3 deletions.
**Detailed Description:** This commit introduces a comprehensive testing framework to the project using `pytest`. A `pytest.ini` file was added to configure the test runner, defining test paths, file patterns, and markers. New directories and `__init__.py` files were created under `tests/` for organizing tests by category (models, routes, utils). A `conftest.py` file was added to define shared fixtures for tests, such as `app`, `client`, and sample data (`sample_user`, `sample_diary_entry`, `sample_goal`, `sample_daily_stats`). Initial basic tests were added in `tests/test_basic.py`, `tests/test_models/test_user.py`, `tests/test_routes/test_auth.py`, and `tests/test_utils/test_goal_helpers.py` to cover core functionalities. The `requirements.txt` was updated to include `pytest` and its related plugins (`coverage`, `pytest-flask`, `pytest-mock`). A `tests/README.md` was also added to provide documentation on how to run and structure tests. A minor adjustment was made to the word cloud weight calculation in `routes/progress.py`.

## 417cf110a7aef8351f1a81a92176b899e7b24a92
**Author:** Peremil
**Date:** Sun Jun 29 11:00:23 2025 +0200
**Message:** updated requirements.txt
**Summary:** Modified `requirements.txt`. Overall, 6 insertions and 1 deletion.
**Detailed Description:** This commit updates the `requirements.txt` file, primarily to include new dependencies necessary for the recently integrated testing framework and Flask-Migrate. Specifically, `alembic`, `dnspython`, `Flask-Migrate`, `idna`, and `Mako` were added. The `email_validator` package was also updated to `email-validator`.

## b0259bbc12fa88abece0aa19ffafd44b90836856
**Author:** Peremil
**Date:** Sun Jun 29 10:58:14 2025 +0200
**Message:** completed implementing flask_migrate
**Summary:** Modified multiple files including `migrations/README`, `migrations/alembic.ini`, `migrations/env.py`, `migrations/script.py.mako`, `migrations/versions/8d44538eef95_baseline.py`, and `web_app.py`. Overall, 217 insertions and 4 deletions.
**Detailed Description:** This commit completes the integration of Flask-Migrate for database schema management. New files were added to the `migrations/` directory, including `README`, `alembic.ini` (Alembic configuration), `env.py` (Alembic environment script), `script.py.mako` (migration script template), and an initial baseline migration script `8d44538eef95_baseline.py`. The `web_app.py` file was updated to initialize `Flask-Migrate` with the Flask application and SQLAlchemy database. This change also removes the `db.create_all()` call from `web_app.py` as database creation and updates will now be handled by migrations. The `requirements.txt` was updated in the previous commit to include `Flask-Migrate` and its dependencies.

## 15217beb47112708c94cb21d2b35b21aac0bad7b
**Author:** Peremil
**Date:** Sun Jun 29 10:10:13 2025 +0200
**Message:** added and removed some documents for future refrence
**Summary:** Modified `250629_suggestions.md` and `GEMINI.md`. Overall, 182 insertions and 218 deletions.
**Detailed Description:** This commit primarily involves a significant restructuring and update of the project's documentation. The `250629_suggestions.md` file, which contained development suggestions, was removed. Concurrently, the `GEMINI.md` file, serving as the project overview for the AI assistant, underwent a major overhaul. It was expanded to include more detailed information about the technology stack, project structure (including specific files and their roles), and key features with their implementation details. This update aims to provide a more comprehensive and precise reference for future AI interactions, ensuring clarity on the application's components and functionalities.

## 54de5fd050fcb4e58121e3f801e95e834264713a
**Author:** Peremil
**Date:** Sun Jun 29 09:38:13 2025 +0200
**Message:** added sessions timer and logging
**Summary:** Modified `config.py`, `routes/auth.py`, and `web_app.py`. Overall, 60 insertions and 8 deletions.
**Detailed Description:** This commit introduces session management with a timeout and enhances logging for authentication events. In `config.py`, `PERMANENT_SESSION_LIFETIME` was set to 24 hours, and `SESSION_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY`, and `SESSION_COOKIE_SAMESITE` were configured for improved security. The `web_app.py` file now includes a `before_request` middleware that validates and renews user sessions, clearing them if they have expired. It also sets `g.user` for template context. Logging was integrated into `web_app.py` for application startup and internal server errors. In `routes/auth.py`, logging was added for successful logins, failed login attempts (due to no user or incorrect password), and registration attempts with existing emails. The logout function was also updated to log the user out explicitly.

## a7b8b3ebfd27b1b4c05fd34bfaf0e446e41f6075
**Author:** Peremil
**Date:** Sat Jun 28 23:43:12 2025 +0200
**Message:** changed the wordcloud display to normalize the words
**Summary:** Modified `routes/progress.py` and `static/js/progress/main.js`. Overall, 38 insertions and 7 deletions.
**Detailed Description:** This commit refines the word cloud generation and display on the progress page. In `routes/progress.py`, the normalization logic for word weights was adjusted to scale from 70 to 150, providing a wider range for word sizes in the word cloud. The stop words list was also updated to include a more comprehensive set of common English words. In `static/js/progress/main.js`, the `weightFactor` function for `wordcloud2.js` was updated with a new scaling logic (minSize 14, maxSize 48) to better utilize the normalized weights from the backend, resulting in a more visually appealing word cloud. The `shrinkToFit` option was also added to the word cloud configuration to improve rendering.

## 4b3a8d4c7ecd7c810c7ced79824a2c0496c06967
**Author:** Peremil
**Date:** Sat Jun 28 23:21:26 2025 +0200
**Message:** fixed flash messages
**Summary:** Modified `routes/diary.py`, `routes/goals.py`, and `templates/base.html`. Overall, 172 insertions and 22 deletions.
**Detailed Description:** This commit focuses on improving the handling and display of flash messages across the application, particularly for form submissions and goal management. In `templates/base.html`, a new block was added to display flashed messages using Bootstrap alerts, ensuring they are consistently styled and dismissible. In `routes/diary.py`, the diary entry form submission now returns a 400 status code along with the form and errors when validation fails, providing better feedback to the user. Similarly, in `routes/goals.py`, the goal creation and update routes were refactored to render the `goals.html` template with appropriate status codes (400 for validation errors, 500 for server errors, 404 for not found) and flash messages when form validation fails or an error occurs. This change also ensures that the `GoalProgressForm` is passed to the template. The success messages for completing or failing goals were also simplified.

## 2f2a562aa3bde5823a1ef1ebd697335fd0d93395
**Author:** Peremil
**Date:** Sat Jun 28 22:15:56 2025 +0200
**Message:** added custom error 404 403 and 500 pages
**Summary:** Modified `templates/errors/403.html`, `templates/errors/404.html`, `templates/errors/500.html`, and `web_app.py`. Overall, 48 insertions.
**Detailed Description:** This commit introduces custom error pages for 403 (Forbidden), 404 (Not Found), and 500 (Internal Server Error) HTTP status codes. New HTML templates (`403.html`, `404.html`, `500.html`) were added to the `templates/errors/` directory, providing a more user-friendly and themed experience for these common errors. Corresponding error handlers were registered in `web_app.py` using `@app.errorhandler` decorators, ensuring that these custom pages are rendered when the respective errors occur.

## 85b28d245098a0860314297da45b3c3343c95655
**Author:** Peremil
**Date:** Sat Jun 28 18:28:58 2025 +0200
**Message:** fixed the goals page aswell
**Summary:** Modified `routes/goals.py` and `templates/goals.html`. Overall, 84 insertions and 52 deletions.
**Detailed Description:** This commit significantly refactors the goals page to integrate Flask-WTF forms for goal creation and progress updates, enhancing validation and user feedback. In `routes/goals.py`, the `create_new_goal` and `update_goal` functions now utilize `GoalForm` and `GoalProgressForm` respectively, handling form validation and displaying errors directly on the `goals.html` page with appropriate HTTP status codes (400 for validation errors, 500 for server errors). The `mark_goal_complete` and `mark_goal_failed` functions were also updated to re-render the `goals.html` page upon completion or failure, providing immediate visual feedback and updated goal statistics, along with relevant status codes (200 for success, 404 for not found, 500 for errors). In `templates/goals.html`, the goal creation form was updated to use Flask-WTF rendering, including CSRF protection and dynamic display of validation errors for each field.

## 9d68695eeb11c2513825c82a275876010097874e
**Author:** Peremil
**Date:** Sat Jun 28 16:34:49 2025 +0200
**Message:** style: ensure character counter text is pure white
**Summary:** Modified `templates/diary.html`. Overall, 5 insertions and 2 deletions.
**Detailed Description:** This commit makes a minor styling adjustment to the diary entry page. The character counter text in `templates/diary.html` has been updated to display in pure white (`#FFFFFF`) instead of the default muted color. Additionally, the JavaScript for the character counter was improved to set the initial character count when the page loads, ensuring accuracy from the start.

## 48a1e1f09ecf0c5733c8da336d62b929eba4bbc1
**Author:** Peremil
**Date:** Sat Jun 28 16:30:35 2025 +0200
**Message:** fix: enforce character limit on diary textarea
**Summary:** Modified `templates/diary.html`. Overall, 23 insertions and 3 deletions.
**Detailed Description:** This commit enforces a character limit of 2000 on the diary entry textarea and provides real-time visual feedback to the user. In `templates/diary.html`, the `maxlength` attribute was added to the diary content textarea. A character counter was implemented below the textarea, which dynamically updates as the user types. If the entered text exceeds 2000 characters, the counter text turns red, and the rating submission buttons are disabled, preventing the submission of entries that are too long.

## 154988123e1d6844f53be67a8c08a79ef9909d3e
**Author:** Peremil
**Date:** Sat Jun 28 16:23:12 2025 +0200
**Message:** fix: resolve diary form submission and validation issues
**Summary:** Modified `routes/diary.py` and `templates/diary.html`. Overall, 32 insertions and 53 deletions.
**Detailed Description:** This commit addresses issues with diary form submission and validation. In `routes/diary.py`, the logic for processing diary entries was refactored to ensure that the rating is correctly captured before form validation. The streak calculation and `DailyStats` update logic were streamlined for clarity and efficiency. Error handling was improved to display all validation errors from the form. In `templates/diary.html`, the rating buttons were changed from direct submit buttons to regular buttons with `data-rating` attributes. JavaScript now handles setting the selected rating to a hidden input field and submitting the form, providing more control over the submission process and allowing for better integration with Flask-WTF validation. The character counter and `maxlength` attribute were also added to the diary content textarea.

## 4c8c9f231db4fd8923810c0a41d919602b80796f
**Author:** Peremil
**Date:** Sat Jun 28 16:18:51 2025 +0200
**Message:** feat: integrate Flask-WTF for diary entries
**Summary:** Modified `routes/diary.py` and `templates/diary.html`. Overall, 36 insertions and 16 deletions.
**Detailed Description:** This commit integrates Flask-WTF for handling diary entry forms, improving validation and security. In `routes/diary.py`, the route now initializes and uses `DiaryEntryForm` to process submissions, leveraging `form.validate_on_submit()` for server-side validation. Flash messages are used to display validation errors to the user. The `templates/diary.html` was updated to render the form fields using Flask-WTF's Jinja2 helpers, including `form.hidden_tag()` for CSRF protection and displaying specific error messages for content and rating fields. This change streamlines form handling and enhances the user experience by providing immediate feedback on invalid inputs.

## 7696eaeef55720807b831b990bc4d955c3e40d96
**Author:** Peremil
**Date:** Sat Jun 28 13:03:32 2025 +0200
**Message:** added form validation with flask-wtf and error handling.
**Summary:** Modified `REFACTORING_PLAN.md`, `forms.py`, `requirements.txt`, `routes/auth.py`, `templates/login.html`, `templates/register.html`, and `validation_security_implementation.md`. Overall, 609 insertions and 54 deletions.
**Detailed Description:** This commit introduces robust form validation and error handling using Flask-WTF. A new `forms.py` file was created to define `LoginForm`, `RegisterForm`, `DiaryEntryForm`, `GoalForm`, and `GoalProgressForm` classes, incorporating validators for data presence, email format, length, password matching, and custom password strength (mixed case, minimum length). The `requirements.txt` was updated to include `Flask-WTF` and `email-validator`. The authentication routes (`routes/auth.py`) were refactored to use these new form classes, replacing manual form handling with `form.validate_on_submit()` and displaying validation errors as flash messages. The `templates/login.html` and `templates/register.html` were updated to render these Flask-WTF forms, including CSRF tokens and displaying validation feedback. Additionally, a `REFACTORING_PLAN.md` and `validation_security_implementation.md` were added to document the strategy for these and future improvements, outlining steps for security, session management, and logging.

## b8e9e5441184677548fd504992e3293f1fe804ee
**Author:** Peremil
**Date:** Fri Jun 27 20:44:27 2025 +0200
**Message:** fixed the export with the new wordcloud
**Summary:** Modified multiple files including `routes/progress.py`, `static/js/progress/export.js`, `static/js/progress/main.js`, `templates/pdf/journey.html`, `templates/progress.html`, and `utils/pdf_generator.py`. Overall, 156 insertions and 12 deletions.
**Detailed Description:** This commit enables the inclusion of the dynamically generated word cloud in the PDF export of the user's journey. On the frontend, `static/js/progress/export.js` was updated with a `waitForWordcloud` function to ensure the word cloud canvas is fully rendered before capturing its image data. This captured image is then sent via a POST request to the backend. On the backend, `routes/progress.py` now receives this word cloud image data. The `utils/pdf_generator.py` was modified to accept and process this image, embedding it into the `templates/pdf/journey.html` for PDF generation. A hidden canvas element was added to `templates/progress.html` to facilitate the image capture. Debugging logs were also added to `static/js/progress/main.js` to monitor the word cloud loading process, and a fallback CDN was introduced for `wordcloud2.js`.

## 608f1cfc0bf79fcb10e1bce550597f5f6f089494
**Author:** Peremil
**Date:** Fri Jun 27 19:57:20 2025 +0200
**Message:** added wordcloud
**Summary:** Modified `routes/progress.py`, `static/js/progress/main.js`, and `templates/progress.html`. Overall, 107 insertions and 2 deletions.
**Detailed Description:** This commit introduces a dynamic word cloud feature to the progress dashboard. In `routes/progress.py`, logic was added to extract and count words from diary entries, filter out stop words, and prepare the data for the word cloud. The word cloud is only generated if there are at least 10 diary entries. In `templates/progress.html`, a new section was added to display the word cloud, with a placeholder message and progress bar if the entry count is insufficient. The `static/js/progress/main.js` was updated to dynamically load the `wordcloud2.js` library and render the word cloud using the processed data, including interactive features like clicking on words to search for them in the diary reader. The word cloud is styled to match the sci-fi theme.

## e92e4cd8a40956cb2af51714ce59fd9782fd8859
**Author:** Peremil
**Date:** Fri Jun 27 19:08:11 2025 +0200
**Message:** minor ui tweaks with collapsable cards
**Summary:** Modified multiple files including `GEMINI.md`, `flask_style_guide.md`, `static/js/goals.js`, `static/js/progress/entries.js`, `templates/diary.html`, and `templates/goals.html`. Overall, 845 insertions and 62 deletions.
**Detailed Description:** This commit introduces minor UI tweaks, primarily focusing on making sections collapsible and improving the display of historical data. A new `flask_style_guide.md` was added, outlining coding standards for Python, HTML, CSS, and JavaScript, including naming conventions and project structure. The `GEMINI.md` file was significantly expanded to provide a more comprehensive overview of the project, detailing the technology stack, project structure, and key features with their implementation. In `templates/goals.html`, a "Show more/less" button was added to the "Recent Goals" section, allowing users to toggle the visibility of older goals. This functionality is supported by new JavaScript in `static/js/goals.js` and `static/js/progress/entries.js` (which now includes a `toggleExtraGoals` function). A minor styling adjustment was made in `templates/diary.html` to ensure the date text is pure white.

## 35a396eb3da29a655a94210ec01f1498d06e75d2
**Author:** Peremil
**Date:** Fri Jun 27 17:05:15 2025 +0200
**Message:** added minimizing top 3 days and clicking on chart points.
**Summary:** Modified `static/js/progress/charts.js`, `static/js/progress/entries.js`, and `templates/progress.html`. Overall, 76 insertions and 42 deletions.
**Detailed Description:** This commit enhances the progress dashboard by adding interactivity to the charts and improving the display of top days. In `static/js/progress/charts.js`, a new `onClick` event handler was added to the points chart, allowing users to click on a data point to navigate to the diary reader page for that specific date. In `templates/progress.html`, the "Top Days" section was updated to initially show only the first three entries for each day, with a "Show more/less" button to toggle the visibility of additional entries. This functionality is supported by a new `toggleExtraEntries` JavaScript function added to `static/js/progress/entries.js`, which dynamically hides or shows entries and updates the button text.

## 1039d8070b48c11da6af9ce3158da55c29758ca9
**Author:** Peremil
**Date:** Fri Jun 27 13:23:26 2025 +0200
**Message:** fixed the card sizes on the search results
**Summary:** Modified `templates/read_diary.html`. Overall, 37 insertions and 9 deletions.
**Detailed Description:** This commit refines the styling and layout of search results on the diary reader page. In `templates/read_diary.html`, the CSS for `.search-result-card` was adjusted to reduce padding and margin, making the cards more compact. New flexbox properties were added to `.search-result-card` and `.search-result-main` to ensure proper alignment and spacing of elements within the search results. The date and snippet elements were given specific styles to control their appearance and overflow behavior, ensuring that long snippets are truncated with ellipses. The "Read Full Day" button was also repositioned for better visual integration.

## 16e81bf07a205883deec8101abc5f24009db29bf
**Author:** Peremil
**Date:** Fri Jun 27 13:19:54 2025 +0200
**Message:** styled the serach results
**Summary:** Modified `templates/read_diary.html`. Overall, 23 insertions and 1 deletion.
**Detailed Description:** This commit focuses on styling the search results section within the `templates/read_diary.html` file. New CSS rules were added for `.search-result-card`, `.search-result-date`, and `.search-result-btn` to give search results a distinct card-like appearance with appropriate padding, margins, and box shadows. The date display within each search result now includes a calendar icon and is styled for better readability. A "Read Full Day" button was added to each search result, allowing users to directly navigate to the full diary entry for that specific date.

## 659665be6691f0a2721a082ac51779489ad32d33
**Author:** Peremil
**Date:** Fri Jun 27 13:15:29 2025 +0200
**Message:** stylised diary page
**Summary:** Modified `templates/read_diary.html` and `users.db`. Overall, 123 insertions and 76 deletions.
**Detailed Description:** This commit introduces a significant visual overhaul to the diary reading page (`templates/read_diary.html`), aligning its design with the sci-fi theme of the application. New CSS styles were added directly within the template to create a `diary-search-card` for the search form, `diary-day-title` for the date display, and `diary-entry-content` for individual diary entries, all featuring dark backgrounds, subtle gradients, rounded borders, and shadows. Navigation buttons were also styled to match. The `users.db` file was also touched, likely due to a local database operation during development, but no functional changes are implied.

## fbb6b3377c22d7c75a977454d156ed3e86e297fb
**Author:** Peremil
**Date:** Fri Jun 27 09:39:42 2025 +0200
**Message:** added the goals page
**Summary:** Modified multiple files including `models/__init__.py`, `models/goal.py`, `routes/__init__.py`, `routes/goals.py`, `routes/progress.py`, `static/css/goals.css`, `static/css/progress.css`, `static/js/goals.js`, `templates/_navbar.html`, `templates/base.html`, `templates/goals.html`, `templates/progress.html`, and `utils/goal_helpers.py`. Overall, 1080 insertions and 3 deletions.
**Detailed Description:** This commit introduces the complete goal setting and tracking functionality to the application. A new `Goal` model was added in `models/goal.py` to store goal details. The `routes/goals.py` blueprint was created to handle all goal-related routes, including creating, viewing, updating, and deleting goals. Helper functions for goal management were added to `utils/goal_helpers.py`. Frontend components were introduced with `templates/goals.html` for the goals page, `static/css/goals.css` for styling, and `static/js/goals.js` for client-side interactivity. The navigation bar (`templates/_navbar.html`) was updated to include a link to the new goals page. Minor adjustments were also made to `routes/progress.py` and `templates/progress.html` to integrate goal-related data into the progress dashboard.

## 5290d52706e0194a7ce30c5da45d7ef7cfacfc1a
**Author:** Peremil
**Date:** Thu Jun 26 21:13:17 2025 +0200
**Message:** refactored progress.html
**Summary:** Modified `static/css/progress.css`, `static/js/progress/entry-toggles.js`, and `templates/progress.html`. Overall, 509 insertions and 548 deletions.
**Detailed Description:** This commit refactors the frontend of the progress dashboard by extracting extensive inline CSS into a dedicated `static/css/progress.css` file. This new CSS file introduces a sci-fi theme with styles for various components like data cards, diary entry cards, and chart overlays, including animations and responsive design. Additionally, a new JavaScript file, `static/js/progress/entry-toggles.js`, was created to handle the interactive expansion and collapse of diary entries displayed on the dashboard. The `templates/progress.html` was updated to import these new external files, improving code organization and maintainability.

## 2b6edf41cd43a3f6f70d90a07f29eef86a749764
**Author:** Peremil
**Date:** Thu Jun 26 21:03:56 2025 +0200
**Message:** redid the progress html front end
**Summary:** Modified `static/js/progress/charts.js` and `templates/progress.html`. Overall, 673 insertions and 60 deletions.
**Detailed Description:** This commit significantly overhauls the frontend of the progress dashboard. It introduces a new sci-fi themed design for various components, including data cards, entry cards, and chart overlays, with animations and responsive adjustments. The inline CSS for these elements was extracted into a separate `progress.css` file for better organization. The Chart.js configuration for the weekday chart was updated to include more styling for axes, grids, and ticks, and to visually dim the chart when insufficient data is available. The `templates/progress.html` file was updated to reflect these new styles and to include a new `entry-toggles.js` script for managing the display of diary entries.

## 3cb673584c5a5a02df76dfee8c8473e81989cc23
**Author:** Peremil
**Date:** Thu Jun 26 20:25:18 2025 +0200
**Message:** changed the readme
**Summary:** Modified `README.md`. Overall, 1 insertion and 1 deletion.
**Detailed Description:** This commit makes a minor update to the `README.md` file. The placeholder text "[your donation link]" in the "Supporting This Project" section was replaced with "[Coming soon]", indicating that donation options are not yet available.

## 22f7f645e64007d665a8501901782e44d1770428
**Author:** Peremil
**Date:** Thu Jun 26 20:23:47 2025 +0200
**Message:** redid the diary.html and added backend logic to recent posts
**Summary:** Modified `routes/diary.py`, `templates/diary.html`, and `utils/progress_helpers.py`. Overall, 156 insertions and 12 deletions.
**Detailed Description:** This commit overhauls the diary entry page (`templates/diary.html`) with a new sci-fi themed design, including a prominent header, a styled textarea for entries, and visually distinct buttons for rating. It also introduces a "Recent Reflections" section to display the user's latest diary entries. On the backend, `routes/diary.py` was updated to fetch these recent entries, leveraging a new `get_recent_entries` helper function added to `utils/progress_helpers.py`. This helper function retrieves a specified number of the most recent diary entries for a given user, enhancing the user's ability to review their past reflections directly on the diary page.

## 24f9aab37fd0972a9313a44556736550e7e46334
**Author:** Peremil
**Date:** Thu Jun 26 17:04:07 2025 +0200
**Message:** refactored my html!
**Summary:** Modified multiple files including `templates/_navbar.html`, `templates/base.html`, `templates/diary.html`, `templates/index.html`, `templates/login.html`, `templates/progress.html`, `templates/read_diary.html`, and `templates/register.html`. Overall, 97 insertions and 242 deletions.
**Detailed Description:** This commit introduces a significant refactoring of the HTML structure across the application by implementing a base template (`base.html`) and a separate navigation bar partial (`_navbar.html`). All individual HTML pages (`diary.html`, `index.html`, `login.html`, `progress.html`, `read_diary.html`, `register.html`) were updated to extend `base.html` and include `_navbar.html`, eliminating redundant HTML, Bootstrap imports, and navigation code. This change centralizes common elements, improves maintainability, and ensures a consistent look and feel across the application. The navigation bar logic was also updated to dynamically display links based on user authentication status and the current page.

## 932d20d8a68416e1f7d475f2aa523bb08abcf5ef
**Author:** Peremil
**Date:** Thu Jun 26 16:41:21 2025 +0200
**Message:** redid index.html
**Summary:** Modified `static/css/custom_css.css` and `templates/index.html`. Overall, 51 insertions and 16 deletions.
**Detailed Description:** This commit reworks the `index.html` landing page to improve its visual appeal and structure. The main hero section was redesigned with a new layout and text, replacing the previous image-based header. A new three-column layout was introduced to highlight key features or steps of the application. Corresponding CSS adjustments were made in `static/css/custom_css.css` to style the new hero section and refine the background colors for cards and the footer, ensuring a consistent dark theme.

## fa036679c2162f39318bd53ef5616f9318babfba
**Author:** Peremil
**Date:** Thu Jun 26 12:12:54 2025 +0200
**Message:** refactored progress.py into helpers
**Summary:** Modified `GEMINI.md`, `routes/progress.py`, and `utils/progress_helpers.py`. Overall, 256 insertions and 203 deletions.
**Detailed Description:** This commit refactors the `progress.py` route by extracting its data retrieval and calculation logic into a new utility module, `utils/progress_helpers.py`. This improves modularity and maintainability by centralizing functions for fetching user statistics, points data, streak information, top days, and weekday performance. The `routes/progress.py` file was updated to import and utilize these new helper functions. Additionally, `GEMINI.md` was updated to reflect this change in project structure and highlight the role of the new `progress_helpers.py` module.

## d09da881bccfed7280c715eac5bda133b0fa5669
**Author:** Peremil
**Date:** Wed Jun 25 20:20:04 2025 +0200
**Message:** refactored javascript and css
**Summary:** Modified multiple files including `static/css/pdf_journey.css`, `static/js/progress/charts.js`, `static/js/progress/entries.js`, `static/js/progress/export.js`, `static/js/progress/main.js`, `templates/pdf/journey.html`, `templates/progress.html`, and `utils/pdf_generator.py`. Overall, 493 insertions and 313 deletions.
**Detailed Description:** This commit focuses on refactoring the JavaScript and CSS for the progress page and PDF generation. It extracts the inline CSS from `templates/pdf/journey.html` into a new dedicated stylesheet `static/css/pdf_journey.css`, improving separation of concerns and maintainability. Similarly, the JavaScript logic for charts, entry toggles, and export functionality on the progress page was modularized into separate files: `static/js/progress/charts.js`, `static/js/progress/entries.js`, `static/js/progress/export.js`, and `static/js/progress/main.js`. The `templates/progress.html` was updated to import these new JavaScript modules. The `utils/pdf_generator.py` was also modified to load the external `pdf_journey.css` file when generating PDFs.

## dd9f29913385b1084b9a0e8c80a4ef67498ba70d
**Author:** Peremil
**Date:** Tue Jun 24 22:15:29 2025 +0200
**Message:** added export functionality
**Summary:** Modified multiple files including `requirements.txt`, `routes/progress.py`, `static/css/custom_css.css`, `templates/pdf/journey.html`, `templates/progress.html`, and `utils/pdf_generator.py`. Overall, 604 insertions and 5 deletions.
**Detailed Description:** This commit introduces the PDF export functionality to the progress page. It adds a new route `/export-journey` in `routes/progress.py` that handles the generation and serving of a PDF report. This report includes user's diary entries, points data, and weekday performance charts. To achieve this, several new dependencies were added to `requirements.txt`, including `WeasyPrint` for HTML to PDF conversion and `matplotlib` for generating static chart images. A new utility module `utils/pdf_generator.py` was created to encapsulate the PDF generation logic, including creating charts and embedding them into an HTML template (`templates/pdf/journey.html`). The `templates/progress.html` was updated to include an "Export Journey" button and a loading overlay for the export process, with corresponding CSS in `static/css/custom_css.css` for styling.

## e47905284322866dff12e66f524237fe197c637d
**Author:** Peremil
**Date:** Sun Jun 22 21:54:24 2025 +0200
**Message:** added bar chart over points/weekdays
**Summary:** Modified `routes/progress.py` and `templates/progress.html`. Overall, 124 insertions and 74 deletions.
**Detailed Description:** This commit introduces a new bar chart to the progress dashboard, visualizing the user's average points per day of the week. In `routes/progress.py`, logic was added to calculate average points for each weekday and determine if there is sufficient data (at least two different weekdays with two or more entries each) to display meaningful insights. Sample data is provided for the chart when real data is insufficient. The previous "Best Day" and "Worst Day" text messages were removed, as their functionality is now superseded by this new chart. In `templates/progress.html`, a new section was added to display this "Average Points by Day of Week" chart. An overlay is shown over the chart when there isn't enough data, guiding the user to write more entries to unlock this feature. The JavaScript for rendering this chart was added directly within the `progress.html` template.

## 8d4c1e023267b9796d9a3c101acdb929b8ab9c7b
**Author:** Peremil
**Date:** Sun Jun 22 07:46:50 2025 +0200
**Message:** added config.py, refactoring done
**Summary:** Modified `config.py` and `web_app.py`. Overall, 94 insertions and 31 deletions.
**Detailed Description:** This commit introduces a `config.py` file to centralize application configuration settings, including database URIs, secret keys, and environment-specific settings (development, production, testing). It also refactors `web_app.py` to implement an application factory pattern (`create_app`). This change improves the application's modularity and testability by allowing different configurations to be loaded dynamically. The `SECRET_KEY` is now loaded from environment variables via `python-dotenv`, and a validation step ensures its presence. The database initialization (`db.init_app`) is moved into the `create_app` function, and `db.create_all()` is called within an application context when the script is run directly.

## a0e793b5f8d68348504161d8571504245242f084
**Author:** Peremil
**Date:** Sun Jun 22 07:29:31 2025 +0200
**Message:** refactored all routes
**Summary:** Modified multiple files including `routes/__init__.py`, `routes/auth.py`, `routes/diary.py`, `routes/progress.py`, `routes/reader.py`, and `web_app.py`. Overall, 451 insertions and 412 deletions.
**Detailed Description:** This commit refactors the application's routing by introducing Flask Blueprints for better organization and modularity. Separate blueprints were created for authentication (`routes/auth.py`), diary entries (`routes/diary.py`), progress tracking (`routes/progress.py`), and diary reading (`routes/reader.py`). A new `routes/__init__.py` file was added to register these blueprints with the main Flask application. This change significantly reduces the size and complexity of `web_app.py` by moving route definitions and their associated logic into dedicated modules, improving code readability and maintainability.

## 6ffa0bcb4b1cb3ba7d28cd0536d32815c6edeb6c
**Author:** Peremil
**Date:** Sun Jun 22 07:07:34 2025 +0200
**Message:** moved the search functions into swperate  utils
**Summary:** Modified `utils/__init__.py`, `utils/search_helpers.py`, and `web_app.py`. Overall, 84 insertions and 73 deletions.
**Detailed Description:** This commit refactors the search functionality by moving the `handle_search` and `create_search_snippet` functions from `web_app.py` into a new dedicated utility module, `utils/search_helpers.py`. An `__init__.py` file was added to the `utils` directory to make these functions importable. This change improves code organization and separation of concerns, making the codebase more modular and easier to manage. The `web_app.py` file was updated to import these functions from the new `utils` module.

## 29687e3fc8872b9822ad9ea7d57d48665347fca3
**Author:** Peremil
**Date:** Sun Jun 22 07:01:09 2025 +0200
**Message:** moved the database and model creation to seperate -py
**Summary:** Modified multiple files including `models/__init__.py`, `models/daily_stats.py`, `models/database.py`, `models/diary_entry.py`, `models/user.py`, and `web_app.py`. Overall, 56 insertions and 53 deletions.
**Detailed Description:** This commit refactors the database and model definitions by moving them into a new `models/` directory. Specifically, `database.py` now initializes the SQLAlchemy `db` object, and separate files (`user.py`, `diary_entry.py`, `daily_stats.py`) define the respective SQLAlchemy models. An `__init__.py` file in the `models/` directory makes these models easily importable. This change significantly cleans up `web_app.py` by removing the inline model definitions and database configuration, promoting better code organization and separation of concerns.

## 605ced1600aa9a6ebfa182258a5ec3e051d02cb8
**Author:** Peremil
**Date:** Wed Jun 18 23:36:05 2025 +0200
**Message:** added seach functionality for the diary
**Summary:** Modified `templates/progress.html`, `templates/read_diary.html`, and `web_app.py`. Overall, 172 insertions and 18 deletions.
**Detailed Description:** This commit introduces search functionality to the diary reader. Users can now search their diary entries by text content and/or date. The `templates/read_diary.html` was updated to include a search form and display search results with highlighted keywords. The `web_app.py` file was modified to handle search queries, filter entries based on the search criteria, and generate snippets for display. Minor adjustments were also made to `templates/progress.html` related to chart zoom functionality.

## 7804f0d5a33f4c61364e2c900e9f382c8633cce9
**Author:** Peremil
**Date:** Mon Jun 16 20:57:00 2025 +0200
**Message:** updated readme
**Summary:** Modified `README.md`. Overall, 1 insertion and 1 deletion.
**Detailed Description:** This commit updates the `README.md` file to replace the placeholder `[Your Name]` with the actual author's name, "Peremil Starklint Söderström," in the copyright notice. This change personalizes the project's attribution.

## f5c86040572bced4254bf4418bf41ec1136db703
**Author:** Peremil
**Date:** Mon Jun 16 20:54:49 2025 +0200
**Message:** Remove users.db from tracking
**Summary:** Modified `users.db`. Overall, 0 insertions and 0 deletions.
**Detailed Description:** This commit removes the `users.db` file from Git tracking. This is typically done to prevent the database file, which often contains sensitive user data and is dynamically generated, from being committed to the version control system. This ensures that the database schema is managed through migrations (if applicable) and that local development databases do not interfere with the repository.

## 2839a5ca68f5ffbc63224c916ea2e21e28e51ac1
**Author:** Peremil
**Date:** Mon Jun 16 20:51:05 2025 +0200
**Message:** added .env file for flask key
**Summary:** Modified `web_app.py`. Overall, 7 insertions and 4 deletions.
**Detailed Description:** This commit introduces the use of a `.env` file to manage the Flask `SECRET_KEY`. The `web_app.py` file was modified to load environment variables using `python-dotenv` and retrieve the `SECRET_KEY` from `os.environ`. A `ValueError` is now raised if the `SECRET_KEY` is not set, ensuring that the application's security is not compromised by a missing key. This change improves security practices by externalizing sensitive configuration.

## 8d974c23945cc1aa61897f910837a19c421e5b32
**Author:** Peremil
**Date:** Sun Jun 15 20:13:06 2025 +0200
**Message:** added readme and license information
**Summary:** Modified `LICENSE`, `README.md`, and `web_app.py`. Overall, 227 insertions.
**Detailed Description:** This commit introduces the `LICENSE` file, specifying the Apache License 2.0 for the project. It also updates the `README.md` to include a new section detailing the licensing information and a placeholder for project support/donations. Additionally, a license header comment was added to the `web_app.py` file, ensuring that the license terms are clearly stated within the main application file.

## 655f447a2b71229d3a634291c156d06ec83499a7
**Author:** Peremil
**Date:** Sun Jun 15 19:54:34 2025 +0200
**Message:** updated the readme and added requirements.txt
**Summary:** Modified `README.md` and `requirements.txt`. Overall, 119 insertions and 2 deletions.
**Detailed Description:** This commit significantly updates the `README.md` file to provide a comprehensive overview of the "My Inner Scope" project. It now includes sections on the application's purpose, features (current and planned), technical stack, installation instructions, and database schema. This makes the README a much more informative resource for new contributors or users. Additionally, a `requirements.txt` file was added, listing all Python dependencies required to run the application, ensuring easier setup and dependency management.

## 758ce092e6621221f678d51d2b322964b6fd3941
**Author:** Peremil
**Date:** Sun Jun 15 19:18:00 2025 +0200
**Message:** finished basic complete diary book
**Summary:** Modified `templates/read_diary.html` and `web_app.py`. Overall, 116 insertions and 13 deletions.
**Detailed Description:** This commit completes the basic implementation of the diary reading feature. The `templates/read_diary.html` was significantly updated to display diary entries for a specific date, including navigation buttons for previous and next days. It also introduces an empty state message when no entries are available and a front page view displaying the user's first entry date. The `web_app.py` file was modified to handle the `/read-diary` route, fetching entries based on the provided date parameter, determining navigation links, and formatting the date for display. It also includes logic to handle cases where no entries exist or an invalid date is provided.

## 366a365bd26632f65442433d4ecaa71a8f779511
**Author:** Peremil
**Date:** Sun Jun 15 19:02:39 2025 +0200
**Message:** started on the complete diary page
**Summary:** Modified `templates/diary.html`, `templates/progress.html`, `templates/read_diary.html`, and `web_app.py`. Overall, 72 insertions.
**Detailed Description:** This commit begins the implementation of a dedicated diary reading page. A new HTML template, `templates/read_diary.html`, was created to serve as the interface for viewing past diary entries. The navigation bars in `templates/diary.html` and `templates/progress.html` were updated to include a link to this new "Read diary" page. In `web_app.py`, a new route `/read-diary` was added to render this page, initially displaying a basic template and handling the retrieval of the user's first diary entry date to determine if any entries exist.

## b1fb55773804a69b8462715f9c725bf5a1fd2932
**Author:** Peremil
**Date:** Sat Jun 14 20:59:20 2025 +0200
**Message:** fixed the dynamic navbar showing user name
**Summary:** Modified `templates/diary.html`, `templates/progress.html`, and `web_app.py`. Overall, 30 insertions and 13 deletions.
**Detailed Description:** This commit addresses an issue where the dynamic navigation bar was not correctly displaying the user's name on the diary and progress pages. The `web_app.py` file was updated to fetch the `display_name` (either the user's `user_name` or a truncated version of their email) and pass it to the `diary.html` and `progress.html` templates. The templates were then modified to use this `display_name` in the navigation bar, ensuring a personalized welcome message for logged-in users.

## 2a3b5ab500afb81d4190b2654b075f184f32a2de
**Author:** Peremil
**Date:** Wed Jun 11 20:16:40 2025 +0200
**Message:** added last card comparing 7 days and zoom in graph.
**Summary:** Modified `templates/progress.html` and `web_app.py`. Overall, 78 insertions and 4 deletions.
**Detailed Description:** This commit enhances the progress dashboard by adding a "Weekly Trend" card and enabling zoom and pan functionality for the points chart. In `web_app.py`, logic was added to calculate the trend of points earned over the last two weeks (current 7 days vs. previous 7 days) and generate a corresponding message. The `templates/progress.html` was updated to display this new "Weekly Trend" card. Additionally, the Chart.js configuration for the points chart in `templates/progress.html` was modified to enable `chartjs-plugin-zoom`, allowing users to zoom and pan the chart using the mouse wheel and pinch gestures.

## d299bc509836df52ea7ad538182fcd2a76eb108d
**Author:** Peremil
**Date:** Tue Jun 10 19:09:52 2025 +0200
**Message:** added worst/best day logic
**Summary:** Modified `templates/progress.html` and `web_app.py`. Overall, 89 insertions and 2 deletions.
**Detailed Description:** This commit enhances the progress dashboard by introducing logic to identify and display the user's best and worst performing days of the week based on average points. In `web_app.py`, new calculations were added to determine average points for each weekday. If sufficient data is available (at least two different weekdays with two or more entries each), the system generates a random motivational message for the best day and a constructive message for the worst day. These messages are then displayed in new "Your Best Day" and "Room for Growth" cards on the `templates/progress.html` page. These cards are conditionally rendered, appearing only when enough data has been collected to provide meaningful insights.

## ce310918eb3ec59c5f100e7876ba9a4bb8621cb2
**Author:** Peremil
**Date:** Tue Jun 10 18:46:24 2025 +0200
**Message:** added top 3 days
**Summary:** Modified `templates/progress.html` and `web_app.py`. Overall, 84 insertions and 2 deletions.
**Detailed Description:** This commit introduces the "Your Top 3 Days" section to the progress dashboard. In `web_app.py`, logic was added to query the `DailyStats` for the top 3 days with the most points for the current user, and to fetch all associated diary entries for those days. The `templates/progress.html` was updated to display these top days in a new section, showing the date, points, and a preview of the diary entries. A JavaScript function `toggleEntry` was also added to `templates/progress.html` to allow users to expand and collapse the full content of the diary entries within this section.

## 474e5f29d90a68055a96cd9b3bc17828fb4f634f
**Author:** Peremil
**Date:** Fri Jun 6 15:37:58 2025 +0200
**Message:** added graph to progess route
**Summary:** Modified `templates/progress.html`, `users.db`, and `web_app.py`. Overall, 54 insertions and 1 deletion.
**Detailed Description:** This commit integrates a cumulative points graph into the progress dashboard. In `web_app.py`, logic was added to fetch historical daily points data and calculate cumulative points over time. This data is then passed to the `templates/progress.html`. The `templates/progress.html` was updated to include a new canvas element for the chart and JavaScript code to render a line graph using Chart.js, Luxon, and chartjs-adapter-luxon. This graph visualizes the user's total points earned over their journey. The `users.db` file was also touched, likely due to a local database operation during development, but no functional changes are implied.

## 2c31c29b20ad45f49eebfae88d9f0a6cc3ee371f
**Author:** Peremil
**Date:** Tue May 27 00:33:38 2025 +0200
**Message:** tried to solve a crash
**Summary:** Modified `web_app.py`. Overall, 18 insertions and 4 deletions.
**Detailed Description:** This commit addresses a potential crash in `web_app.py` related to how daily statistics and streaks are handled. The logic for initializing `DailyStats` was refined to ensure that a new `DailyStats` entry is created only if one doesn't already exist for the current day. Previously, the condition for creating a new `DailyStats` entry was overly complex and could lead to incorrect streak calculations or crashes. The update simplifies this logic, ensuring that streaks are correctly continued or started, and points are added to the correct `DailyStats` record.

## cec06fb6aaee7bf985b911a198185ec5960a0ed6
**Author:** Peremil
**Date:** Sun May 25 18:34:57 2025 +0200
**Message:** updated point changes on new branch
**Summary:** Modified `web_app.py`. Overall, 14 insertions and 1 deletion.
**Detailed Description:** This commit refines the logic for handling daily points and streaks in `web_app.py`. It modifies the `diary_entry` function to ensure that `DailyStats` are correctly initialized or updated, particularly when a user makes their first entry of the day or continues a streak. Additionally, the `login_page` function was updated to create a `DailyStats` entry with 1 point for the current day upon successful login if one doesn't already exist. This ensures that a user's daily progress is tracked from the moment they log in.

## 6461ba80fe1c93c8846ebc261159024e90741570
**Author:** Peremil
**Date:** Sun May 25 09:03:40 2025 +0200
**Message:** added features to the dashboard
**Summary:** Modified `templates/progress.html` and `web_app.py`. Overall, 76 insertions and 13 deletions.
**Detailed Description:** This commit enhances the progress dashboard by adding key statistics and displaying them in a card-based layout. In `web_app.py`, logic was implemented to retrieve and calculate `points_today`, `total_points`, `current_streak`, `longest_streak`, and `total_entries` for the logged-in user. These calculated values are then passed to the `templates/progress.html`. The `templates/progress.html` was updated to display these statistics using Bootstrap cards, replacing the previous placeholder text. This provides users with a quick overview of their progress.

## bb738313ed1de3a832f786c0f7a18db0570b7d84
**Author:** Peremil
**Date:** Sat May 24 23:00:25 2025 +0200
**Message:** added points database. and logic to diary route
**Summary:** Modified `templates/diary.html`, `templates/progress.html`, and `web_app.py`. Overall, 59 insertions and 5 deletions.
**Detailed Description:** This commit introduces the core points and streak tracking system to the application. A new `DailyStats` SQLAlchemy model was added to the database, designed to store daily points, current streak, and longest streak for each user. The `diary_entry` route in `web_app.py` was updated to incorporate logic for calculating and updating these daily statistics: it now checks for existing daily stats, calculates streaks based on previous entries, and awards points (5 for 'encouraged' and 2 for 'want to change' behaviors). Additionally, the `login_page` was modified to ensure a `DailyStats` entry is created for the current day upon successful login if one doesn't already exist. Minor adjustments were also made to the navigation bar links in `templates/diary.html` and `templates/progress.html`.

## 4edf2987b5176979c1455b322fc0314ab6139a53
**Author:** Peremil
**Date:** Fri May 23 22:37:55 2025 +0200
**Message:** added sign up button to frontpage and change navbar on /progress
**Summary:** Modified `templates/index.html` and `templates/progress.html`. Overall, 2 insertions and 2 deletions.
**Detailed Description:** This commit makes minor adjustments to the frontend. In `templates/index.html`, the "Sign up" button on the front page was updated to correctly link to the `/register` route. Additionally, the navigation bar on the `/progress` page (`templates/progress.html`) was modified to change its active link from "Diary" to "Progress", ensuring the correct page is highlighted when the user is on the progress dashboard.

## c29deb37a23217d1169af1955dde8b26bb9d24ca
**Author:** Peremil
**Date:** Fri May 23 21:56:27 2025 +0200
**Message:** added user sessions
**Summary:** Modified `templates/diary.html`, `templates/progress.html`, `web_app.py`, and `web_server.code-workspace`. Overall, 28 insertions and 9 deletions.
**Detailed Description:** This commit introduces user session management to the application. The `web_app.py` file was updated to enable Flask sessions by setting a `secret_key`. The `login_page` function now stores the `user.id` in the session upon successful login, and the `diary_entry` and `progress` routes were modified to require a logged-in user by checking for `user_id` in the session. A new `/logout` route was added to clear the user session. The navigation bars in `templates/diary.html` and `templates/progress.html` were updated to reflect the new logout functionality. Additionally, a `.code-workspace` file was added, likely for VS Code, to define the project workspace.

## a9b872834099107d5bb4bb0c8d39428b0538b474
**Author:** Peremil
**Date:** Mon May 19 20:29:35 2025 +0200
**Message:** added tables for entries
**Summary:** Modified `static/css/custom_css.css`, `templates/diary.html`, and `web_app.py`. Overall, 47 insertions and 15 deletions.
**Detailed Description:** This commit introduces the `DiaryEntry` SQLAlchemy model to store user diary entries, including content and a rating. The `web_app.py` file was updated to define this new model and to handle POST requests to the `/diary` route, allowing users to submit their diary entries. Submitted entries are saved to the database with a placeholder `user_id` and a rating. The `templates/diary.html` was modified to include a form for submitting diary entries, with a textarea for content and buttons for rating. Minor styling adjustments were also made in `static/css/custom_css.css` to accommodate the new diary input field.

## 194f73f1dc6768e0538c9d7df288e09539899182
**Author:** Peremil
**Date:** Sun May 18 21:06:16 2025 +0200
**Message:** added some styling to progress.html
**Summary:** Modified `templates/progress.html`. Overall, 43 insertions and 1 deletion.
**Detailed Description:** This commit adds initial styling and structure to the `progress.html` page. It integrates the `custom_css.css` stylesheet and includes a basic navigation bar. The page now displays a main heading "Your Progress" and a subheading "A summary of your journey so far." Below this, a container with a row of three columns is set up, each with a card for displaying progress metrics like "Total Points," "Current Streak," and "Weekly Summary," currently showing "Coming soon..." placeholders. This sets up the visual framework for the progress dashboard.

## 927a4c5e024d05faf52fad757c40f57cebb89022
**Author:** Peremil
**Date:** Sun May 18 20:50:22 2025 +0200
**Message:** added skeleton for progress page
**Summary:** Modified `templates/diary.html`, `templates/progress.html`, and `web_app.py`. Overall, 22 insertions and 2 deletions.
**Detailed Description:** This commit lays the groundwork for the progress tracking page. A new HTML file, `templates/progress.html`, was created to serve as a placeholder for the user's progress dashboard. The `web_app.py` file was updated to include a new route `/progress` that renders this new template. Additionally, the navigation bar in `templates/diary.html` was modified to include a link to the new `/progress` route, allowing users to navigate to their progress page.

## 7e3f9c36b194c9228a08181c0537150d7c58a5b5
**Author:** Peremil
**Date:** Sat May 17 20:49:13 2025 +0200
**Message:** added password hashing
**Summary:** Modified `web_app.py`. Overall, 7 insertions and 2 deletions.
**Detailed Description:** This commit enhances the security of user authentication by implementing password hashing using `werkzeug.security`. The `web_app.py` file was updated to use `generate_password_hash` when a new user registers, storing a secure hash of the password instead of the plain text. For login, `check_password_hash` is now used to verify the entered password against the stored hash. This significantly improves the application's security by protecting user credentials.

## 2f554d93f4b98f3e3f47d733a3395026cf71c532
**Author:** Peremil
**Date:** Fri May 16 18:51:06 2025 +0200
**Message:** added get/post to login, register
**Summary:** Modified `templates/login.html`, `templates/register.html`, and `web_app.py`. Overall, 69 insertions and 29 deletions.
**Detailed Description:** This commit implements the GET and POST request handling for the login and registration pages. In `web_app.py`, the `/login` and `/register` routes were updated to process form submissions. For login, it now checks if a user exists with the provided email and verifies the password. For registration, it validates that passwords match, checks for existing email addresses, and creates a new user in the database. The `templates/login.html` and `templates/register.html` were modified to include `method="POST"` and `action` attributes in their forms, along with `name` attributes for input fields, enabling proper form submission.

## cd31561fe56d88789c7df6c11338c4368816ac4d
**Author:** Peremil
**Date:** Fri May 16 17:16:39 2025 +0200
**Message:** set up a sqlite server with sqlalchemy
**Summary:** Modified `templates/login.html` and `web_app.py`. Overall, 21 insertions and 1 deletion.
**Detailed Description:** This commit sets up a SQLite database using SQLAlchemy for the application. The `web_app.py` file was updated to configure SQLAlchemy, connect to a `users.db` SQLite file, and define the `User` model with fields for `id`, `email`, `password`, and `user_name`. The `db.create_all()` function is called within an application context to create the database tables on application startup. Additionally, the `templates/login.html` was updated to correct a link to the registration page in the navigation menu.

## b7692ba58e68e0b575ac2d30580afdc0c5cd3479
**Author:** Peremil
**Date:** Tue May 13 17:07:51 2025 +0200
**Message:** added submitbutton to register form
**Summary:** Modified `templates/register.html`. Overall, 1 insertion.
**Detailed Description:** This commit adds a submit button to the registration form in `templates/register.html`. Previously, the form lacked a clear way for users to submit their registration details. This change introduces a Bootstrap-styled primary button with the text "Submit", allowing users to complete the registration process.

## 0289bb221347f94fc9dfa32a46f76aa7d3b7ccc4
**Author:** Peremil
**Date:** Tue May 13 17:02:21 2025 +0200
**Message:** added register page
**Summary:** Modified `static/css/custom_css.css`, `templates/index.html`, `templates/register.html`, and `web_app.py`. Overall, 69 insertions and 1 deletion.
**Detailed Description:** This commit introduces a new registration page to the application. A new HTML file, `templates/register.html`, was created to provide a form for user registration, including fields for email, name, password, and password confirmation, along with a checkbox for agreeing to terms of service. The `web_app.py` file was updated to include a new route `/register` that renders this registration page. The `templates/index.html` was modified to add a link to the new registration page in the navigation menu. Additionally, `static/css/custom_css.css` was updated to include styling for the new registration form.

## 3841f88ee73a78168cb23579d7ac9b1c45b09d64
**Author:** Peremil
**Date:** Mon May 12 20:14:08 2025 +0200
**Message:** added log in page:)
**Summary:** Modified `static/css/custom_css.css`, `templates/index.html`, `templates/login.html`, and `web_app.py`. Overall, 58 insertions and 3 deletions.
**Detailed Description:** This commit introduces a new login page to the application. A new HTML file, `templates/login.html`, was created to provide a form for user login, including fields for email and password. The `web_app.py` file was updated to include a new route `/login` that renders this login page. The `templates/index.html` was modified to add a link to the new login page in the navigation menu. Additionally, `static/css/custom_css.css` was updated to include styling for the new login form.

## bc05841f63d363601077573db91d496fdc9dfcdb
**Author:** Peremil
**Date:** Sun May 11 17:40:15 2025 +0200
**Message:** Added diary page and started design
**Summary:** Modified `static/css/custom_css.css`, `templates/diary.html`, and `web_app.py`. Overall, 72 insertions.
**Detailed Description:** This commit introduces the diary entry page to the application. A new HTML file, `templates/diary.html`, was created to provide a basic interface for users to write daily entries, including a textarea for content and two buttons for rating their behavior ("I want to change this behaviour" and "This is encouraged"). The `web_app.py` file was updated to include a new route `/diary` that renders this diary page. Additionally, `static/css/custom_css.css` was updated to include styling for the new diary input field and the rating buttons, and the navigation bar in `templates/diary.html` was set up.

## c3d2e0061e84ed377293669702b5b5dfcbfd5d92
**Author:** Peremil
**Date:** Sat May 10 20:56:28 2025 +0200
**Message:** removed file
**Summary:** Modified `log_in_info.py`. Overall, 4 deletions.
**Detailed Description:** This commit removes the `log_in_info.py` file from the project. This file previously contained hardcoded user login information, which is not a secure practice for storing credentials. Its removal indicates a move towards a more secure authentication system, likely involving a database for user management.

## 83f4331bd34af6a7ddf443ddbb6f46cb3796e13a
**Author:** Peremil
**Date:** Sat May 10 20:52:04 2025 +0200
**Message:** added more styling, dark background
**Summary:** Modified `static/css/custom_css.css` and `templates/index.html`. Overall, 25 insertions and 6 deletions.
**Detailed Description:** This commit introduces significant styling changes to the application, primarily focusing on establishing a dark, sci-fi inspired theme. In `static/css/custom_css.css`, new CSS rules were added to set a dark background for the `body` and navigation bar, and to apply a text shadow effect for headings. The navigation bar in `templates/index.html` was updated to use the new custom dark styling. The main heading on the index page was also modified to use a bold font and the new text shadow. This commit aims to enhance the visual appeal and consistency of the application's user interface.

## b3050f1db967eb43631beebf708bd49d76959c52
**Author:** Peremil
**Date:** Sat May 10 13:01:34 2025 +0200
**Message:** added navbar, hero image, and columns
**Summary:** Modified `static/assets/starry_sky.jpg`, `static/css/custom_css.css`, and `templates/index.html`. Overall, 27 insertions and 1 deletion.
**Detailed Description:** This commit introduces significant visual enhancements to the `index.html` page. A new navigation bar was added, providing basic navigation options. A hero section with a background image (`static/assets/starry_sky.jpg`) was implemented to create a more engaging landing experience. Below the hero section, a three-column layout was introduced to highlight key steps or features of the application. A new `static/css/custom_css.css` file was created to house custom styles for these new elements, ensuring a consistent design.

## 6a3f4d937acb6dfe3562794629e864d8479731a1
**Author:** Peremil
**Date:** Sat May 10 11:51:34 2025 +0200
**Message:** started on the real pagelayout
**Summary:** Modified `templates/index.html` and `web_app.py`. Overall, 22 insertions and 11 deletions.
**Detailed Description:** This commit marks the beginning of a more structured page layout for the application. The `templates/index.html` file was significantly updated to include a basic Bootstrap navigation bar with a dropdown menu for future links like "Register", "Log in", "About", and "Donate". The previous simple "Welcome" heading and diary input elements were removed. The `web_app.py` file was also updated to remove the dependency on `log_in_info` and to render `index.html` without passing any `signed` variable, reflecting the shift towards a more dynamic and user-driven content display.

## 4ee868ecceb5544be010b53e4310464de14a32b0
**Author:** Peremil
**Date:** Fri May 9 15:31:35 2025 +0200
**Message:** trying out flask stuff + html
**Summary:** Modified `log_in_info.py`, `templates/index.html`, and `web_app.py`. Overall, 11 insertions and 2 deletions.
**Detailed Description:** This commit introduces initial Flask integration and dynamic content rendering. A new file `log_in_info.py` was added to store placeholder user information. The `web_app.py` file was updated to import this user data and pass it to the `templates/index.html` when rendering the homepage. The `templates/index.html` was modified to dynamically display a list of signed-up users, demonstrating basic Jinja2 templating and Flask's ability to pass data to templates.

## 8457bea87a94a092d500c4c2966c70bfda41094f
**Author:** Peremil
**Date:** Fri May 9 07:08:17 2025 +0200
**Message:** just trying out adding button and text input
**Summary:** Modified `templates/index.html`. Overall, 2 insertions.
**Detailed Description:** This commit adds a basic text input field and a submit button to the `templates/index.html` file. This is a preliminary step to test user interaction elements within the web application, allowing for a simple diary entry input and submission mechanism.

## 01f7557a38f5cf42de5815505e32657e5a563983
**Author:** Peremil
**Date:** Thu May 8 22:27:56 2025 +0200
**Message:** started webserver project
**Summary:** Modified `templates/index.html` and `web_app.py`. Overall, 22 insertions.
**Detailed Description:** This commit marks the initial setup of the web server project. It introduces the basic Flask application structure with `web_app.py` as the main entry point. A simple HTML template `templates/index.html` was created, displaying a welcome message and a brief description of the application. The Flask app is configured to render this `index.html` for the root route (`/`).

## 3982a165c3586e53e6ea6ad58e4d39be3e166e4f
**Author:** PapaPandroni
**Date:** Thu May 8 21:48:21 2025 +0200
**Message:** Initial commit
**Summary:** Modified `.gitignore` and `README.md`. Overall, 176 insertions.
