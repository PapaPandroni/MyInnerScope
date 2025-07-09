from datetime import date
from .database import db


class DiaryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    entry_date = db.Column(db.Date, default=date.today, nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", backref="entries")
