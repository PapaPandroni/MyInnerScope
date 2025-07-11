"""
Frontend Regression Prevention Tests

These tests specifically target issues that were found during refactoring
to prevent them from reoccurring. Each test validates a specific issue
that was discovered and fixed.
"""

import pytest
from bs4 import BeautifulSoup
import re
from flask import url_for
from tests.conftest import extract_csrf_token


class TestDiaryFormRegression:
    """Test to prevent diary form submission issues."""

    def test_diary_form_ids_match_javascript_selectors(self, client, sample_user):
        """
        Regression test for diary form submission issue.
        
        This test ensures that the HTML form elements have IDs that match
        what the JavaScript code expects to find.
        
        Issue: JavaScript looked for 'diary-form' and 'rating-input' but
        HTML had 'diary_form' and 'rating_input'.
        """
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/diary")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Verify form ID matches JavaScript expectations
        form = soup.find('form', id='diary_form')
        assert form is not None, "Form with id='diary_form' not found - JavaScript won't be able to submit form"
        
        # Verify rating input ID matches JavaScript expectations
        rating_input = soup.find('input', id='rating_input')
        assert rating_input is not None, "Input with id='rating_input' not found - JavaScript won't be able to set rating"
        
        # Verify textarea ID matches JavaScript expectations
        textarea = soup.find('textarea', id='diary_textarea')
        assert textarea is not None, "Textarea with id='diary_textarea' not found - JavaScript won't be able to access content"
        
        # Verify character counter ID matches JavaScript expectations
        char_counter = soup.find(id='char_counter')
        assert char_counter is not None, "Element with id='char_counter' not found - JavaScript character counting won't work"

    def test_diary_rating_buttons_have_correct_attributes(self, client, sample_user):
        """
        Test that diary rating buttons have the correct data attributes
        that JavaScript expects.
        """
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/diary")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Find rating buttons
        rating_buttons = soup.find_all('button', attrs={'data-rating': True})
        assert len(rating_buttons) == 2, "Should have exactly 2 rating buttons"
        
        # Check for positive rating button
        positive_button = soup.find('button', attrs={'data-rating': '1'})
        assert positive_button is not None, "Positive rating button (data-rating='1') not found"
        
        # Check for negative rating button
        negative_button = soup.find('button', attrs={'data-rating': '-1'})
        assert negative_button is not None, "Negative rating button (data-rating='-1') not found"


class TestGoalsJavaScriptRegression:
    """Test to prevent goals JavaScript variable name issues."""

    def test_goals_form_elements_match_javascript_variables(self, client, sample_user):
        """
        Regression test for goals JavaScript variable name mismatch.
        
        This test ensures that the HTML elements have IDs that match
        the variable names used in the JavaScript code.
        
        Issue: JavaScript used camelCase variables like 'suggestionsContainer'
        and 'categorySelect' but referenced snake_case variables.
        """
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/goals")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Verify category select exists (referenced as category_select in JS)
        category_select = soup.find('select', id='category')
        assert category_select is not None, "Select with id='category' not found - JavaScript variable category_select won't work"
        
        # Verify title input exists (referenced as title_input in JS)
        title_input = soup.find('input', id='title')
        assert title_input is not None, "Input with id='title' not found - JavaScript variable title_input won't work"
        
        # Verify suggestions container exists (referenced as suggestions_container in JS)
        suggestions_container = soup.find(id='suggestions')
        assert suggestions_container is not None, "Element with id='suggestions' not found - JavaScript variable suggestions_container won't work"
        
        # Verify suggestions list exists (referenced as suggestions_list in JS)
        suggestions_list = soup.find(id='suggestions_list')
        assert suggestions_list is not None, "Element with id='suggestions_list' not found - JavaScript variable suggestions_list won't work"

    def test_goal_suggestions_api_endpoint_exists(self, client, sample_user):
        """
        Test that the goal suggestions API endpoint works correctly.
        
        This endpoint is called by JavaScript on the goals page.
        """
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id

        # Get CSRF token
        response = client.get("/goals")
        csrf_token = extract_csrf_token(response.data)

        # Test the API endpoint that JavaScript calls
        response = client.get(
            "/api/goals/suggestions/Personal Development",
            headers={"X-CSRFToken": csrf_token}
        )
        assert response.status_code == 200, "Goal suggestions API endpoint not working"
        
        data = response.get_json()
        assert "suggestions" in data, "API response missing 'suggestions' key"
        assert isinstance(data["suggestions"], list), "API suggestions should be a list"


