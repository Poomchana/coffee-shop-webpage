from flask import Blueprint, render_template, request, flash, redirect, url_for
from backend.database import create_connection

inventory_bp = Blueprint('inventory', __name__  , template_folder='../frontend')

@inventory_bp.route('/inventory')
def view_inventory():
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM inventory")
            items = c.fetchall()
            return render_template('inventory.html', items=items)
        except Error as e:
            flash('Database error occurred', 'danger')
        finally:
            conn.close()
    return render_template('inventory.html', items=[])

@inventory_bp.route('/add_inventory', methods=['GET', 'POST'])
def add_inventory():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        unit = request.form['unit']
        threshold = request.form.get('threshold', 0)
        
        conn = create_connection()
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute("INSERT INTO inventory (name, quantity, unit, threshold) VALUES (?, ?, ?, ?)",
                         (name, quantity, unit, threshold))
                conn.commit()
                flash('Inventory item added successfully!', 'success')
                return redirect(url_for('inventory.view_inventory'))
            except Error as e:
                flash('Database error occurred', 'danger')
            finally:
                conn.close()
    
    return render_template('add_inventory.html')