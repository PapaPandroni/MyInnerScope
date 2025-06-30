document.addEventListener('DOMContentLoaded', function() {
    if (!document.cookie.includes('cookie_consent=true')) {
        var banner = document.createElement('div');
        banner.className = 'cookie-consent-banner bg-dark text-white p-3 fixed-bottom text-center';
        banner.innerHTML = `
            <span>This site uses essential cookies for login and security. <a href="/privacy" class="link-light">Learn more</a>.</span>
            <button class="btn btn-primary btn-sm ms-3" id="acceptCookies">Accept</button>
        `;
        document.body.appendChild(banner);
        document.getElementById('acceptCookies').onclick = function() {
            document.cookie = 'cookie_consent=true; path=/; max-age=31536000';
            banner.remove();
        };
    }
}); 