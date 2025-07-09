"""
Tests for CSRF protection
"""

import pytest


def test_csrf_token_in_template(client):
    """Test that CSRF token is available in templates"""
    response = client.get("/")
    assert response.status_code == 200
    # Check that CSRF token meta tag is present
    assert b"csrf-token" in response.data
    assert b"content=" in response.data


def test_csrf_token_in_register_page(client):
    """Test that CSRF token is available in register page"""
    response = client.get("/register")
    assert response.status_code == 200
    # Check that CSRF token meta tag is present
    assert b"csrf-token" in response.data
    assert b"content=" in response.data


def test_csrf_token_in_login_page(client):
    """Test that CSRF token is available in login page"""
    response = client.get("/login")
    assert response.status_code == 200
    # Check that CSRF token meta tag is present
    assert b"csrf-token" in response.data
    assert b"content=" in response.data
