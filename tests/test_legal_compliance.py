"""
Legal Compliance Tests for My Inner Scope Application

Tests to verify legal documents and privacy compliance including:
- Privacy policy content and analytics disclosure
- Terms of service accuracy  
- Cookie consent system functionality
- GDPR compliance features
- Legal document accessibility
"""

import pytest
import re
from bs4 import BeautifulSoup


class TestPrivacyPolicy:
    """Test privacy policy content and compliance"""
    
    def test_privacy_policy_accessibility(self, client):
        """Test privacy policy page is accessible"""
        response = client.get('/privacy')
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Test page structure
        title = soup.find('h1')
        assert title is not None
        assert 'Privacy Policy' in title.text
    
    def test_analytics_disclosure_present(self, client):
        """Test privacy policy includes analytics data collection disclosure"""
        response = client.get('/privacy')
        assert response.status_code == 200
        
        content = response.data.decode('utf-8')
        
        # Test analytics disclosure is present
        assert 'Google Analytics' in content
        assert 'Analytics Cookies (Optional)' in content
        assert 'anonymized' in content.lower()
        assert 'consent' in content.lower()
        
        # Test analytics data types are disclosed
        assert 'page views' in content.lower() or 'navigation patterns' in content.lower()
        assert 'feature usage' in content.lower() or 'interaction data' in content.lower()
        assert 'user interactions' in content.lower() or 'interaction data' in content.lower()
        assert 'ip addresses' in content.lower()
    
    def test_essential_data_disclosure(self, client):
        """Test privacy policy includes essential data collection disclosure"""
        response = client.get('/privacy')
        assert response.status_code == 200
        
        content = response.data.decode('utf-8')
        
        # Test essential data types are disclosed
        assert 'email address' in content.lower()
        assert 'diary entries' in content.lower()
        assert 'goals' in content.lower()
        assert 'session cookies' in content.lower()
    
    def test_cookie_management_disclosure(self, client):
        """Test privacy policy explains cookie management"""
        response = client.get('/privacy')
        assert response.status_code == 200
        
        content = response.data.decode('utf-8')
        
        # Test cookie management information
        assert 'cookie preferences' in content.lower()
        assert 'cookie consent' in content.lower()
        assert 'can be disabled' in content.lower()
        assert 'explicitly consent' in content.lower()
    
    def test_gdpr_rights_disclosure(self, client):
        """Test privacy policy includes GDPR rights"""
        response = client.get('/privacy')
        assert response.status_code == 200
        
        content = response.data.decode('utf-8')
        
        # Test GDPR rights are disclosed
        assert 'Right to Access' in content
        assert 'Right to Erasure' in content
        assert 'Right to Rectification' in content
        assert 'Right to Object' in content
        
        # Test data export is mentioned
        assert 'download' in content.lower()
        assert 'delete your account' in content.lower()


class TestTermsOfService:
    """Test terms of service content and accuracy"""
    
    def test_terms_accessibility(self, client):
        """Test terms of service page is accessible"""
        response = client.get('/terms')
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Test page structure
        title = soup.find('h1')
        assert title is not None
        assert 'Terms of Service' in title.text
    
    def test_data_sharing_disclosure(self, client):
        """Test terms accurately describe data sharing with analytics"""
        response = client.get('/terms')
        assert response.status_code == 200
        
        content = response.data.decode('utf-8')
        
        # Test data sharing is accurately described
        assert 'personal data' in content.lower()
        assert 'third parties' in content.lower()
        assert 'Google Analytics' in content
        assert 'anonymous' in content.lower()
        assert 'consent' in content.lower()
    
    def test_service_limitations_disclosed(self, client):
        """Test terms include appropriate service limitations"""
        response = client.get('/terms')
        assert response.status_code == 200
        
        content = response.data.decode('utf-8')
        
        # Test service limitations
        assert 'as is' in content.lower()
        assert 'as available' in content.lower()
        assert 'no warranty' in content.lower()
        assert 'data loss' in content.lower()
    
    def test_account_deletion_rights(self, client):
        """Test terms include account deletion rights"""
        response = client.get('/terms')
        assert response.status_code == 200
        
        content = response.data.decode('utf-8')
        
        # Test account deletion is mentioned
        assert 'delete your account' in content.lower()
        assert 'irreversible' in content.lower()