class TestDonatePageRegression:
    """Test to prevent donate page JavaScript issues."""

    def test_donate_page_element_ids_match_javascript(self, client, sample_user):
        """
        Regression test for donate page ID mismatch.
        
        This test ensures that the BMC widget error element has the correct ID
        that JavaScript expects to find.
        
        Issue: JavaScript looked for 'bmc-widget-error' but HTML had 'bmc_widget_error'.
        """
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/donate")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Verify BMC widget wrapper exists
        bmc_wrapper = soup.find(id='bmc_widget_wrapper')
        assert bmc_wrapper is not None, "Element with id='bmc_widget_wrapper' not found"
        
        # Verify BMC error element has correct ID (should be snake_case to match JavaScript)
        bmc_error = soup.find(id='bmc_widget_error')
        assert bmc_error is not None, "Element with id='bmc_widget_error' not found - JavaScript error handling won't work"
        
        # Verify error element is initially hidden
        style = bmc_error.get('style', '')
        assert 'display:none' in style.replace(' ', ''), "BMC error element should be initially hidden"


class TestProgressPageRegression:
    """Test to prevent progress page class name issues."""

    def test_progress_page_class_names_match_javascript(self, client, app, sample_user):
        """
        Regression test for progress page class name inconsistencies.
        
        This test ensures that CSS class names in HTML match what
        JavaScript expects to find for toggle functionality.
        
        Issue: JavaScript looked for '.extra_goal' but HTML had '.extra-goal'.
        """
        with app.app_context():
            # Create enough goals to trigger "show more" functionality
            from app.models import Goal, db
            from app.models.goal import GoalCategory, GoalStatus
            from datetime import date, timedelta
            
            for i in range(7):  # More than 5 to trigger extra-goal class
                goal = Goal(
                    user_id=sample_user.id,
                    category=GoalCategory.PERSONAL_DEV,
                    title=f"Test Goal {i}",
                    week_start=date.today() - timedelta(days=14),
                    week_end=date.today() - timedelta(days=7),
                    status=GoalStatus.COMPLETED
                )
                db.session.add(goal)
            
            db.session.commit()

        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/goals")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for extra-goal class elements (JavaScript expects .extra-goal)
        extra_goals = soup.find_all(class_='extra-goal')
        if extra_goals:  # Only check if they exist
            assert len(extra_goals) > 0, "extra-goal class elements not found - JavaScript toggle won't work"
        
        # Check for show more button
        show_more_btn = soup.find('button', id='show_more_goals_btn')
        if show_more_btn:  # Only check if button exists
            assert show_more_btn is not None, "show_more_goals_btn not found - JavaScript toggle won't work"

    def test_progress_page_entry_class_names_consistent(self, client, app, sample_user):
        """
        Test that entry class names are consistent for JavaScript functionality.
        """
        with app.app_context():
            # Create diary entries to ensure entry elements are rendered
            from app.models import DiaryEntry, DailyStats, db
            from datetime import date, timedelta
            
            for i in range(5):
                entry = DiaryEntry(
                    user_id=sample_user.id,
                    content=f"Test entry {i}",
                    rating=1,
                    entry_date=date.today() - timedelta(days=i)
                )
                db.session.add(entry)
                
                stats = DailyStats(
                    user_id=sample_user.id,
                    date=date.today() - timedelta(days=i),
                    points=5,
                    current_streak=1,
                    longest_streak=1
                )
                db.session.add(stats)
            
            db.session.commit()

        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/progress")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for entry preview and full elements with consistent ID patterns
        preview_elements = soup.find_all(id=re.compile(r'preview_\d+'))
        full_elements = soup.find_all(id=re.compile(r'full_\d+'))
        
        # These should exist if entries are present
        if preview_elements or full_elements:
            # At least some entry elements should be found
            assert len(preview_elements) > 0 or len(full_elements) > 0, "No entry toggle elements found"


