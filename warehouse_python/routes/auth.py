from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from models import db, User
from models.settings import BackgroundSettings

auth_bp = Blueprint('auth', __name__)


def _get_background():
    bg = BackgroundSettings.query.first()
    if not bg:
        bg = BackgroundSettings()
        db.session.add(bg)
        db.session.commit()
    return bg


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    bg    = _get_background()
    error = None

    if request.method == 'POST':
        username = request.form.get('login', '').strip()
        password = request.form.get('password', '')
        user     = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))

        error = 'Invalid username or password.'

    return render_template('login.html', bg=bg, error=error)



@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Only available when no users exist yet — creates the first admin account.
    if User.query.count() > 0:
        flash('Public registration is disabled. Contact an administrator.', 'warning')
        return redirect(url_for('auth.login'))

    error = None

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')

        if not username or not password:
            error = 'All fields are required.'
        elif password != confirm:
            error = 'Passwords do not match.'
        elif len(password) < 8:
            error = 'Password must be at least 8 characters.'
        elif User.query.filter_by(username=username).first():
            error = 'Username is already taken.'
        else:
            user = User(email=username, username=username, role='admin')
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Admin account created!', 'success')
            return redirect(url_for('main.dashboard'))

    return render_template('register.html', error=error)
