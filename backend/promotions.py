from flask import Blueprint, render_template, request, flash, redirect, url_for
from backend.database import create_connection

promotions_bp = Blueprint('promotions', __name__ , template_folder='../frontend')

@promotions_bp.route('/promotions')
def view_promotions():
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM promotions")
            promotions = c.fetchall()
            return render_template('promotions.html', promotions=promotions)
        except Error as e:
            flash('Database error occurred', 'danger')
        finally:
            conn.close()
    return render_template('promotions.html', promotions=[])

@promotions_bp.route('/add_promotion', methods=['GET', 'POST'])
def add_promotion():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        promo_code = request.form['promo_code']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        is_active = 1 if request.form.get('is_active') else 0
        
        conn = create_connection()
        if conn is not None:
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
                flash('Database error occurred', 'danger')
            finally:
                conn.close()
    
    return render_template('edit_promotion.html', promotion=None)

@promotions_bp.route('/edit_promotion/<int:promotion_id>', methods=['GET', 'POST'])
def edit_promotion(promotion_id):
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            if request.method == 'POST':
                name = request.form['name']
                description = request.form.get('description', '')
                promo_code = request.form['promo_code']
                start_date = request.form['start_date']
                end_date = request.form['end_date']
                is_active = 1 if request.form.get('is_active') else 0
                
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
            flash('Database error occurred', 'danger')
        finally:
            conn.close()
    return redirect(url_for('promotions.view_promotions'))

@promotions_bp.route('/delete_promotion/<int:promotion_id>')
def delete_promotion(promotion_id):
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("DELETE FROM promotions WHERE id=?", (promotion_id,))
            conn.commit()
            flash('Promotion deleted successfully!', 'success')
        except Error as e:
            flash('Database error occurred', 'danger')
        finally:
            conn.close()
    return redirect(url_for('promotions.view_promotions'))