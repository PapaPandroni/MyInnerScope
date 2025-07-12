from typing import Tuple
from .database import db
from datetime import datetime, timedelta, timezone, date
import enum


class GoalCategory(enum.Enum):
    EXERCISE = "Exercise & Fitness"
    LEARNING = "Learning & Reading"
    MINDFULNESS = "Mindfulness & Mental Health"
    SOCIAL = "Social Connections"
    PRODUCTIVITY = "Productivity & Work"
    PERSONAL_DEV = "Personal Development"
    HOME = "Home & Organization"
    CREATIVE = "Creative Pursuits"
    CUSTOM = "Custom Goal"


class GoalStatus(enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"


class Goal(db.Model):
    __tablename__ = "goals"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Goal details
    category = db.Column(db.Enum(GoalCategory), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Time tracking
    week_start = db.Column(db.Date, nullable=False)  # Start date (date of creation)
    week_end = db.Column(db.Date, nullable=False)  # End date (6 days after creation)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Progress tracking
    status = db.Column(db.Enum(GoalStatus), default=GoalStatus.ACTIVE)
    progress_notes = db.Column(db.Text, nullable=True)

    # Relationships
    user = db.relationship("User", backref="goals")

    def __repr__(self) -> str:
        return f"<Goal {self.title} - {self.status.value}>"

    @property
    def is_current(self) -> bool:
        """Check if this goal is still active (today between start and end)"""
        today = datetime.now(timezone.utc).date()
        return (
            self.week_start <= today <= self.week_end
            and self.status == GoalStatus.ACTIVE
        )

    @property
    def days_remaining(self) -> int:
        today = datetime.now(timezone.utc).date()
        if today > self.week_end:
            return 0
        return (self.week_end - today).days

    @property
    def progress_percentage(self) -> float:
        total_days = (self.week_end - self.week_start).days + 1
        days_passed = (datetime.now(timezone.utc).date() - self.week_start).days + 1
        return min(100, max(0, (days_passed / total_days) * 100))

    @staticmethod
    def get_goal_dates(target_date: date = None) -> Tuple[date, date]:
        """Get the start and end date for a new goal (start = today, end = today+6)"""
        if target_date is None:
            target_date = datetime.now(timezone.utc).date()
        start = target_date
        end = start + timedelta(days=6)
        return start, end
