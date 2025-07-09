"""
Main routes for the application.
"""

from typing import Union, Tuple
from flask import Blueprint, render_template, current_app

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def hello() -> str:
    return render_template("index.html")


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
