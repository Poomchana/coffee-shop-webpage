from flask import Blueprint, render_template, request, flash, redirect, url_for
from backend.database import create_connection
from backend.auth_utils import login_required
from sqlite3 import Error

promotions_bp = Blueprint('promotions', __name__, template_folder='../frontend/managesystem')

@promotions_bp.route('/admin/promotions')
@login_required
def view_promotions():
    conn = create_connection()
    promotions = []
    if conn:
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM promotions")
            promotions = c.fetchall()
        except Error as e:
            flash(f'Database error: {str(e)}', 'danger')
        finally:
            conn.close()
    return render_template('promotions.html', promotions=promotions)

@promotions_bp.route('/admin/add_promotion', methods=['GET', 'POST'])
@login_required
def add_promotion():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        promo_code = request.form['promo_code']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        is_active = 1 if request.form.get('is_active') else 0

        # ตรวจสอบวันที่
        if start_date > end_date:
            flash('Start date cannot be later than end date.', 'danger')
            return render_template('edit_promotion.html', promotion=None)

        conn = create_connection()
        if conn:
            try:
                c = conn.cursor()
                c.execute("""INSERT INTO promotions 
                            (name, description, promo_code, start_date, end_date, is_active)
                            VALUES (?, ?, ?, ?, ?, ?)""",
                         (name, description, promo_code, start_date, end_date, is_active))
                conn.commit()
                flash('Promotion added successfully!', 'success')
                return redirect(url_for('promotions.view_promotions'))
            except Error as e:
                flash(f'Database error: {str(e)}', 'danger')
            finally:
                conn.close()
    
    return render_template('edit_promotion.html', promotion=None)

@promotions_bp.route('/admin/edit_promotion/<int:promotion_id>', methods=['GET', 'POST'])
@login_required
def edit_promotion(promotion_id):
    conn = create_connection()
    if conn:
        try:
            c = conn.cursor()
            if request.method == 'POST':
                name = request.form['name']
                description = request.form.get('description', '')
                promo_code = request.form['promo_code']
                start_date = request.form['start_date']
                end_date = request.form['end_date']
                is_active = 1 if request.form.get('is_active') else 0

                # ตรวจสอบวันที่
                if start_date > end_date:
                    flash('Start date cannot be later than end date.', 'danger')
                    return redirect(url_for('promotions.edit_promotion', promotion_id=promotion_id))

                c.execute("""UPDATE promotions SET 
                            name=?, description=?, promo_code=?, 
                            start_date=?, end_date=?, is_active=?
                            WHERE id=?""",
                         (name, description, promo_code, start_date, end_date, is_active, promotion_id))
                conn.commit()
                flash('Promotion updated successfully!', 'success')
                return redirect(url_for('promotions.view_promotions'))
            
            c.execute("SELECT * FROM promotions WHERE id=?", (promotion_id,))
            promotion = c.fetchone()
            return render_template('edit_promotion.html', promotion=promotion)
        except Error as e:
            flash(f'Database error: {str(e)}', 'danger')
        finally:
            conn.close()
    
    return redirect(url_for('promotions.view_promotions'))

@promotions_bp.route('/admin/delete_promotion/<int:promotion_id>')
@login_required
def delete_promotion(promotion_id):
    conn = create_connection()
    if conn:
        try:
            c = conn.cursor()
            c.execute("DELETE FROM promotions WHERE id=?", (promotion_id,))
            conn.commit()
            flash('Promotion deleted successfully!', 'success')
        except Error as e:
            flash(f'Database error: {str(e)}', 'danger')
        finally:
            conn.close()
    
    return redirect(url_for('promotions.view_promotions'))
