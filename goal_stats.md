# Plan for Implementing Goal Statistics

This document outlines the plan to add goal-related statistics to the progress page.

### Ideas for Goal Statistics

*   **Goal Success Rate:** A percentage showing how many of their past goals (that are no longer in progress) they have successfully completed. This provides a great motivational metric.
*   **Category Success Breakdown:** Instead of just showing completed goals per category, we can create a stacked bar chart that shows both *completed* and *failed* goals for each category. This would give the user a much clearer picture of which areas they are excelling in and which might need more focus.
*   **New Stat Cards:** We can add new summary cards for "Total Goals Completed" and "Goal Success Rate" to the overview section for quick insights.

### Implementation Plan

Here is a step-by-step plan to implement these new features:

**Part 1: Backend - Gathering the Data**

1.  **Create a New Helper Function:** In `utils/goal_helpers.py`, create a new function called `get_goal_statistics(user_id)`. This function will be responsible for calculating all the goal-related stats. It will:
    *   Query the database for all of the user's goals that have a status of `completed` or `failed`.
    *   Calculate the total number of completed goals.
    *   Calculate the goal success rate.
    *   Aggregate the number of completed and failed goals for each category and return this data in a format that is easy to use for a chart.

2.  **Update the Progress Route:** In `routes/progress.py`:
    *   Call the new `get_goal_statistics` function to get the goal stats for the current user.
    *   Pass these new statistics to the `progress.html` template so they can be displayed.

**Part 2: Frontend - Displaying the Statistics**

1.  **Update the Progress Template (`templates/progress.html`):**
    *   **Add New Stat Cards:** Add two new cards to the "Exploration Overview" section to display the "Total Goals Completed" and "Goal Success Rate".
    *   **Add a New Chart:** Add a new section for "Goal Performance by Category" with a new chart.
    *   **Implement a "Locked" State:** Just like the other charts, if a user doesn't have any completed or failed goals yet, show a "locked" message to encourage them to set and complete goals.

2.  **Update the Charting Logic (`static/js/progress/charts.js`):**
    *   Add a new function to create the "Goal Performance by Category" chart.
    *   This chart will be a **stacked bar chart**, with each bar representing a category. The bar will be segmented to show the number of completed goals and failed goals.
    *   The chart will be styled to match the existing "sci-fi" theme of the application.
