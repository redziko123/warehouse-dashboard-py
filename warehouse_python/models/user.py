from datetime import datetime, date

import bcrypt
from flask_login import UserMixin

from models._db import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    email         = db.Column(db.String(255), unique=True, nullable=False)
    username      = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role          = db.Column(db.String(20), default='user')   # 'admin' | 'user'
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password: str):
        self.password_hash = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()
        ).decode()

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())

    @property
    def is_admin(self) -> bool:
        return self.role == 'admin'

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'role': self.role,
        }


class Employee(db.Model):
    __tablename__ = 'employees'

    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(200), nullable=False)
    birthday = db.Column(db.Date, nullable=False)

    def days_until_birthday(self, today: date | None = None) -> int:
        today = today or date.today()
        this_year = date(today.year, self.birthday.month, self.birthday.day)
        if this_year >= today:
            return (this_year - today).days
        next_year = date(today.year + 1, self.birthday.month, self.birthday.day)
        return (next_year - today).days

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'birthday': self.birthday.isoformat(),
            'days_until': self.days_until_birthday(),
        }
