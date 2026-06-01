from datetime import datetime

import requests as _requests
from flask import Blueprint, jsonify, current_app
from flask_login import login_required

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/time')
@login_required
def api_time():
    now = datetime.now()
    return jsonify({
        'time': now.strftime('%H:%M:%S'),
        'date': now.strftime('%A, %d %B %Y'),
        'week': now.isocalendar()[1],
    })


@api_bp.route('/truck-stats')
@login_required
def truck_stats():
    # Proxies the truck-count API so the browser never calls it directly.
    # Returns nulls when not configured — UI shows '--' instead of crashing.
    url = current_app.config.get('TRUCK_API_URL', '').strip()
    if not url:
        return jsonify({'loaded': None, 'unloaded': None, 'issues': None,
                        'source': 'not_configured'})
    try:
        resp = _requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        # Handle both array and object responses
        if isinstance(data, list):
            data = data[0] if data else {}
        # Support both lowercase and capitalized keys
        loaded   = data.get('loaded')   or data.get('Loaded')
        unloaded = data.get('unloaded') or data.get('Unloaded')
        issues   = data.get('issues')   or data.get('Issues')
        return jsonify({
            'loaded':   loaded,
            'unloaded': unloaded,
            'issues':   issues,
            'source':   'api',
        })
    except Exception as e:
        return jsonify({'loaded': None, 'unloaded': None, 'issues': None,
                        'source': 'error', 'detail': str(e)}), 200


@api_bp.route('/stats/<int:year>')
@login_required
def stats_by_year(year):
    from models.stats import WeeklyStats
    rows = (WeeklyStats.query
            .filter_by(year=year)
            .order_by(WeeklyStats.week)
            .all())
    return jsonify({'year': year, 'rows': [r.to_dict() for r in rows]})
