from .database import db

class DailyStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)

    points = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)

    user = db.relationship('User', backref='daily_stats')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'date', name='user_date_uc'),
    )