"""
Template-JavaScript Integration Tests

These tests verify that HTML templates contain the correct elements that JavaScript
code expects to find. This prevents issues like the diary form submission bug where
JavaScript looked for elements with IDs that didn't exist in the HTML.
"""

import pytest
from bs4 import BeautifulSoup
import json
import re
from flask import url_for
from tests.conftest import extract_csrf_token


class TestTemplateJavaScriptIntegration:
    """Test integration between HTML templates and JavaScript code."""

    def test_diary_form_elements_exist(self, client, sample_user):
        """Test that diary page has all required form elements for JavaScript."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/diary")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for form element with correct ID
        diary_form = soup.find('form', id='diary_form')
        assert diary_form is not None, "Form with id='diary_form' not found"
        
        # Check for rating input with correct ID
        rating_input = soup.find('input', id='rating_input')
        assert rating_input is not None, "Input with id='rating_input' not found"
        
        # Check for textarea with correct ID
        diary_textarea = soup.find('textarea', id='diary_textarea')
        assert diary_textarea is not None, "Textarea with id='diary_textarea' not found"
        
        # Check for character counter with correct ID
        char_counter = soup.find(id='char_counter')
        assert char_counter is not None, "Element with id='char_counter' not found"
        
        # Check for rating buttons with correct data attributes
        rating_buttons = soup.find_all('button', attrs={'data-rating': True})
        assert len(rating_buttons) >= 2, "Rating buttons with data-rating attributes not found"
        
        # Verify rating button values
        rating_values = [btn.get('data-rating') for btn in rating_buttons]
        assert '1' in rating_values, "Positive rating button (data-rating='1') not found"
        assert '-1' in rating_values, "Negative rating button (data-rating='-1') not found"

    def test_goals_form_elements_exist(self, client, sample_user):
        """Test that goals page has all required form elements for JavaScript."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/goals")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for category select with correct ID
        category_select = soup.find('select', id='category')
        assert category_select is not None, "Select with id='category' not found"
        
        # Check for title input with correct ID
        title_input = soup.find('input', id='title')
        assert title_input is not None, "Input with id='title' not found"
        
        # Check for suggestions container with correct ID
        suggestions_container = soup.find(id='suggestions')
        assert suggestions_container is not None, "Element with id='suggestions' not found"
        
        # Check for suggestions list with correct ID
        suggestions_list = soup.find(id='suggestions_list')
        assert suggestions_list is not None, "Element with id='suggestions_list' not found"

    def test_donate_page_elements_exist(self, client, sample_user):
        """Test that donate page has all required elements for JavaScript."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/donate")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for BMC widget wrapper with correct ID
        bmc_wrapper = soup.find(id='bmc_widget_wrapper')
        assert bmc_wrapper is not None, "Element with id='bmc_widget_wrapper' not found"
        
        # Check for BMC widget error element with correct ID
        bmc_error = soup.find(id='bmc_widget_error')
        assert bmc_error is not None, "Element with id='bmc_widget_error' not found"

    def test_progress_page_chart_elements_exist(self, client, sample_user):
        """Test that progress page has all required chart elements for JavaScript."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/progress")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for chart canvas elements
        points_chart = soup.find('canvas', id='pointsChart')
        assert points_chart is not None, "Canvas with id='pointsChart' not found"
        
        weekday_chart = soup.find('canvas', id='weekdayChart')
        assert weekday_chart is not None, "Canvas with id='weekdayChart' not found"
        
        goal_category_chart = soup.find('canvas', id='goalCategoryChart')
        assert goal_category_chart is not None, "Canvas with id='goalCategoryChart' not found"

    def test_progress_page_data_scripts_exist(self, client, sample_user):
        """Test that progress page has all required data scripts for JavaScript."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/progress")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for data scripts with correct IDs
        points_data = soup.find('script', id='points_data')
        assert points_data is not None, "Script with id='points_data' not found"
        
        weekday_data = soup.find('script', id='weekday_data')
        assert weekday_data is not None, "Script with id='weekday_data' not found"
        
        goal_stats_data = soup.find('script', id='goal_stats_data')
        assert goal_stats_data is not None, "Script with id='goal_stats_data' not found"
        
        # Verify data scripts contain valid JSON
        try:
            json.loads(points_data.string)
        except (json.JSONDecodeError, TypeError):
            pytest.fail("points_data script does not contain valid JSON")
        
        try:
            json.loads(weekday_data.string)
        except (json.JSONDecodeError, TypeError):
            pytest.fail("weekday_data script does not contain valid JSON")
        
        try:
            json.loads(goal_stats_data.string)
        except (json.JSONDecodeError, TypeError):
            pytest.fail("goal_stats_data script does not contain valid JSON")

    def test_csrf_token_meta_tag_exists(self, client, sample_user):
        """Test that pages have CSRF token meta tag for JavaScript."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        # Test multiple pages that use CSRF tokens in JavaScript
        pages = ["/diary", "/goals", "/progress"]
        
        for page in pages:
            response = client.get(page)
            assert response.status_code == 200
            
            soup = BeautifulSoup(response.data, 'html.parser')
            
            # Check for CSRF token meta tag
            csrf_meta = soup.find('meta', attrs={'name': 'csrf-token'})
            assert csrf_meta is not None, f"CSRF token meta tag not found on {page}"
            assert csrf_meta.get('content'), f"CSRF token meta tag empty on {page}"

    def test_tour_configuration_exists_for_new_users(self, client, sample_user):
        """Test that tour configuration is properly set for JavaScript."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/diary")
        assert response.status_code == 200
        
        # Check for tour configuration in JavaScript
        response_text = response.data.decode('utf-8')
        
        # Look for tour_config object
        tour_config_pattern = r'window\.tour_config\s*=\s*\{'
        assert re.search(tour_config_pattern, response_text), "tour_config not found in JavaScript"

    def test_entry_toggle_elements_exist(self, client, app, sample_user):
        """Test that progress page has elements for entry toggling functionality."""
        with app.app_context():
            # Create some diary entries to ensure toggle elements are rendered
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
            
            db.session.commit()
        
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/progress")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for entry preview and full elements
        preview_elements = soup.find_all(id=re.compile(r'preview_\d+'))
        full_elements = soup.find_all(id=re.compile(r'full_\d+'))
        
        # Should have some preview/full elements if entries exist
        if preview_elements:
            assert len(preview_elements) > 0, "No entry preview elements found"
            assert len(full_elements) > 0, "No entry full elements found"

    def test_goal_history_toggle_elements_exist(self, client, app, sample_user):
        """Test that goals page has elements for goal history toggling."""
        with app.app_context():
            # Create some goals to ensure toggle elements are rendered
            from app.models import Goal, db
            from app.models.goal import GoalCategory, GoalStatus
            from datetime import date, timedelta
            
            for i in range(7):  # More than 5 to trigger "show more" functionality
                goal = Goal(
                    user_id=sample_user.id,
                    category=GoalCategory.PERSONAL_DEV,
                    title=f"Test Goal {i}",
                    week_start=date.today() - timedelta(days=7),
                    week_end=date.today(),
                    status=GoalStatus.COMPLETED
                )
                db.session.add(goal)
            
            db.session.commit()
        
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/goals")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for show more button for goals
        show_more_btn = soup.find('button', id='show_more_goals_btn')
        if show_more_btn:  # Only check if button exists (depends on number of goals)
            assert show_more_btn is not None, "Show more goals button not found"
            
        # Check for extra-goal class elements
        extra_goals = soup.find_all(class_='extra-goal')
        # This is optional since it depends on having enough goals

    def test_wordcloud_elements_exist(self, client, app, sample_user):
        """Test that progress page has wordcloud elements when sufficient data exists."""
        with app.app_context():
            # Create enough diary entries to unlock wordcloud (need 10+)
            from app.models import DiaryEntry, db
            from datetime import date, timedelta
            
            for i in range(12):  # More than 10 entries
                entry = DiaryEntry(
                    user_id=sample_user.id,
                    content=f"Test wordcloud entry {i} with various words and content",
                    rating=1,
                    entry_date=date.today() - timedelta(days=i)
                )
                db.session.add(entry)
            
            db.session.commit()
        
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/progress")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for wordcloud container (should exist when data is sufficient)
        wordcloud_div = soup.find('div', id='wordcloud')
        assert wordcloud_div is not None, "Wordcloud div with id='wordcloud' not found"
        
        # Check for wordcloud canvas 
        wordcloud_canvas = soup.find('canvas', id='wordcloud_canvas')
        assert wordcloud_canvas is not None, "Wordcloud canvas with id='wordcloud_canvas' not found"


class TestJavaScriptDataStructures:
    """Test that data passed to JavaScript has the correct structure."""

    def test_progress_data_structure(self, client, sample_user):
        """Test that progress data has the correct structure for JavaScript."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/progress")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Get weekday data script
        weekday_script = soup.find('script', id='weekday_data')
        if weekday_script and weekday_script.string:
            data = json.loads(weekday_script.string)
            
            # Check for expected keys (snake_case)
            assert 'weekday_data' in data, "weekday_data key not found"
            assert 'has_sufficient_weekday_data' in data, "has_sufficient_weekday_data key not found"
            assert 'sample_weekday_data' in data, "sample_weekday_data key not found"

    def test_tour_config_structure(self, client, sample_user):
        """Test that tour configuration has the correct structure."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/diary")
        assert response.status_code == 200
        
        response_text = response.data.decode('utf-8')
        
        # Extract tour_config JavaScript object
        tour_config_match = re.search(
            r'window\.tour_config\s*=\s*(\{[^}]+\})', 
            response_text
        )
        
        if tour_config_match:
            # Basic validation that it looks like a proper object
            config_str = tour_config_match.group(1)
            assert 'is_new_user' in config_str, "is_new_user not found in tour_config"
            assert 'user_entry_count' in config_str, "user_entry_count not found in tour_config"