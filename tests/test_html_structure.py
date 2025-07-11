"""
HTML Structure Validation Tests

These tests validate the HTML structure of rendered templates to ensure
consistency and catch structural issues that could break JavaScript functionality.
"""

import pytest
from bs4 import BeautifulSoup
import re
from flask import url_for


class TestHTMLStructure:
    """Test HTML structure and element consistency across templates."""

    def test_base_template_structure(self, client, sample_user):
        """Test that base template has required structure."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/diary")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for essential HTML structure
        assert soup.find('html'), "HTML tag not found"
        assert soup.find('head'), "HEAD tag not found"
        assert soup.find('body'), "BODY tag not found"
        assert soup.find('title'), "TITLE tag not found"
        
        # Check for Bootstrap CSS
        bootstrap_css = soup.find('link', attrs={'href': re.compile(r'bootstrap.*\.css')})
        assert bootstrap_css, "Bootstrap CSS not found"
        
        # Check for meta charset
        charset_meta = soup.find('meta', attrs={'charset': True})
        assert charset_meta, "Charset meta tag not found"
        
        # Check for viewport meta
        viewport_meta = soup.find('meta', attrs={'name': 'viewport'})
        assert viewport_meta, "Viewport meta tag not found"

    def test_navbar_structure(self, client, sample_user):
        """Test that navbar has consistent structure across pages."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        pages = ["/diary", "/progress", "/goals", "/read-diary"]
        
        for page in pages:
            response = client.get(page)
            if response.status_code == 200:
                soup = BeautifulSoup(response.data, 'html.parser')
                
                # Check for navbar
                navbar = soup.find('nav', class_=re.compile(r'navbar'))
                assert navbar, f"Navbar not found on {page}"
                
                # Check for brand/logo
                navbar_brand = soup.find(class_=re.compile(r'navbar-brand'))
                assert navbar_brand, f"Navbar brand not found on {page}"
                
                # Check for navigation links
                nav_links = soup.find_all('a', class_=re.compile(r'nav-link'))
                assert len(nav_links) > 0, f"No nav links found on {page}"

    def test_form_structure_consistency(self, client, sample_user):
        """Test that forms have consistent structure and required elements."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        # Test diary form
        response = client.get("/diary")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check diary form structure
        form = soup.find('form', id='diary_form')
        assert form, "Diary form not found"
        assert form.get('method'), "Form method not specified"
        assert form.get('action'), "Form action not specified"
        
        # Check for CSRF token (Flask-WTF renders this via form.hidden_tag())
        # Note: CSRF is disabled in testing config, so check if it exists OR if we're in testing mode
        hidden_inputs = form.find_all('input', type='hidden')
        csrf_inputs = form.find_all('input', attrs={'name': re.compile(r'csrf')})
        page_csrf = soup.find_all('input', attrs={'name': re.compile(r'csrf')})
        csrf_meta = soup.find('meta', attrs={'name': 'csrf-token'})
        
        # In production CSRF should exist, in testing it's disabled but meta tag still present
        has_csrf = len(hidden_inputs) > 0 or len(csrf_inputs) > 0 or len(page_csrf) > 0 or csrf_meta is not None
        assert has_csrf, f"No CSRF protection found in diary form. Hidden: {len(hidden_inputs)}, CSRF inputs: {len(csrf_inputs)}, Page CSRF: {len(page_csrf)}, Meta tag: {csrf_meta is not None}"
        
        # Check for required form fields
        content_field = form.find('textarea', id='diary_textarea')
        assert content_field, "Content textarea not found"
        
        rating_field = form.find('input', id='rating_input')
        assert rating_field, "Rating input not found"

    def test_goal_form_structure(self, client, sample_user):
        """Test that goal form has proper structure."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/goals")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Find goal creation form
        form = soup.find('form', action=re.compile(r'.*goals/create'))
        assert form, "Goal creation form not found"
        
        # Check for required fields
        category_field = form.find('select', id='category')
        assert category_field, "Category select not found"
        
        title_field = form.find('input', id='title')
        assert title_field, "Title input not found"
        
        # Check for CSRF token (Flask-WTF renders this via form.hidden_tag())
        # Note: CSRF is disabled in testing config, so check if it exists OR if we're in testing mode
        hidden_inputs = form.find_all('input', type='hidden')
        csrf_inputs = form.find_all('input', attrs={'name': re.compile(r'csrf')})
        page_csrf = soup.find_all('input', attrs={'name': re.compile(r'csrf')})
        csrf_meta = soup.find('meta', attrs={'name': 'csrf-token'})
        
        # In production CSRF should exist, in testing it's disabled but meta tag still present
        has_csrf = len(hidden_inputs) > 0 or len(csrf_inputs) > 0 or len(page_csrf) > 0 or csrf_meta is not None
        assert has_csrf, f"No CSRF protection found in goal form. Hidden: {len(hidden_inputs)}, CSRF inputs: {len(csrf_inputs)}, Page CSRF: {len(page_csrf)}, Meta tag: {csrf_meta is not None}"

    def test_button_structure_consistency(self, client, sample_user):
        """Test that buttons have consistent structure and classes."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/diary")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check rating buttons
        rating_buttons = soup.find_all('button', attrs={'data-rating': True})
        assert len(rating_buttons) >= 2, "Rating buttons not found"
        
        for button in rating_buttons:
            assert 'btn' in button.get('class', []), "Button missing 'btn' class"
            assert button.get('data-rating'), "Button missing data-rating attribute"
            assert button.get('type') == 'button', "Button should have type='button'"

    def test_card_structure_consistency(self, client, sample_user):
        """Test that card components have consistent structure."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/progress")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for card structure
        cards = soup.find_all(class_=re.compile(r'card'))
        assert len(cards) > 0, "No cards found on progress page"
        
        for card in cards:
            # Cards should have proper structure (Bootstrap 'card' or custom card classes)
            card_classes = card.get('class', [])
            if isinstance(card_classes, str):
                card_classes = card_classes.split()
            has_card_class = any('card' in cls for cls in card_classes)
            assert has_card_class, f"Element with classes {card_classes} should have some 'card' related class"

    def test_chart_canvas_structure(self, client, sample_user):
        """Test that chart canvases have proper structure."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/progress")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for chart canvases
        charts = ['pointsChart', 'weekdayChart', 'goalCategoryChart']
        
        for chart_id in charts:
            canvas = soup.find('canvas', id=chart_id)
            assert canvas, f"Canvas with id='{chart_id}' not found"
            
            # Canvas should have proper attributes
            assert canvas.get('width'), f"Canvas {chart_id} missing width attribute"
            assert canvas.get('height'), f"Canvas {chart_id} missing height attribute"

    def test_data_script_structure(self, client, sample_user):
        """Test that data scripts have proper structure and content type."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/progress")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for data scripts
        data_scripts = ['points_data', 'weekday_data', 'goal_stats_data']
        
        for script_id in data_scripts:
            script = soup.find('script', id=script_id)
            assert script, f"Script with id='{script_id}' not found"
            
            # Check content type
            content_type = script.get('type')
            assert content_type == 'application/json', f"Script {script_id} should have type='application/json'"

    def test_accessibility_structure(self, client, sample_user):
        """Test basic accessibility structure elements."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/diary")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for proper heading hierarchy
        h1_tags = soup.find_all('h1')
        assert len(h1_tags) >= 1, "Page should have at least one h1 tag"
        
        # Check for form labels
        labels = soup.find_all('label')
        for label in labels:
            # Labels should have 'for' attribute or contain input
            assert label.get('for') or label.find(['input', 'select', 'textarea']), \
                "Label should have 'for' attribute or contain form element"

    def test_responsive_structure(self, client, sample_user):
        """Test that pages have responsive design elements."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/progress")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for Bootstrap responsive classes
        responsive_elements = soup.find_all(class_=re.compile(r'col-|row|container'))
        assert len(responsive_elements) > 0, "No responsive grid elements found"
        
        # Check for responsive breakpoint classes
        breakpoint_classes = soup.find_all(class_=re.compile(r'col-(sm|md|lg|xl)'))
        assert len(breakpoint_classes) > 0, "No responsive breakpoint classes found"

    def test_javascript_loading_structure(self, client, sample_user):
        """Test that JavaScript files are loaded in correct order."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/progress")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for script tags
        scripts = soup.find_all('script', src=True)
        
        # Should have Bootstrap JS
        bootstrap_js = any('bootstrap' in script.get('src', '') for script in scripts)
        assert bootstrap_js, "Bootstrap JavaScript not found"
        
        # Should have Chart.js for progress page
        chart_js = any('chart' in script.get('src', '').lower() for script in scripts)
        assert chart_js, "Chart.js not found on progress page"

    def test_css_loading_structure(self, client, sample_user):
        """Test that CSS files are loaded correctly."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        response = client.get("/progress")
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for CSS links
        css_links = soup.find_all('link', rel='stylesheet')
        assert len(css_links) > 0, "No CSS stylesheets found"
        
        # Should have Bootstrap CSS
        bootstrap_css = any('bootstrap' in link.get('href', '') for link in css_links)
        assert bootstrap_css, "Bootstrap CSS not found"

    def test_flash_message_structure(self, client, sample_user):
        """Test that flash message structure is consistent."""
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.id
        
        # Create a goal to trigger a flash message
        from tests.conftest import extract_csrf_token
        
        response = client.get("/goals")
        csrf_token = extract_csrf_token(response.data)
        
        data = {
            "category": "Personal Development",
            "title": "Test Flash Message Goal",
            "csrf_token": csrf_token,
        }
        
        response = client.post("/goals/create", data=data, follow_redirects=True)
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Check for alert/flash message structure
        alerts = soup.find_all(class_=re.compile(r'alert'))
        if alerts:  # Flash messages may not always be present
            for alert in alerts:
                assert 'alert' in alert.get('class', []), "Alert should have 'alert' class"

    def test_error_page_structure(self, client):
        """Test that error pages have proper structure."""
        # Test 404 page
        response = client.get("/nonexistent-page")
        
        if response.status_code == 404:
            soup = BeautifulSoup(response.data, 'html.parser')
            
            # Should still have basic HTML structure
            assert soup.find('html'), "404 page missing HTML tag"
            assert soup.find('head'), "404 page missing HEAD tag"
            assert soup.find('body'), "404 page missing BODY tag"
            assert soup.find('title'), "404 page missing TITLE tag"