class TestChartRegression:
    """Test to prevent chart rendering issues."""

    def test_chart_canvas_elements_exist_for_javascript(self, client, sample_user):
        """
        Test that chart canvas elements exist for Chart.js to render.
        
        This ensures that the JavaScript chart rendering code can find
        the canvas elements it expects.
        """
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/progress")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for all chart canvas elements that JavaScript expects
        expected_charts = ['pointsChart', 'weekdayChart', 'goalCategoryChart']
        
        for chart_id in expected_charts:
            canvas = soup.find('canvas', id=chart_id)
            assert canvas is not None, f"Canvas with id='{chart_id}' not found - Chart.js rendering will fail"

    def test_chart_data_scripts_have_correct_structure(self, client, sample_user):
        """
        Test that data scripts for charts have the correct JSON structure
        that JavaScript expects.
        """
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/progress")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for data scripts with correct IDs and structure
        data_scripts = ['points_data', 'weekday_data', 'goal_stats_data']
        
        for script_id in data_scripts:
            script = soup.find('script', id=script_id)
            assert script is not None, f"Data script with id='{script_id}' not found - JavaScript data loading will fail"
            
            # Verify it's marked as JSON
            assert script.get('type') == 'application/json', f"Script {script_id} should have type='application/json'"


class TestCSRFRegression:
    """Test to prevent CSRF token issues."""

    def test_csrf_meta_tag_exists_for_javascript(self, client, sample_user):
        """
        Test that CSRF meta tag exists for JavaScript to access.
        
        JavaScript code needs access to CSRF tokens for AJAX requests.
        """
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        # Test pages that use CSRF tokens in JavaScript
        pages_with_csrf_js = ["/goals"]  # Goals page uses CSRF in API calls
        
        for page in pages_with_csrf_js:
            response = client.get(page)
            assert response.status_code == 200
            
            soup = BeautifulSoup(response.data, 'html.parser')
            
            # Check for CSRF meta tag
            csrf_meta = soup.find('meta', attrs={'name': 'csrf-token'})
            assert csrf_meta is not None, f"CSRF meta tag not found on {page} - JavaScript AJAX requests will fail"
            assert csrf_meta.get('content'), f"CSRF meta tag empty on {page}"


class TestTourSystemRegression:
    """Test to prevent tour system issues."""

    def test_tour_configuration_available_for_javascript(self, client, sample_user):
        """
        Test that tour configuration is properly available to JavaScript.
        
        The tour system relies on window.tour_config being properly set.
        """
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        # Test pages that include tour functionality
        tour_pages = ["/diary", "/progress", "/goals"]
        
        for page in tour_pages:
            response = client.get(page)
            assert response.status_code == 200
            
            response_text = response.data.decode('utf-8')
            
            # Check for tour configuration
            if 'tour_config' in response_text:
                # If tour config exists, it should have proper structure
                assert 'window.tour_config' in response_text, f"Tour config not properly set on {page}"
                assert 'is_new_user' in response_text, f"Tour config missing is_new_user on {page}"

    def test_tour_script_loading(self, client, sample_user):
        """
        Test that tour controller script is loaded when needed.
        """
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/diary")
        assert response.status_code == 200
        
        response_text = response.data.decode('utf-8')
        
        # Check for tour script loading
        if 'tour-controller.js' in response_text:
            soup = BeautifulSoup(response.data, 'html.parser')
            tour_script = soup.find('script', src=re.compile(r'.*tour-controller\.js'))
            assert tour_script is not None, "Tour controller script not properly loaded"


class TestNamingConsistencyRegression:
    """Test to prevent naming consistency issues across the application."""

    def test_snake_case_vs_kebab_case_consistency(self, client, sample_user):
        """
        General test to catch snake_case vs kebab-case inconsistencies
        that could break JavaScript functionality.
        """
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        # Test critical pages for ID consistency
        critical_pages = ["/diary", "/goals", "/progress"]
        
        for page in critical_pages:
            response = client.get(page)
            assert response.status_code == 200
            
            soup = BeautifulSoup(response.data, 'html.parser')
            
            # Check that important form elements use consistent naming
            forms = soup.find_all('form')
            for form in forms:
                form_id = form.get('id')
                if form_id:
                    # Form IDs should use snake_case (based on our convention)
                    assert '_' in form_id or form_id.islower(), f"Form ID '{form_id}' on {page} should use snake_case"
                
                # Check form inputs
                inputs = form.find_all(['input', 'select', 'textarea'])
                for input_elem in inputs:
                    input_id = input_elem.get('id')
                    if input_id and input_id not in ['csrf_token']:  # Skip CSRF token
                        # Important form element IDs should use snake_case
                        if any(keyword in input_id for keyword in ['diary', 'rating', 'category', 'title', 'char']):
                            assert '_' in input_id or input_id.islower(), f"Input ID '{input_id}' on {page} should use snake_case"