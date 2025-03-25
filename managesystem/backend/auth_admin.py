from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from sqlite3 import Error
from backend.database import create_connection
from backend.auth_utils import login_required

auth_bp = Blueprint('auth', __name__, template_folder='../frontend/admin')

@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = create_connection()
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
                user = c.fetchone()
                
                if user:
                    # ตรวจสอบว่า role เป็น admin หรือไม่
                    if user[3] != 'admin':
                        flash('อนุญาตให้เฉพาะผู้ดูแลระบบ (Admin) เท่านั้นเข้าสู่ระบบ', 'danger')
                        return redirect(url_for('auth.login'))
                    
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

@auth_bp.route('/admin/logout')
@login_required
def logout():
    session.clear()
    flash('คุณได้ออกจากระบบแล้ว', 'info')
    return redirect(url_for('auth.login'))
