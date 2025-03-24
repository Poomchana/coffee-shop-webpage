from flask import Blueprint, render_template, request, flash, redirect, url_for
from backend.database import create_connection
from datetime import datetime

members_bp = Blueprint('members', __name__ , template_folder='../frontend')

@members_bp.route('/members')
def view_members():
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM members")
            members = c.fetchall()
            return render_template('members.html', members=members)
        except Error as e:
            flash('Database error occurred', 'danger')
        finally:
            conn.close()
    return render_template('members.html', members=[])

@members_bp.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form.get('email', '')
        join_date = datetime.now().strftime('%Y-%m-%d')
        
        conn = create_connection()
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute("INSERT INTO members (name, phone, email, join_date) VALUES (?, ?, ?, ?)",
                         (name, phone, email, join_date))
                conn.commit()
                flash('Member added successfully!', 'success')
                return redirect(url_for('members.view_members'))
            except Error as e:
                flash('Database error occurred', 'danger')
            finally:
                conn.close()
    
    return render_template('edit_member.html', member=None)

@members_bp.route('/edit_member/<int:member_id>', methods=['GET', 'POST'])
def edit_member(member_id):
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            if request.method == 'POST':
                name = request.form['name']
                phone = request.form['phone']
                email = request.form.get('email', '')
                points = request.form.get('points', 0)
                is_active = 1 if request.form.get('is_active') else 0
                
                c.execute("""UPDATE members SET 
                            name=?, phone=?, email=?, points=?, is_active=?
                            WHERE id=?""",
                         (name, phone, email, points, is_active, member_id))
                conn.commit()
                flash('Member updated successfully!', 'success')
                return redirect(url_for('members.view_members'))
            
            c.execute("SELECT * FROM members WHERE id=?", (member_id,))
            member = c.fetchone()
            return render_template('edit_member.html', member=member)
        except Error as e:
            flash('Database error occurred', 'danger')
        finally:
            conn.close()
    return redirect(url_for('members.view_members'))

@members_bp.route('/delete_member/<int:member_id>')
def delete_member(member_id):
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute("DELETE FROM members WHERE id=?", (member_id,))
            conn.commit()
            flash('Member deleted successfully!', 'success')
        except Error as e:
            flash('Database error occurred', 'danger')
        finally:
            conn.close()
    return redirect(url_for('members.view_members'))