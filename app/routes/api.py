from flask import Blueprint, jsonify, session
from datetime import date
from ..models import DailyStats, DiaryEntry, Goal
from ..utils.points_service import PointsService

api_bp = Blueprint("api", __name__)

@api_bp.route("/api/points-breakdown")
def points_breakdown():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session["user_id"]
    
    # Get detailed breakdown from PointsLog
    breakdown = PointsService.get_daily_breakdown(user_id)
    
    return jsonify(breakdown)
