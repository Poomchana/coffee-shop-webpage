from functools import wraps
from flask import redirect, url_for, flash, session

def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('กรุณาเข้าสู่ระบบก่อนใช้งาน', 'warning')
            return redirect(url_for('auth_admin.login'))
        return f(*args, **kwargs)
    return decorated_function

def shop_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('กรุณาเข้าสู่ระบบก่อนใช้งาน', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
