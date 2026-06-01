from datetime import datetime

from models._db import db


class WeeklyStats(db.Model):
    __tablename__ = 'weekly_stats'

    id              = db.Column(db.Integer, primary_key=True)
    year            = db.Column(db.Integer, nullable=False, default=datetime.utcnow().year)
    week            = db.Column(db.Integer, nullable=False)   # 1–52
    loaded_trucks   = db.Column(db.Integer, default=0)
    unloaded_trucks = db.Column(db.Integer, default=0)
    errors          = db.Column(db.Integer, default=0)

    __table_args__ = (
        db.UniqueConstraint('year', 'week', name='uq_year_week'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'year': self.year,
            'week': self.week,
            'loaded_trucks': self.loaded_trucks,
            'unloaded_trucks': self.unloaded_trucks,
            'errors': self.errors,
        }
