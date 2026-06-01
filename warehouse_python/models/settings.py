from models._db import db


class BackgroundSettings(db.Model):
    __tablename__ = 'background_settings'

    id                   = db.Column(db.Integer, primary_key=True)
    home_background_url  = db.Column(db.String(500), default='')
    login_background_url = db.Column(db.String(500), default='')


    def to_dict(self):
        return {
            'home_background_url': self.home_background_url,
            'login_background_url': self.login_background_url,
        }
