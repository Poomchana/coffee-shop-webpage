from flask import Blueprint, render_template, request
from backend.database import create_connection
from datetime import datetime

sales_bp = Blueprint('sales', __name__  , template_folder='../frontend/managesystem')

@sales_bp.route('/admin/sales')
def view_sales():
    period = request.args.get('period', 'day')
    
    conn = create_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            
            if period == 'day':
                date = datetime.now().strftime('%Y-%m-%d')
                c.execute("SELECT * FROM sales WHERE date(transaction_date) = ?", (date,))
                title = "Today's Sales"
            elif period == 'month':
                month = datetime.now().strftime('%Y-%m')
                c.execute("SELECT * FROM sales WHERE strftime('%Y-%m', transaction_date) = ?", (month,))
                title = "This Month's Sales"
            elif period == 'year':
                year = datetime.now().strftime('%Y')
                c.execute("SELECT * FROM sales WHERE strftime('%Y', transaction_date) = ?", (year,))
                title = "This Year's Sales"
            else:
                c.execute("SELECT * FROM sales")
                title = "All Sales"
            
            sales = c.fetchall()
            
            # Calculate totals
            total_sales = sum(sale[2] for sale in sales)
            total_discounts = sum(sale[3] for sale in sales)
            
            return render_template('sales.html', 
                                sales=sales, 
                                period=period,
                                title=title,
                                total_sales=total_sales,
                                total_discounts=total_discounts)
        except Error as e:
            flash('Database error occurred', 'danger')
        finally:
            conn.close()
    return render_template('sales.html', sales=[], period=period, title="Sales Report")