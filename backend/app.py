import sys
from pathlib import Path
from flask import Flask, render_template, redirect, url_for, session, request  # เพิ่ม request ตรงนี้
from flask_login import LoginManager
from functools import wraps

# เพิ่ม path ของโปรเจคลงในระบบ
sys.path.insert(0, str(Path(__file__).parent.parent))

app = Flask(__name__, template_folder='../frontend')
app.secret_key = 'your_secret_key_here'  # ควรเปลี่ยนเป็นรหัสลับที่แท้จริง

# ตั้งค่า Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# สร้าง decorator สำหรับตรวจสอบการล็อกอิน
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('auth.login', next=request.url))  # ใช้ request ตรงนี้
        return f(*args, **kwargs)
    return decorated_function

# Import และลงทะเบียน Blueprints
from backend.auth import auth_bp
from backend.inventory import inventory_bp
from backend.menu import menu_bp
from backend.discounts import discounts_bp
from backend.promotions import promotions_bp
from backend.sales import sales_bp
from backend.members import members_bp

app.register_blueprint(auth_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(discounts_bp)
app.register_blueprint(promotions_bp)
app.register_blueprint(sales_bp)
app.register_blueprint(members_bp)

@app.route('/')
@login_required
def home():
    return render_template('dashboard.html')

# ฟังก์ชันสำหรับโหลดผู้ใช้
@login_manager.user_loader
def load_user(user_id):
    from backend.database import create_connection
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user if user else None

if __name__ == '__main__':
    app.run(debug=True)