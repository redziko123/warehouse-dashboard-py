from datetime import datetime, date

from flask import Blueprint, render_template, request
from flask_login import login_required

from models import db
from models.content import NewsItem, TipItem, WarningItem, Lesson
from models.stats import WeeklyStats
from models.user import Employee
from models.settings import BackgroundSettings


main_bp = Blueprint('main', __name__)


def _get_background():
    bg = BackgroundSettings.query.first()
    if not bg:
        bg = BackgroundSettings()
        db.session.add(bg)
        db.session.commit()
    return bg


@main_bp.route('/')
@login_required
def dashboard():
    bg       = _get_background()
    year     = datetime.now().year
    week_num = datetime.now().isocalendar()[1]

    stats_rows = (WeeklyStats.query
                  .filter_by(year=year)
                  .order_by(WeeklyStats.week)
                  .all())

    news     = NewsItem.query.order_by(NewsItem.date.desc()).limit(6).all()
    tips     = TipItem.query.order_by(TipItem.date.desc()).limit(10).all()
    lessons  = (Lesson.query
                .filter_by(is_featured=True)
                .order_by(Lesson.order)
                .limit(6)
                .all())
    warnings = (WarningItem.query
                .filter_by(is_active=True)
                .order_by(WarningItem.date.desc())
                .limit(10)
                .all())

    employees_sorted = [
        e for e in sorted(
            Employee.query.all(),
            key=lambda e: e.days_until_birthday()
        )
        if e.days_until_birthday() <= 7
    ]

    stats_rows_json = [r.to_dict() for r in stats_rows]
    current_stats   = next((r for r in stats_rows if r.week == week_num),     None)
    prev_stats      = next((r for r in stats_rows if r.week == week_num - 1), None)

    return render_template(
        'dashboard.html',
        bg=bg,
        stats_rows=stats_rows,
        stats_rows_json=stats_rows_json,
        current_week=week_num,
        current_stats=current_stats,
        prev_stats=prev_stats,
        news=news,
        tips=tips,
        lessons=lessons,
        warnings=warnings,
        upcoming_birthdays=employees_sorted,
        now=datetime.now(),
    )



@main_bp.route('/news/<int:news_id>')
@login_required
def news_detail(news_id):
    item = NewsItem.query.get_or_404(news_id)
    return render_template('news_detail.html', item=item)



@main_bp.route('/lessons')
@login_required
def lessons_page():
    category = request.args.get('category', '')
    query    = Lesson.query.order_by(Lesson.order, Lesson.title)
    if category:
        query = query.filter_by(category=category)
    lessons    = query.all()
    categories = [c[0] for c in db.session.query(Lesson.category).distinct().all()]
    return render_template('lessons.html', lessons=lessons,
                           categories=categories, selected_category=category)



@main_bp.route('/lessons/<int:lesson_id>')
@login_required
def lesson_detail(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    return render_template('lesson_detail.html', lesson=lesson)
