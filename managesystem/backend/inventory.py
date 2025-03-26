from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from backend.database import create_connection
from backend.auth_utils import admin_login_required
from sqlite3 import Error

inventory_bp = Blueprint('inventory', __name__, template_folder='../frontend')

@inventory_bp.route('/admin/inventory')
@admin_login_required
def view_inventory():
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM inventory")
            items = c.fetchall()
            return render_template('inventory.html', items=items)
        except Error as e:
            flash(f'Database error occurred: {str(e)}', 'danger')
        finally:
            conn.close()
    return render_template('inventory.html', items=[])

@inventory_bp.route('/admin/add_inventory', methods=['GET', 'POST'])
@admin_login_required
def add_inventory():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        unit = request.form['unit']
        threshold = request.form.get('threshold', 0)
        branches = request.form.get('branches')
        
        # Check if branches is provided or set to empty string if not
        if not branches:
            branches = ''
        
        conn = create_connection()
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute("INSERT INTO inventory (name, quantity, unit, threshold, branches) VALUES (?, ?, ?, ?, ?) ",
                         (name, quantity, unit, threshold, branches))
                conn.commit()
                flash('Inventory item added successfully!', 'success')
                return redirect(url_for('inventory.view_inventory'))
            except Error as e:
                flash(f'Database error occurred: {str(e)}', 'danger')
            finally:
                conn.close()
    
    return render_template('add_inventory.html')

@inventory_bp.route('/admin/edit_inventory/<int:item_id>', methods=['GET', 'POST'])
@admin_login_required
def edit_inventory(item_id):
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            if request.method == 'POST':
                name = request.form['name']
                quantity = request.form['quantity']
                unit = request.form['unit']
                threshold = request.form.get('threshold', 0)
                branches = request.form.get('branches')
                
                # Ensure branches is provided or set to empty string if not
                if not branches:
                    branches = ''
                
                c.execute("UPDATE inventory SET name=?, quantity=?, unit=?, threshold=?, branches=? WHERE id=?", 
                         (name, quantity, unit, threshold, branches, item_id))
                conn.commit()
                flash('Inventory item updated successfully!', 'success')
                return redirect(url_for('inventory.view_inventory'))
            
            c.execute("SELECT * FROM inventory WHERE id=?", (item_id,))
            item = c.fetchone()
            return render_template('edit_inventory.html', item=item)
        except Error as e:
            flash(f'Database error occurred: {str(e)}', 'danger')
        finally:
            conn.close()
    return redirect(url_for('inventory.view_inventory'))

@inventory_bp.route('/admin/delete_inventory/<int:item_id>')
@admin_login_required
def delete_inventory(item_id):
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("DELETE FROM inventory WHERE id=?", (item_id,))
            conn.commit()
            flash('Inventory item deleted successfully!', 'success')
        except Error as e:
            flash(f'Database error occurred: {str(e)}', 'danger')
        finally:
            conn.close()
    return redirect(url_for('inventory.view_inventory'))
