"""
Main routes for the application.
"""

from typing import Union, Tuple
from flask import Blueprint, render_template, current_app, Response, url_for
from datetime import datetime

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def hello() -> str:
    return render_template("main/index.html")


@main_bp.route("/about")
def about() -> str:
    return render_template("main/about.html")


@main_bp.route("/faq")
def faq() -> str:
    return render_template("main/faq.html")


@main_bp.route("/robots.txt")
def robots_txt() -> Response:
    """Serve robots.txt file for search engine crawlers."""
    robots_content = """User-agent: *
Allow: /
Allow: /about
Allow: /privacy
Allow: /terms
Allow: /donate
Allow: /register
Allow: /login

# Disallow private/authenticated areas
Disallow: /diary
Disallow: /progress
Disallow: /goals
Disallow: /profile
Disallow: /settings
Disallow: /read-diary
Disallow: /api/

# Sitemap location
Sitemap: {sitemap_url}

# Crawl delay to be respectful
Crawl-delay: 1
""".format(sitemap_url=url_for('main.sitemap_xml', _external=True))
    
    return Response(robots_content, mimetype='text/plain')


@main_bp.route("/sitemap.xml")
def sitemap_xml() -> Response:
    """Generate XML sitemap for search engines."""
    # Get current date for lastmod
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Define static pages with their priorities and change frequencies
    static_pages = [
        {
            'url': url_for('main.hello', _external=True),
            'lastmod': current_date,
            'changefreq': 'weekly',
            'priority': '1.0'
        },
        {
            'url': url_for('main.about', _external=True),
            'lastmod': current_date,
            'changefreq': 'monthly',
            'priority': '0.8'
        },
        {
            'url': url_for('main.faq', _external=True),
            'lastmod': current_date,
            'changefreq': 'monthly',
            'priority': '0.7'
        },
        {
            'url': url_for('legal.privacy', _external=True),
            'lastmod': current_date,
            'changefreq': 'yearly',
            'priority': '0.5'
        },
        {
            'url': url_for('legal.terms', _external=True),
            'lastmod': current_date,
            'changefreq': 'yearly',
            'priority': '0.5'
        },
        {
            'url': url_for('legal.donate', _external=True),
            'lastmod': current_date,
            'changefreq': 'monthly',
            'priority': '0.6'
        },
        {
            'url': url_for('auth.register', _external=True),
            'lastmod': current_date,
            'changefreq': 'monthly',
            'priority': '0.7'
        },
        {
            'url': url_for('auth.login_page', _external=True),
            'lastmod': current_date,
            'changefreq': 'monthly',
            'priority': '0.7'
        }
    ]
    
    # Generate XML sitemap
    sitemap_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''
    
    for page in static_pages:
        sitemap_xml += f'''    <url>
        <loc>{page['url']}</loc>
        <lastmod>{page['lastmod']}</lastmod>
        <changefreq>{page['changefreq']}</changefreq>
        <priority>{page['priority']}</priority>
    </url>
'''
    
    sitemap_xml += '</urlset>'
    
    return Response(sitemap_xml, mimetype='application/xml')


@main_bp.app_errorhandler(404)
def page_not_found(e) -> Tuple[str, int]:
    return render_template("errors/404.html"), 404


@main_bp.app_errorhandler(403)
def forbidden(e) -> Tuple[str, int]:
    return render_template("errors/403.html"), 403


@main_bp.app_errorhandler(500)
def internal_server_error(e) -> Tuple[str, int]:
    current_app.logger.error(f"Internal Server Error: {e}", exc_info=True)
    return render_template("errors/500.html"), 500
