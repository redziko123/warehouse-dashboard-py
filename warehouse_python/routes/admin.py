from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from models import db
from models.user import User, Employee
from models.content import NewsItem, TipItem, WarningItem, Lesson
from models.stats import WeeklyStats
from models.settings import BackgroundSettings
from utils.helpers import admin_required, save_uploaded_image, delete_static_image

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def _get_background():
    bg = BackgroundSettings.query.first()
    if not bg:
        bg = BackgroundSettings()
        db.session.add(bg)
        db.session.commit()
    return bg



@admin_bp.route('')
@admin_bp.route('/')
@login_required
@admin_required
def admin_panel():
    return render_template('admin/index.html')



@admin_bp.route('/stats', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_stats():
    year    = request.args.get('year', datetime.now().year, type=int)
    message = None

    if request.method == 'POST':
        year = int(request.form.get('year', datetime.now().year))
        for week in range(1, 53):
            loaded   = int(request.form.get(f'loaded_{week}',   0) or 0)
            unloaded = int(request.form.get(f'unloaded_{week}', 0) or 0)
            errors   = int(request.form.get(f'errors_{week}',   0) or 0)
            row = WeeklyStats.query.filter_by(year=year, week=week).first()
            if not row:
                row = WeeklyStats(year=year, week=week)
                db.session.add(row)
            row.loaded_trucks   = loaded
            row.unloaded_trucks = unloaded
            row.errors          = errors
        db.session.commit()
        message = 'Statistics saved!'

    stats_rows = (WeeklyStats.query
                  .filter_by(year=year)
                  .order_by(WeeklyStats.week)
                  .all())
    stats_map = {r.week: r for r in stats_rows}
    return render_template('admin/stats.html',
                           stats_map=stats_map, year=year,
                           message=message, range52=range(1, 53))



@admin_bp.route('/news', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_news():
    message = None
    error   = None

    if request.method == 'POST':
        action = request.form.get('action', 'add')

        if action == 'add':
            title = request.form.get('title', '').strip()
            desc  = request.form.get('description', '').strip()
            if not title or not desc:
                error = 'Title and description are required.'
            else:
                image_url = save_uploaded_image(request.files.get('image'), 'news')
                db.session.add(NewsItem(title=title, description=desc,
                                        image_url=image_url,
                                        date=datetime.utcnow()))
                db.session.commit()
                message = 'Article added!'

        elif action == 'delete':
            item = NewsItem.query.get(int(request.form.get('news_id', 0)))
            if item:
                delete_static_image(item.image_url or '')
                db.session.delete(item)
                db.session.commit()
                message = 'Article deleted.'

        elif action == 'edit':
            item = NewsItem.query.get(int(request.form.get('news_id', 0)))
            if item:
                item.title       = request.form.get('title', item.title).strip()
                item.description = request.form.get('description', item.description).strip()
                new_img = request.files.get('image')
                if new_img and new_img.filename:
                    delete_static_image(item.image_url or '')
                    item.image_url = save_uploaded_image(new_img, 'news')
                db.session.commit()
                message = 'Article updated.'

    news = NewsItem.query.order_by(NewsItem.date.desc()).all()
    return render_template('admin/news.html', news=news, message=message, error=error)



@admin_bp.route('/tips', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_tips():
    message = None
    error   = None

    if request.method == 'POST':
        action = request.form.get('action', 'add')

        if action == 'add':
            text         = request.form.get('text', '').strip()
            is_important = 'is_important' in request.form
            if not text:
                error = 'Tip content is required.'
            else:
                db.session.add(TipItem(text=text, is_important=is_important,
                                       date=datetime.utcnow()))
                db.session.commit()
                message = 'Tip added!'

        elif action == 'delete':
            item = TipItem.query.get(int(request.form.get('tip_id', 0)))
            if item:
                db.session.delete(item)
                db.session.commit()
                message = 'Tip deleted.'

        elif action == 'edit':
            tip_id       = int(request.form.get('tip_id', 0))
            text         = request.form.get('text', '').strip()
            is_important = 'is_important' in request.form
            item = TipItem.query.get(tip_id)
            if item and text:
                item.text         = text
                item.is_important = is_important
                db.session.commit()
                message = 'Tip updated.'

    tips = TipItem.query.order_by(TipItem.date.desc()).all()
    return render_template('admin/tips.html', tips=tips, message=message, error=error)



@admin_bp.route('/warnings', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_warnings():
    message = None
    error   = None

    if request.method == 'POST':
        action = request.form.get('action', 'add')

        if action == 'add':
            title = request.form.get('title', '').strip()
            desc  = request.form.get('description', '').strip()
            if not title or not desc:
                error = 'Title and description are required.'
            else:
                image_url = save_uploaded_image(request.files.get('image'), 'warnings') or ''
                db.session.add(WarningItem(title=title, description=desc,
                                           image_url=image_url, is_active=True,
                                           date=datetime.utcnow()))
                db.session.commit()
                message = 'Warning added!'

        elif action == 'delete':
            item = WarningItem.query.get(int(request.form.get('warning_id', 0)))
            if item:
                delete_static_image(item.image_url)
                db.session.delete(item)
                db.session.commit()
                message = 'Warning deleted.'

        elif action == 'toggle':
            item = WarningItem.query.get(int(request.form.get('warning_id', 0)))
            if item:
                item.is_active = not item.is_active
                db.session.commit()
                message = 'Warning status updated.'

    warnings = WarningItem.query.order_by(WarningItem.date.desc()).all()
    return render_template('admin/warnings.html', warnings=warnings,
                           message=message, error=error)



LESSON_CATEGORIES = ['General', 'Safety', 'Quality']


@admin_bp.route('/lessons', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_lessons():
    message = None
    error   = None

    if request.method == 'POST':
        action = request.form.get('action', 'add')

        if action == 'add':
            title    = request.form.get('title', '').strip()
            desc     = request.form.get('description', '').strip()
            if not title or not desc:
                error = 'Title and description are required.'
            else:
                item = Lesson(
                    title=title,
                    description=desc,
                    content=request.form.get('content', '').strip(),
                    image_url=save_uploaded_image(request.files.get('image'), 'lessons'),
                    category=request.form.get('category', 'General').strip(),
                    is_featured='is_featured' in request.form,
                    order=int(request.form.get('order', 0) or 0),
                )
                db.session.add(item)
                db.session.commit()
                message = 'Training added!'

        elif action == 'delete':
            item = Lesson.query.get(int(request.form.get('lesson_id', 0)))
            if item:
                delete_static_image(item.image_url or '')
                db.session.delete(item)
                db.session.commit()
                message = 'Training deleted.'

        elif action == 'edit':
            item = Lesson.query.get(int(request.form.get('lesson_id', 0)))
            if item:
                item.title       = request.form.get('title', item.title).strip()
                item.description = request.form.get('description', item.description).strip()
                item.content     = request.form.get('content', item.content).strip()
                item.category    = request.form.get('category', item.category).strip()
                item.is_featured = 'is_featured' in request.form
                item.order       = int(request.form.get('order', item.order) or item.order)
                new_img = save_uploaded_image(request.files.get('image'), 'lessons')
                if new_img:
                    delete_static_image(item.image_url or '')
                    item.image_url = new_img
                db.session.commit()
                message = 'Training updated.'

    lessons = Lesson.query.order_by(Lesson.order, Lesson.title).all()
    return render_template('admin/lessons.html', lessons=lessons,
                           categories=LESSON_CATEGORIES,
                           message=message, error=error)



@admin_bp.route('/background', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_background():
    bg      = _get_background()
    message = None
    error   = None

    if request.method == 'POST':
        home_file = request.files.get('home_image')
        home_url  = request.form.get('home_url', '').strip()
        if home_file and home_file.filename:
            saved = save_uploaded_image(home_file, 'backgrounds')
            if saved:
                delete_static_image(bg.home_background_url)
                bg.home_background_url = saved
            else:
                error = 'File format not allowed.'
        elif home_url:
            bg.home_background_url = home_url
        elif 'clear_home' in request.form:
            delete_static_image(bg.home_background_url)
            bg.home_background_url = ''

        login_file = request.files.get('login_image')
        login_url  = request.form.get('login_url', '').strip()
        if login_file and login_file.filename:
            saved = save_uploaded_image(login_file, 'backgrounds')
            if saved:
                delete_static_image(bg.login_background_url)
                bg.login_background_url = saved
            else:
                error = error or 'Niedozwolony format pliku.'
        elif login_url:
            bg.login_background_url = login_url
        elif 'clear_login' in request.form:
            delete_static_image(bg.login_background_url)
            bg.login_background_url = ''

        if not error:
            db.session.commit()
            message = 'Backgrounds updated!'

    return render_template('admin/background.html', bg=bg, message=message, error=error)



@admin_bp.route('/users', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_users():
    message = None
    error   = None

    if request.method == 'POST':
        action = request.form.get('action', 'add')

        if action == 'add':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            role     = request.form.get('role', 'user')
            if not username or not password:
                error = 'All fields are required.'
            elif len(password) < 8:
                error = 'Password must be at least 8 characters.'
            elif User.query.filter_by(username=username).first():
                error = 'Username is already taken.'
            else:
                u = User(email=username, username=username, role=role)
                u.set_password(password)
                db.session.add(u)
                db.session.commit()
                message = f'User {username} added.'

        elif action == 'delete':
            user_id = int(request.form.get('user_id', 0))
            if user_id == current_user.id:
                error = 'You cannot delete your own account.'
            else:
                u = User.query.get(user_id)
                if u:
                    db.session.delete(u)
                    db.session.commit()
                    message = 'User deleted.'

        elif action == 'change_role':
            u = User.query.get(int(request.form.get('user_id', 0)))
            if u and u.id != current_user.id:
                u.role = request.form.get('role', 'user')
                db.session.commit()
                message = 'User role updated.'

        elif action == 'reset_password':
            password = request.form.get('new_password', '')
            u = User.query.get(int(request.form.get('user_id', 0)))
            if u and len(password) >= 8:
                u.set_password(password)
                db.session.commit()
                message = 'Password has been reset.'
            else:
                error = 'Password must be at least 8 characters.'

    users = User.query.order_by(User.username).all()
    return render_template('admin/users.html', users=users, message=message, error=error)



@admin_bp.route('/birthdays', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_birthdays():
    message = None
    error   = None

    if request.method == 'POST':
        action = request.form.get('action', 'add')

        if action == 'add':
            name     = request.form.get('name', '').strip()
            birthday = request.form.get('birthday', '')
            if not name or not birthday:
                error = 'Name and birthday are required.'
            else:
                try:
                    bday = datetime.strptime(birthday, '%Y-%m-%d').date()
                    db.session.add(Employee(name=name, birthday=bday))
                    db.session.commit()
                    message = f'{name} has been added.'
                except ValueError:
                    error = 'Invalid date format.'

        elif action == 'delete':
            emp = Employee.query.get(int(request.form.get('employee_id', 0)))
            if emp:
                db.session.delete(emp)
                db.session.commit()
                message = 'Employee deleted.'

        elif action == 'edit':
            emp_id   = int(request.form.get('employee_id', 0))
            name     = request.form.get('name', '').strip()
            birthday = request.form.get('birthday', '')
            emp = Employee.query.get(emp_id)
            if emp and name and birthday:
                try:
                    emp.name     = name
                    emp.birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
                    db.session.commit()
                    message = 'Employee data updated.'
                except ValueError:
                    error = 'Invalid date format.'

    employees = sorted(Employee.query.order_by(Employee.name).all(),
                       key=lambda e: e.days_until_birthday())
    return render_template('admin/birthdays.html', employees=employees,
                           message=message, error=error)