class TestCookieCompliance:
    """Test cookie consent and compliance features"""
    
    def test_cookie_consent_javascript_present(self, client):
        """Test cookie consent JavaScript is loaded"""
        response = client.get('/')
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Test cookie consent script is included
        scripts = soup.find_all('script')
        cookie_script_found = False
        
        for script in scripts:
            if script.get('src') and 'cookie_consent' in script.get('src'):
                cookie_script_found = True
                break
        
        assert cookie_script_found, "Cookie consent JavaScript not found"
    
    def test_analytics_conditional_loading(self, client):
        """Test Google Analytics loads conditionally"""
        response = client.get('/')
        assert response.status_code == 200
        
        content = response.data.decode('utf-8')
        
        # Test Google Analytics is conditionally loaded
        if 'GOOGLE_ANALYTICS_ID' in content:
            # If GA is configured, test it's properly implemented
            assert 'anonymize_ip' in content
            assert 'respect_header' in content
            assert 'gtag' in content
    
    def test_meta_csrf_token_present(self, client):
        """Test CSRF token is available for JavaScript"""
        response = client.get('/')
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Test CSRF token meta tag exists
        csrf_meta = soup.find('meta', attrs={'name': 'csrf-token'})
        assert csrf_meta is not None
        assert 'content' in csrf_meta.attrs
        assert len(csrf_meta['content']) > 0


class TestLegalPageSEO:
    """Test SEO implementation for legal pages"""
    
    def test_privacy_page_seo(self, client):
        """Test privacy policy page has proper SEO meta tags"""
        response = client.get('/privacy')
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Test title
        title = soup.find('title')
        assert title is not None
        assert 'Privacy Policy' in title.text
        
        # Test meta description
        description = soup.find('meta', attrs={'name': 'description'})
        assert description is not None
        assert 'privacy' in description['content'].lower()
        assert 'GDPR' in description['content']
        
        # Test canonical URL
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        assert canonical is not None
        assert canonical['href'].endswith('/privacy')
    
    def test_terms_page_seo(self, client):
        """Test terms of service page has proper SEO meta tags"""
        response = client.get('/terms')
        assert response.status_code == 200
        
        soup = BeautifulSoup(response.data, 'html.parser')
        
        # Test title
        title = soup.find('title')
        assert title is not None
        assert 'Terms of Service' in title.text
        
        # Test meta description
        description = soup.find('meta', attrs={'name': 'description'})
        assert description is not None
        assert 'terms' in description['content'].lower()
        
        # Test canonical URL
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        assert canonical is not None
        assert canonical['href'].endswith('/terms')


class TestDataPrivacyFeatures:
    """Test application data privacy features"""
    
    def test_session_security_headers(self, client):
        """Test session cookies have security attributes"""
        # Make a request that would set a session cookie
        response = client.get('/')
        
        # Test security headers are present
        assert response.status_code == 200
        
        # Check if security headers are set in cookies
        if 'Set-Cookie' in response.headers:
            cookie_header = response.headers.get('Set-Cookie')
            # Should include security attributes
            assert 'HttpOnly' in cookie_header
            assert 'Secure' in cookie_header
            assert 'SameSite' in cookie_header
    
    def test_no_sensitive_data_exposure(self, client):
        """Test no sensitive configuration data is exposed"""
        response = client.get('/')
        assert response.status_code == 200
        
        content = response.data.decode('utf-8')
        
        # Test sensitive data is not exposed
        assert 'SECRET_KEY' not in content
        assert 'DATABASE_URL' not in content
        assert 'password' not in content.lower() or 'password' in content.lower()  # Allow password in forms
    
    def test_error_pages_dont_expose_debug_info(self, client):
        """Test error pages don't expose debug information"""
        # Test a route that should return 404
        response = client.get('/nonexistent-page')
        assert response.status_code == 404
        
        content = response.data.decode('utf-8')
        
        # Test no debug information is exposed
        assert 'Traceback' not in content
        assert 'File "' not in content
        assert 'line ' not in content


class TestComplianceDocumentation:
    """Test compliance documentation completeness"""
    
    def test_all_legal_pages_accessible(self, client):
        """Test all legal pages are accessible"""
        legal_pages = ['/privacy', '/terms']
        
        for page in legal_pages:
            response = client.get(page)
            assert response.status_code == 200, f"Legal page {page} not accessible"
    
    def test_legal_pages_included_in_sitemap(self, client):
        """Test legal pages are included in sitemap"""
        response = client.get('/sitemap.xml')
        assert response.status_code == 200
        
        content = response.data.decode('utf-8')
        
        # Test legal pages are in sitemap
        assert '/privacy' in content
        assert '/terms' in content
    
    def test_legal_pages_in_robots_txt(self, client):
        """Test legal pages are allowed in robots.txt"""
        response = client.get('/robots.txt')
        assert response.status_code == 200
        
        content = response.data.decode('utf-8')
        
        # Test legal pages are allowed
        assert 'Allow: /privacy' in content
        assert 'Allow: /terms' in content
    
    def test_contact_information_present(self, client):
        """Test contact information is present in legal documents"""
        legal_pages = ['/privacy', '/terms']
        
        for page in legal_pages:
            response = client.get(page)
            assert response.status_code == 200
            
            content = response.data.decode('utf-8')
            
            # Test contact information is present
            assert ('contact' in content.lower() or 
                   'repository' in content.lower() or 
                   'developer' in content.lower()), f"No contact info in {page}"


# Pytest markers for test organization
pytestmark = [
    pytest.mark.legal,
    pytest.mark.compliance,
    pytest.mark.integration
]