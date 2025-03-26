from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user
from backend.database import create_connection
from backend.user_model import User

admin_auth_bp = Blueprint('auth_admin', __name__, template_folder='../frontend')

@admin_auth_bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))  # ถ้าล็อกอินอยู่แล้วไปหน้า dashboard ทันที

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password, role FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data and user_data[2] == password:  # ควรใช้การเข้ารหัสรหัสผ่าน (เช่น bcrypt)
            if user_data[3] != 'admin':
                flash('อนุญาตให้เฉพาะผู้ดูแลระบบ (Admin) เท่านั้นเข้าสู่ระบบ', 'danger')
                return redirect(url_for('auth_admin.login'))
            
            user = User(user_data[0], user_data[1], user_data[3])
            login_user(user)  # บันทึกสถานะล็อกอิน

            flash('เข้าสู่ระบบสำเร็จ', 'success')
            next_page = request.args.get('next') or url_for('admin_dashboard')
            return redirect(next_page)

        flash('ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง', 'danger')

    return render_template('login.html')

@admin_auth_bp.route('/admin/logout')
def logout():
    logout_user()
    flash('คุณได้ออกจากระบบแล้ว', 'info')
    return redirect(url_for('auth_admin.login'))
