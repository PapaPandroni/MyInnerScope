from typing import Optional
from .database import db
from datetime import datetime, timezone, date
import enum


class PointsSourceType(enum.Enum):
    DIARY_ENTRY = "diary_entry"
    GOAL_COMPLETED = "goal_completed"
    GOAL_FAILED = "goal_failed"
    DAILY_LOGIN = "daily_login"
    STREAK_7_DAY = "streak_7_day"
    STREAK_30_DAY = "streak_30_day"


class PointsLog(db.Model):
    """Log of all point-earning activities for detailed tracking and breakdowns."""

    __tablename__ = "points_log"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Point transaction details
    date = db.Column(db.Date, nullable=False)
    points = db.Column(db.Integer, nullable=False)

    # Source tracking
    source_type = db.Column(db.String(20), nullable=False)
    source_id = db.Column(
        db.Integer, nullable=True
    )  # diary_entry.id or goal.id (null for login)
    description = db.Column(db.Text, nullable=False)  # Human-readable description

    # Timestamp
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = db.relationship("User", backref="points_log")

    def __repr__(self) -> str:
        return f"<PointsLog {self.user_id}: {self.points}pts from {self.source_type.value} on {self.date}>"

    @staticmethod
    def create_entry(
        user_id: int,
        points: int,
        source_type: PointsSourceType,
        description: str,
        date: Optional[date] = None,
        source_id: Optional[int] = None,
    ) -> "PointsLog":
        """Create a new points log entry.

        Args:
            user_id: User who earned the points
            points: Number of points earned
            source_type: Type of activity that earned points
            description: Human-readable description of the activity
            date: Date the points were earned (defaults to today)
            source_id: Optional ID of the source object (diary entry, goal, etc.)

        Returns:
            The created PointsLog entry
        """
        if date is None:
            date = datetime.now(timezone.utc).date()

        log_entry = PointsLog(
            user_id=user_id,
            date=date,
            points=points,
            source_type=(
                source_type.value
                if isinstance(source_type, PointsSourceType)
                else source_type
            ),
            source_id=source_id,
            description=description,
        )

        db.session.add(log_entry)
        return log_entry

    @staticmethod
    def get_daily_breakdown(
        user_id: int, target_date: Optional[date] = None
    ) -> list["PointsLog"]:
        """Get all point-earning activities for a specific day.

        Args:
            user_id: User to get breakdown for
            target_date: Date to get breakdown for (defaults to today)

        Returns:
            List of PointsLog entries for the specified date
        """
        if target_date is None:
            target_date = datetime.now(timezone.utc).date()

        return (
            PointsLog.query.filter_by(user_id=user_id, date=target_date)
            .order_by(PointsLog.created_at.desc())
            .all()
        )

    @staticmethod
    def get_daily_total(user_id: int, target_date: Optional[date] = None) -> int:
        """Get total points earned on a specific day.

        Args:
            user_id: User to get total for
            target_date: Date to get total for (defaults to today)

        Returns:
            Total points earned on the specified date
        """
        if target_date is None:
            target_date = datetime.now(timezone.utc).date()

        result = (
            db.session.query(db.func.sum(PointsLog.points))
            .filter_by(user_id=user_id, date=target_date)
            .scalar()
        )

        return result or 0
