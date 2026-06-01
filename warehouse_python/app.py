import os
from datetime import datetime

from flask import Flask, render_template
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from config import Config
from models import db, User, WeeklyStats, BackgroundSettings
from routes.auth  import auth_bp
from routes.main  import main_bp
from routes.admin import admin_bp
from routes.api   import api_bp


def create_app(config_object=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    CSRFProtect(app)

    login_manager = LoginManager(app)
    login_manager.login_view     = 'auth.login'
    login_manager.login_message  = ''

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    return app


def init_db(app: Flask):
    """Create tables and seed initial rows on first run."""
    with app.app_context():
        db.create_all()

        if not BackgroundSettings.query.first():
            db.session.add(BackgroundSettings())

        year = datetime.now().year
        if not WeeklyStats.query.filter_by(year=year).first():
            for w in range(1, 53):
                db.session.add(WeeklyStats(year=year, week=w))

        db.session.commit()
        print("OK  Database tables created/updated.")


app = create_app()

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    init_db(app)
    app.run(host='0.0.0.0', port=5000, debug=False)

