import os
import uuid
from functools import wraps

from flask import abort, url_for, current_app
from flask_login import current_user


def admin_required(f):
    """Blocks access for non-admin users with a 403."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated



def allowed_file(filename: str) -> bool:
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', set())
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


def save_uploaded_image(file_storage, subfolder: str = 'general') -> str | None:
    """Saves upload to static/uploads/<subfolder>/ and returns its URL, or None."""
    if not file_storage or file_storage.filename == '':
        return None
    if not allowed_file(file_storage.filename):
        return None

    ext      = file_storage.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    dest_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(dest_dir, exist_ok=True)
    file_storage.save(os.path.join(dest_dir, filename))

    return url_for('static', filename=f'uploads/{subfolder}/{filename}')


def delete_static_image(url: str) -> None:
    if not url:
        return
    try:
        rel       = url.split('/static/', 1)[1]
        full_path = os.path.join(current_app.static_folder, rel)
        if os.path.isfile(full_path):
            os.remove(full_path)
    except Exception:
        pass
