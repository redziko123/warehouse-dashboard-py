from datetime import datetime

from models._db import db


class NewsItem(db.Model):
    __tablename__ = 'news'

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date        = db.Column(db.DateTime, default=datetime.utcnow)
    image_url   = db.Column(db.String(500), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date': self.date.isoformat(),
            'image_url': self.image_url,
        }


class TipItem(db.Model):
    __tablename__ = 'tips'

    id           = db.Column(db.Integer, primary_key=True)
    text         = db.Column(db.Text, nullable=False)
    date         = db.Column(db.DateTime, default=datetime.utcnow)
    is_important = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'date': self.date.isoformat(),
            'is_important': self.is_important,
        }


class WarningItem(db.Model):
    __tablename__ = 'warnings'

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date        = db.Column(db.DateTime, default=datetime.utcnow)
    image_url   = db.Column(db.String(500), default='')
    is_active   = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date': self.date.isoformat(),
            'image_url': self.image_url,
            'is_active': self.is_active,
        }


class Lesson(db.Model):
    __tablename__ = 'lessons'

    id               = db.Column(db.Integer, primary_key=True)
    title            = db.Column(db.String(255), nullable=False)
    description      = db.Column(db.Text, nullable=False)
    content          = db.Column(db.Text, default='')
    image_url        = db.Column(db.String(500), nullable=True)
    category         = db.Column(db.String(100), default='General')
    duration_minutes = db.Column(db.Integer, default=5)
    icon_name        = db.Column(db.String(50), default='article')
    is_featured      = db.Column(db.Boolean, default=False)
    order            = db.Column(db.Integer, default=0)
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'content': self.content,
            'image_url': self.image_url,
            'category': self.category,
            'duration_minutes': self.duration_minutes,
            'icon_name': self.icon_name,
            'is_featured': self.is_featured,
            'order': self.order,
        }
