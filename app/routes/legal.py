from flask import Blueprint, render_template

legal_bp = Blueprint("legal", __name__)


@legal_bp.route("/privacy")
def privacy() -> str:
    return render_template("legal/privacy.html")


@legal_bp.route("/terms")
def terms() -> str:
    return render_template("legal/terms.html")


@legal_bp.route("/donate")
def donate() -> str:
    return render_template("main/donate.html")
