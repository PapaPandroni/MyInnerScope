document.addEventListener('DOMContentLoaded', function() {
    // Check if user has already provided consent
    const hasEssentialConsent = document.cookie.includes('cookie_consent=true');
    const hasAnalyticsConsent = document.cookie.includes('analytics_consent=true');
    
    if (!hasEssentialConsent) {
        showCookieConsentBanner();
    }
    
    // If analytics is configured but user hasn't consented, disable tracking
    if (window.gtag && !hasAnalyticsConsent) {
        window.gtag('consent', 'default', {
            'analytics_storage': 'denied',
            'ad_storage': 'denied'
        });
    }
    
    function showCookieConsentBanner() {
        const banner = document.createElement('div');
        banner.className = 'cookie-consent-banner bg-dark text-white p-3 fixed-bottom shadow-lg';
        banner.style.zIndex = '9999';
        banner.innerHTML = `
            <div class="container">
                <div class="row align-items-center">
                    <div class="col-md-8">
                        <h5 class="mb-2">Cookie Consent</h5>
                        <p class="mb-0 small">
                            We use essential cookies for login and security. 
                            Optional analytics cookies help us improve the app. 
                            <a href="/privacy" class="link-light">Learn more</a>
                        </p>
                    </div>
                    <div class="col-md-4 text-end mt-2 mt-md-0">
                        <button class="btn btn-outline-light btn-sm me-2" id="manageCookies">Manage</button>
                        <button class="btn btn-success btn-sm me-2" id="acceptAll">Accept All</button>
                        <button class="btn btn-light btn-sm" id="acceptEssential">Essential Only</button>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(banner);
        
        // Event handlers
        document.getElementById('acceptAll').onclick = function() {
            setConsent(true, true);
            banner.remove();
        };
        
        document.getElementById('acceptEssential').onclick = function() {
            setConsent(true, false);
            banner.remove();
        };
        
        document.getElementById('manageCookies').onclick = function() {
            showCookiePreferences();
        };
    }
    
    function showCookiePreferences() {
        const modal = document.createElement('div');
        modal.className = 'modal fade show';
        modal.style.display = 'block';
        modal.style.zIndex = '10000';
        modal.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content bg-dark text-white">
                    <div class="modal-header">
                        <h5 class="modal-title">Cookie Preferences</h5>
                        <button type="button" class="btn-close btn-close-white" id="closeCookieModal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-4">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="essentialCookies" checked disabled>
                                <label class="form-check-label" for="essentialCookies">
                                    <strong>Essential Cookies</strong> (Required)
                                </label>
                                <small class="form-text text-muted d-block">
                                    These cookies are necessary for login, security, and basic functionality. They cannot be disabled.
                                </small>
                            </div>
                        </div>
                        <div class="mb-4">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="analyticsCookies" ${hasAnalyticsConsent ? 'checked' : ''}>
                                <label class="form-check-label" for="analyticsCookies">
                                    <strong>Analytics Cookies</strong> (Optional)
                                </label>
                                <small class="form-text text-muted d-block">
                                    These cookies help us understand how you use the app so we can improve it. All data is anonymized.
                                </small>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" id="closeCookieModal">Cancel</button>
                        <button type="button" class="btn btn-primary" id="savePreferences">Save Preferences</button>
                    </div>
                </div>
            </div>
        `;
        
        // Add backdrop
        const backdrop = document.createElement('div');
        backdrop.className = 'modal-backdrop fade show';
        backdrop.style.zIndex = '9999';
        document.body.appendChild(backdrop);
        document.body.appendChild(modal);
        
        // Event handlers
        document.getElementById('closeCookieModal').onclick = function() {
            modal.remove();
            backdrop.remove();
        };
        
        document.getElementById('savePreferences').onclick = function() {
            const analyticsEnabled = document.getElementById('analyticsCookies').checked;
            setConsent(true, analyticsEnabled);
            modal.remove();
            backdrop.remove();
            
            // Remove banner if it exists
            const banner = document.querySelector('.cookie-consent-banner');
            if (banner) banner.remove();
        };
    }
    
    function setConsent(essential, analytics) {
        // Set essential cookies consent
        document.cookie = 'cookie_consent=true; path=/; max-age=31536000; SameSite=Lax';
        
        // Set analytics consent
        if (analytics) {
            document.cookie = 'analytics_consent=true; path=/; max-age=31536000; SameSite=Lax';
            
            // Enable Google Analytics if configured
            if (window.gtag) {
                window.gtag('consent', 'update', {
                    'analytics_storage': 'granted'
                });
            }
        } else {
            document.cookie = 'analytics_consent=false; path=/; max-age=31536000; SameSite=Lax';
            
            // Disable Google Analytics
            if (window.gtag) {
                window.gtag('consent', 'update', {
                    'analytics_storage': 'denied'
                });
            }
        }
    }
    
    // Expose function to allow users to change preferences later
    window.showCookiePreferences = showCookiePreferences;
}); 