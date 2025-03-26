from flask import Blueprint, render_template, request, flash, redirect, url_for
from backend.database import create_connection
from datetime import datetime
from sqlite3 import Error
from backend.auth_utils import admin_login_required

discounts_bp = Blueprint('discounts', __name__ , template_folder='../frontend/admin')

@discounts_bp.route('/admin/discounts')
@admin_login_required
def view_discounts():
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM discounts")
            discounts = c.fetchall()
            return render_template('discounts.html', discounts=discounts)
        except Error as e:
            flash('Database error occurred', 'danger')
        finally:
            conn.close()
    return render_template('discounts.html', discounts=[])

@discounts_bp.route('/admin/add_discount', methods=['GET', 'POST'])
@admin_login_required
def add_discount():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        discount_percent = request.form['discount_percent']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        is_active = 1 if request.form.get('is_active') else 0
        
        conn = create_connection()
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute("""INSERT INTO discounts 
                            (name, description, discount_percent, start_date, end_date, is_active)
                            VALUES (?, ?, ?, ?, ?, ?)""",
                         (name, description, discount_percent, start_date, end_date, is_active))
                conn.commit()
                flash('Discount added successfully!', 'success')
                return redirect(url_for('discounts.view_discounts'))
            except Error as e:
                flash('Database error occurred', 'danger')
            finally:
                conn.close()
    
    return render_template('edit_discount.html', discount=None)

@discounts_bp.route('/admin/edit_discount/<int:discount_id>', methods=['GET', 'POST'])
@admin_login_required
def edit_discount(discount_id):
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            if request.method == 'POST':
                name = request.form['name']
                description = request.form.get('description', '')
                discount_percent = request.form['discount_percent']
                start_date = request.form['start_date']
                end_date = request.form['end_date']
                is_active = 1 if request.form.get('is_active') else 0
                
                c.execute("""UPDATE discounts SET 
                            name=?, description=?, discount_percent=?, 
                            start_date=?, end_date=?, is_active=?
                            WHERE id=?""",
                         (name, description, discount_percent, start_date, end_date, is_active, discount_id))
                conn.commit()
                flash('Discount updated successfully!', 'success')
                return redirect(url_for('discounts.view_discounts'))
            
            c.execute("SELECT * FROM discounts WHERE id=?", (discount_id,))
            discount = c.fetchone()
            return render_template('edit_discount.html', discount=discount)
        except Error as e:
            flash('Database error occurred', 'danger')
        finally:
            conn.close()
    return redirect(url_for('discounts.view_discounts'))

@discounts_bp.route('/admin/delete_discount/<int:discount_id>')
@admin_login_required
def delete_discount(discount_id):
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("DELETE FROM discounts WHERE id=?", (discount_id,))
            conn.commit()
            flash('Discount deleted successfully!', 'success')
        except Error as e:
            flash('Database error occurred', 'danger')
        finally:
            conn.close()
    return redirect(url_for('discounts.view_discounts'))
