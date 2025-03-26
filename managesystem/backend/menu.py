from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from backend.database import create_connection
from backend.auth_utils import admin_login_required
from sqlite3 import Error

menu_bp = Blueprint('menu', __name__, template_folder='../frontend')

@menu_bp.route('/admin/menu', methods=['GET', 'POST'])
@admin_login_required
def view_menu():
    search_query = request.form.get('search', '')

    conn = create_connection()
    items = []
    if conn:
        try:
            c = conn.cursor()
            if search_query:
                c.execute("SELECT * FROM menu_items WHERE name LIKE ?", ('%' + search_query + '%',))
            else:
                c.execute("SELECT * FROM menu_items")
            items = c.fetchall()
        except Error as e:
            flash(f'Database error: {str(e)}', 'danger')
        finally:
            conn.close()
    
    return render_template('menu.html', items=items)

@menu_bp.route('/admin/add_menu_item', methods=['GET', 'POST'])
@admin_login_required
def add_menu_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        price = request.form['price']
        category = request.form.get('category', '')

        conn = create_connection()
        if conn:
            try:
                c = conn.cursor()
                c.execute("INSERT INTO menu_items (name, description, price, category) VALUES (?, ?, ?, ?)",
                         (name, description, price, category))
                conn.commit()
                flash('Menu item added successfully!', 'success')
                return redirect(url_for('menu.view_menu'))
            except Error as e:
                flash(f'Database error: {str(e)}', 'danger')
            finally:
                conn.close()
    
    return render_template('edit_menu.html', item=None)

@menu_bp.route('/admin/edit_menu_item/<int:item_id>', methods=['GET', 'POST'])
@admin_login_required
def edit_menu_item(item_id):
    conn = create_connection()
    if conn:
        try:
            c = conn.cursor()
            if request.method == 'POST':
                name = request.form['name']
                description = request.form.get('description', '')
                price = request.form['price']
                category = request.form.get('category', '')
                is_available = 1 if request.form.get('is_available') else 0  # ป้องกัน None

                c.execute("""UPDATE menu_items SET 
                            name=?, description=?, price=?, category=?, is_available=?
                            WHERE id=?""",
                         (name, description, price, category, is_available, item_id))
                conn.commit()
                flash('Menu item updated successfully!', 'success')
                return redirect(url_for('menu.view_menu'))
            
            c.execute("SELECT * FROM menu_items WHERE id=?", (item_id,))
            item = c.fetchone()
            return render_template('edit_menu.html', item=item)
        except Error as e:
            flash(f'Database error: {str(e)}', 'danger')
        finally:
            conn.close()
    
    return redirect(url_for('menu.view_menu'))

@menu_bp.route('/admin/delete_menu_item/<int:item_id>')
@admin_login_required
def delete_menu_item(item_id):
    conn = create_connection()
    if conn:
        try:
            c = conn.cursor()
            c.execute("DELETE FROM menu_items WHERE id=?", (item_id,))
            conn.commit()
            flash('Menu item deleted successfully!', 'success')
        except Error as e:
            flash(f'Database error: {str(e)}', 'danger')
        finally:
            conn.close()
    
    return redirect(url_for('menu.view_menu'))
