"""
SEO Integration Summary Tests for My Inner Scope Application

Comprehensive tests covering the most critical SEO and legal compliance elements.
These tests validate the core functionality without being too strict on exact wording.
"""

import pytest
import json
import re
from bs4 import BeautifulSoup


class TestCriticalSEOElements:
    """Test the most critical SEO elements are present and functional"""
    
    def test_homepage_has_complete_seo(self, client):
        """Test homepage has all critical SEO elements"""
        response = client.get('/')
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Critical elements must be present
        assert soup.find('title') is not None
        assert soup.find('meta', attrs={'name': 'description'}) is not None
        assert soup.find('link', attrs={'rel': 'canonical'}) is not None
        assert soup.find('meta', attrs={'property': 'og:title'}) is not None
        assert soup.find('meta', attrs={'property': 'og:image'}) is not None
        assert soup.find('meta', attrs={'name': 'twitter:card'}) is not None
    
    def test_structured_data_present(self, client):
        """Test JSON-LD structured data is present and valid"""
        response = client.get('/')
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        json_ld_scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
        
        assert len(json_ld_scripts) > 0
        
        # At least one should be valid JSON
        valid_json_found = False
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                if '@context' in data and '@type' in data:
                    valid_json_found = True
                    break
            except (json.JSONDecodeError, AttributeError):
                continue
        
        assert valid_json_found, "No valid JSON-LD structured data found"
    
    def test_robots_and_sitemap_functional(self, client):
        """Test robots.txt and sitemap.xml are functional"""
        # Test robots.txt
        robots_response = client.get('/robots.txt')
        assert robots_response.status_code == 200
        assert 'User-agent:' in robots_response.data.decode('utf-8')
        assert 'Sitemap:' in robots_response.data.decode('utf-8')
        
        # Test sitemap.xml
        sitemap_response = client.get('/sitemap.xml')
        assert sitemap_response.status_code == 200
        assert '<?xml' in sitemap_response.data.decode('utf-8')
        assert '<urlset' in sitemap_response.data.decode('utf-8')
    
    def test_favicons_accessible(self, client):
        """Test essential favicon files are accessible"""
        favicon_files = [
            '/static/assets/favicon.ico',
            '/static/assets/favicon.svg',
            '/static/assets/apple-touch-icon.png'
        ]
        
        for favicon in favicon_files:
            response = client.get(favicon)
            assert response.status_code == 200, f"Favicon not accessible: {favicon}"
    
    def test_social_preview_image_accessible(self, client):
        """Test social media preview image is accessible"""
        response = client.get('/static/assets/social-preview.jpg')
        assert response.status_code == 200
        assert 'image' in response.content_type


class TestLegalComplianceCore:
    """Test core legal compliance requirements"""
    
    def test_privacy_policy_has_analytics_disclosure(self, client):
        """Test privacy policy mentions analytics"""
        response = client.get('/privacy')
        assert response.status_code == 200
        
        content = response.data.decode('utf-8').lower()
        
        # Must mention analytics and consent
        assert 'analytics' in content
        assert 'consent' in content
        assert 'cookies' in content
    
    def test_terms_of_service_accessible(self, client):
        """Test terms of service is accessible and mentions data"""
        response = client.get('/terms')
        assert response.status_code == 200
        
        content = response.data.decode('utf-8').lower()
        
        # Must mention basic terms concepts
        assert 'data' in content
        assert 'service' in content
        assert 'account' in content
    
    def test_legal_pages_have_proper_seo(self, client):
        """Test legal pages have basic SEO elements"""
        legal_pages = ['/privacy', '/terms']
        
        for page in legal_pages:
            response = client.get(page)
            assert response.status_code == 200
            
            soup = BeautifulSoup(response.data, 'html.parser')
            
            # Must have title and canonical
            assert soup.find('title') is not None
            canonical = soup.find('link', attrs={'rel': 'canonical'})
            assert canonical is not None
            assert canonical['href'].endswith(page)


class TestAnalyticsInfrastructureCore:
    """Test core analytics infrastructure without requiring actual tracking"""
    
    def test_cookie_consent_infrastructure_present(self, client):
        """Test cookie consent system is properly set up"""
        response = client.get('/')
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # CSRF token for consent AJAX
        csrf_meta = soup.find('meta', attrs={'name': 'csrf-token'})
        assert csrf_meta is not None
        
        # Cookie consent script
        scripts = soup.find_all('script')
        cookie_script_found = any('cookie_consent' in script.get('src', '') for script in scripts)
        assert cookie_script_found, "Cookie consent script not found"
    
    def test_analytics_environment_safety(self, app):
        """Test analytics is safely configured for test environment"""
        with app.app_context():
            # Should not have real analytics ID in test
            analytics_id = app.config.get('GOOGLE_ANALYTICS_ID')
            assert analytics_id is None  # Safe for testing
    
    def test_cookie_consent_script_accessible(self, client):
        """Test cookie consent JavaScript is accessible"""
        response = client.get('/static/js/shared/cookie_consent.js')
        assert response.status_code == 200


class TestSEOTechnicalStructure:
    """Test technical SEO structure"""
    
    def test_meta_viewport_present(self, client):
        """Test viewport meta tag is present for mobile SEO"""
        response = client.get('/')
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        assert viewport is not None
    
    def test_lang_attribute_present(self, client):
        """Test lang attribute is present for accessibility and SEO"""
        response = client.get('/')
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        html_tag = soup.find('html')
        assert html_tag is not None
        # Lang attribute should be present
        assert html_tag.get('lang') is not None
    
    def test_sitemap_includes_key_pages(self, client):
        """Test sitemap includes essential public pages"""
        response = client.get('/sitemap.xml')
        assert response.status_code == 200
        
        content = response.data.decode('utf-8')
        
        # Key pages should be included
        essential_pages = ['/', '/about', '/privacy', '/terms']
        for page in essential_pages:
            assert page in content, f"Essential page missing from sitemap: {page}"


class TestOverallComplianceStatus:
    """High-level compliance validation"""
    
    def test_all_critical_pages_accessible(self, client):
        """Test all critical pages load without errors"""
        critical_pages = [
            '/',           # Homepage
            '/about',      # About page
            '/login',      # Login page
            '/register',   # Registration page
            '/privacy',    # Privacy policy
            '/terms',      # Terms of service
            '/robots.txt', # Robots.txt
            '/sitemap.xml' # Sitemap
        ]
        
        for page in critical_pages:
            response = client.get(page)
            assert response.status_code == 200, f"Critical page failed: {page}"
    
    def test_no_debug_info_exposed(self, client):
        """Test no debug information is exposed in production-like setup"""
        response = client.get('/')
        assert response.status_code == 200
        
        content = response.data.decode('utf-8')
        
        # Should not contain debug information
        debug_indicators = ['SECRET_KEY', 'DATABASE_URL', 'Traceback', 'File "']
        for indicator in debug_indicators:
            assert indicator not in content, f"Debug info exposed: {indicator}"
    
    def test_security_headers_present(self, client):
        """Test basic security headers are present"""
        response = client.get('/')
        assert response.status_code == 200
        
        # Basic security should be in place
        if 'Set-Cookie' in response.headers:
            cookie_header = response.headers.get('Set-Cookie')
            # At least one security attribute should be present
            security_attrs = ['HttpOnly', 'Secure', 'SameSite']
            assert any(attr in cookie_header for attr in security_attrs)


# Simple pytest marks that don't require registration
pytestmark = pytest.mark.integration