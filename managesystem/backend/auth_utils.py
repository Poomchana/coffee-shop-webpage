from flask import redirect, url_for, flash
from flask_login import current_user
from functools import wraps

def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('กรุณาล็อกอินก่อนเข้าใช้งาน', 'danger')
            return redirect(url_for('auth_admin.login'))
        return f(*args, **kwargs)
    return decorated_function

