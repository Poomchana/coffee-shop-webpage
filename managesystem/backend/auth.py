from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from werkzeug.security import check_password_hash
from sqlite3 import Error
from backend.database import create_connection

auth_bp = Blueprint('auth', __name__, template_folder='../frontend/store')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('กรุณากรอกชื่อผู้ใช้และรหัสผ่าน', 'warning')
            return redirect(url_for('auth.login'))

        conn = create_connection()
        if conn is not None:
            try:
                with conn:  
                    c = conn.cursor()
                    c.execute("SELECT id, username, password, role FROM users WHERE username = ?", (username,))
                    user = c.fetchone()
                
                if user:
                    # หากเป็น admin ให้เข้าสู่ระบบ
                    session['username'] = user[1]
                    session['role'] = user[3]
                    flash('เข้าสู่ระบบสำเร็จ', 'success')
                    next_page = request.args.get('next') or url_for('admin')
                    return redirect(next_page)
                else:
                    flash('ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง', 'danger')
            except Error as e:
                flash(f'เกิดข้อผิดพลาดฐานข้อมูล: {str(e)}', 'danger')
            finally:
                conn.close()
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('คุณได้ออกจากระบบแล้ว', 'info')
    return redirect(url_for('auth.login'))
