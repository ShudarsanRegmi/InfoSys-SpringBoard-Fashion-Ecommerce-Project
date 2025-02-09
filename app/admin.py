from flask import Blueprint, request, jsonify, get_flashed_messages, redirect, url_for, render_template, flash
from datetime import datetime, timezone, timedelta
from flask_login import login_required, current_user
from .models import db, User, Product, Order, ProductAddLogs, OrderItems
from .decorators import is_admin
from .forms import AddItemForm
from .methods import send_approval_email, send_order_deleted_mail
from werkzeug.security import generate_password_hash
from .visualization import Visualize
import base64
from sqlalchemy import func
import os
from werkzeug.utils import secure_filename
import uuid
import random
import string
from sqlalchemy.exc import IntegrityError

# Define the admin blueprint
admin = Blueprint('admin', __name__)

#Define the Visualization Object
visualize = Visualize()

## Team 3

@admin.route('/')
@login_required
@is_admin
def index():
    return render_template('admin.html')


@admin.route('/product/new', methods=['GET', 'POST'])
@login_required
@is_admin
def new_product():
    if request.method == 'POST':
        try:
            # Extract form fields
            name = request.form['name']
            description = request.form['description']
            details = request.form['details']
            price = float(request.form['price'])
            stock_quantity = int(request.form['stock_quantity'])
            brand = request.form['brand']
            size = request.form['size']
            target_user = request.form['target_user']
            type_ = request.form['type']
            rating = request.form.get('rating', 'not rated')
            color = request.form.get('color', 'nocolor')
            category = request.form['category']

            # Validate required fields
            if not all([name, description, brand, category, size, target_user, type_]):
                return "Missing required fields", 400

            # Handle image upload (if exists)
            image = request.files.get('image')
            image_filename = None
            if image:
                # Ensure the 'static/uploads' directory exists
                uploads_dir = os.path.join('app/static', 'product_uploads')
                if not os.path.exists(uploads_dir):
                    os.makedirs(uploads_dir)  # Create the directory if it doesn't exist

                #generate unique filename
                image_filename = f"{uuid.uuid4().hex}_{secure_filename(image.filename)}"
                image_path = os.path.join(uploads_dir, image_filename)
                image.save(image_path)

            # Create the product object
            new_product = Product(
                name=name,
                description=description,
                details=details,
                price=price,
                stock_quantity=stock_quantity,
                brand=brand,
                size=size,
                target_user=target_user,
                type=type_,
                rating=rating,
                category=category,
                colour=color,
                image=image_filename
            )

            db.session.add(new_product)
            db.session.commit()
            productaddlogs = ProductAddLogs(new_product.id, stock_quantity, price*stock_quantity)
            db.session.add(productaddlogs)
            # Commit to the database
            db.session.commit()

            flash("Product added successfully!", "success")
            return redirect(url_for('admin.product_list'))

        except Exception as e:
            db.session.rollback()
            print(f"Error while adding product: {e}")  # Log the error to the console
            return f"Error while adding product: {e}", 500  # Return the error message

    return render_template('add-shop-items.html')
##########
@admin.route('/product/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@is_admin
def update_product(id):
    # Fetch the product from the database by its ID
    product = db.session.get(Product, id)
    if product is None:
        return "Product not found", 404
        
    if request.method == 'POST':
        try:
            # Extract form fields
            name = request.form['name']
            description = request.form['description']
            details = request.form['details']
            price = float(request.form['price'])
            stock_quantity = int(request.form['stock_quantity'])
            brand = request.form['brand']
            size = request.form['size']
            target_user = request.form['target_user']
            type_ = request.form['type']
            category = request.form['category']

            # Validate required fields
            if not all([name, description, brand, category, size, target_user, type_]):
                return "Missing required fields", 400

            # Handle image upload (if exists)
            image_filename = product.image  # Retain the old image filename if no new image is uploaded
            image = request.files.get('image')
            if image:
                # Ensure the 'static/uploads' directory exists
                uploads_dir = os.path.join('app/static', 'uploads')
                if not os.path.exists(uploads_dir):
                    os.makedirs(uploads_dir)  # Create the directory if it doesn't exist

                # Sanitize the image filename and save it
                image_filename = secure_filename(image.filename)
                image_path = os.path.join(uploads_dir, image_filename)
                image.save(image_path)
            
            if stock_quantity<product.stock_quantity:
                productaddlogs = ProductAddLogs(product.id, product.stock_quantity-stock_quantity, price*product.stock_quantity-stock_quantity)
                db.session.add(productaddlogs)

            # Update the product object with new data
            product.name = name
            product.description = description
            product.details = details
            product.price = price
            product.stock_quantity = stock_quantity
            product.brand = brand
            product.size = size
            product.target_user = target_user
            product.type = type_
            product.category = category
            product.image = image_filename  # Update the image (if new image uploaded)

            # Commit to the database
            db.session.commit()

            flash("Product updated successfully!", "success")
            return redirect(url_for('admin.product_list'))  # Redirect to the product list page

        except Exception as e:
            db.session.rollback()
            print(f"Error occurred while updating product: {e}")
            return f"Error while updating product: {e}", 500  # Internal error

    # If it's a GET request, render the form with the current product data
    return render_template('update-product.html', product=product)


@admin.route('/products', methods=['GET'])
@login_required
@is_admin
def product_list():

    products = Product.query.all()

    # Render the template to display all products
    return render_template('product-list.html', products=products)

@admin.route('/product/delete/<int:id>', methods=['POST'])
@login_required
@is_admin
def delete_product(id):
    # Fetch the product from the database by its ID
    product = db.session.get(Product, id)
    if product is None:
        return "Product not found", 404

    try:
        # Delete the product
        db.session.delete(product)
        db.session.commit()

        print(f"Product {id} deleted successfully")
        return redirect(url_for('admin.product_list'))  # Redirect back to the product list page

    except IntegrityError as e:

        db.session.rollback()
        users = User.query.join(OrderItems, User.id == OrderItems.UserID)\
                  .filter(OrderItems.ProductID == product.id)\
                  .all()

        OrderItems.query.filter_by(ProductID=id).delete()

        # Find orders that no longer have order items
        empty_orders = Order.query.outerjoin(OrderItems, Order.id == OrderItems.OrderID)\
                                 .filter(OrderItems.OrderID.is_(None))\
                                 .all()
        
        # Delete those empty orders
        for order in empty_orders:
            db.session.delete(order)
        # Delete all related product add logs
        ProductAddLogs.query.filter_by(product_id=id).delete()

        # Finally, delete the product
        db.session.delete(product)
        db.session.commit()

        # Finally, delete the product
        db.session.delete(product)
        db.session.commit()
        

        for _ in users:
            send_order_deleted_mail(_.email, _.firstname+" "+_.lastname ,product.name)

    except Exception as e:
        print(f"Error occurred while deleting product: {e}")
        db.session.rollback()
        return "Error while deleting product", 500  # Internal server error

    return redirect(url_for('admin.product_list'))

@admin.route('/approve-delivery-dashboard')
@login_required
@is_admin
def approve_delivery_dashboard():
    delivery_user_request = User.query.filter_by(role='delivery', approved = False).all()
    get_flashed_messages()
    return render_template('approve_delivery.html', delivery_persons=delivery_user_request)

@admin.route("/delete-user/<int:user_id>", methods = ["DELETE"])
@login_required
@is_admin
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        db.session.delete(user)
        db.session.commit()
        send_approval_email(user.email, user.firstname, False)
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500
    finally:
        db.session.close()


@admin.route('/view_orders', methods=['GET'])
@login_required
@is_admin
def view_orders():
    orders = Order.query.all()
    return render_template('view_order.html', orders=orders)


@admin.route("/approve-user/<int:user_id>", methods = ["POST"])
@login_required
@is_admin
def approve_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        user.approved = True
        db.session.commit()
        send_approval_email(user.email, user.firstname, True)
        return jsonify({'message': 'User approved successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500
    finally:
        db.session.close()

#view for chart dashboards
@admin.route("/stats")
@login_required
@is_admin
def stats():
    return render_template('stats.html')

#chart 1 : new and returning customers records
@admin.route('/chart1')
@login_required
@is_admin
def show_chart1():

    first_order_dates = db.session.query(
        Order.customer_id,
        func.min(func.date(Order.order_date)).label('first_order_date')
    ).group_by(Order.customer_id).subquery()

    # Query to calculate new and returning customers per order_date
    stats = db.session.query(
        func.date(Order.order_date).label('order_date'),
        func.count(func.distinct(Order.customer_id)).filter(
            Order.customer_id.in_(
                db.session.query(first_order_dates.c.customer_id).filter(
                    func.date(Order.order_date) == first_order_dates.c.first_order_date
                )
            )
        ).label('new_customers'),
        func.count(func.distinct(Order.customer_id)).filter(
            Order.customer_id.notin_(
                db.session.query(first_order_dates.c.customer_id).filter(
                    func.date(Order.order_date) == first_order_dates.c.first_order_date
                )
            )
        ).label('returning_customers')
    ).group_by(func.date(Order.order_date)).all()

    data = [[] for _ in range(3)]

    for row in stats:
        data[0].append(str(row.order_date))
        data[1].append(row.new_customers)
        data[2].append(row.returning_customers)

    img = visualize.generate_new_old_customers_graph(data[0], data[1], data[2])

    img = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('show_graph.html', img = img, context = {"graph_name" : "New and Returning Customers", "data" : [[data[0][i], data[1][i], data[2][i]] for i in range(len(data[0]))],  "Attributes": ["Order Date", "New Customers", "Returning Customers"]})

@admin.route('/chart2')
@login_required
@is_admin
def show_chart2():
    sales_data = db.session.query(
        func.date(Order.order_date).label('date'),
        func.sum(Order.price).label('total_sales')
    ).group_by(
        func.date(Order.order_date)
    ).order_by(
        func.date(Order.order_date)
    ).all()

    data = [[],[]]

    for row in sales_data:
        data[0].append(str(row.date))
        data[1].append(row.total_sales)
    
    img = visualize.generate_revenue_overtime_graph(data[0], data[1])
    img = base64.b64encode(img.getvalue()).decode('utf8')
    return render_template('show_graph.html', img = img, context = {"graph_name" : "Revenue Over Time", "data" : [[data[0][i], round(data[1][i], 2)] for i in range(len(data[0]))], "Attributes": ["Date", "Total Sales"]})

@admin.route('/chart3')
@login_required
@is_admin
def show_chart3():
    results = (
    db.session.query(Order.status, func.count(Order.status))
    .group_by(Order.status)
    .order_by(Order.status)
    .all()
    )

    status = [result[0] for result in results]
    count = [result[1] for result in results]

    img = visualize.generate_order_status_graph(status, count)
    img = base64.b64encode(img.getvalue()).decode('utf8')
    return render_template('show_graph.html', img = img, context = {"graph_name" : "Order Status", "data" : [[status[i], count[i]] for i in range(len(status))], "Attributes": ["Status", "Count"]})

@admin.route('/chart4')
@login_required
@is_admin
def show_chart4():
    results = (
    db.session.query(Product.category, func.sum(Product.stock_quantity))
    .group_by(Product.category).all())

    products = []
    stocks = []

    for row in results:
        products.append(row[0])
        stocks.append(row[1])
    
    img = visualize.generate_inventory_stocks_graph(products, stocks)
    img = base64.b64encode(img.getvalue()).decode('utf8')
    return render_template('inventory_stocks_insights.html', img = img, context = {"graph_name" : "Inventory Stock Levels", "data" : [[products[i], stocks[i]] for i in range(len(products))], "Attributes": ["Category", "Stock"]})

@admin.route('/chart5')
@login_required
@is_admin
def show_chart5():
    results_expenses = db.session.query(
        func.date(ProductAddLogs.date_added).label('date'),  # Group by date only (ignore time part)
        func.sum(ProductAddLogs.cost).label('total_cost')
    ).group_by(func.date(ProductAddLogs.date_added)).all()
    sales_data = db.session.query(
        func.date(Order.order_date).label('date'),
        func.sum(Order.price).label('total_sales')
    ).group_by(
        func.date(Order.order_date)
    ).order_by(
        func.date(Order.order_date)
    ).all()

    dates = [str(result.date) for result in results_expenses]
    expenses = [round(result.total_cost, 2) for result in results_expenses]
    revenue = [round(result.total_sales, 2) for result in sales_data]

    img = visualize.generate_finantial_overview_graph(dates, expenses, revenue)
    img = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template("show_graph.html", img = img, context = {"graph_name" : "Finantial Overview", "data" : [[dates[i], expenses[i], revenue[i], round(revenue[i]-expenses[i],2)] for i in range(len(dates))], "Attributes": ["Date", "Expenses", "Revenue", "Profits"]} )

@admin.route('/chart6')
@login_required
@is_admin
def show_chart6():
    result = db.session.query(User.role, func.count(User.role)).filter(User.role.in_(["user", "admin"])).group_by(User.role).all()
    approved_delivery = db.session.query(func.count(User.role)).filter(User.approved == True, User.role == "delivery").first()
    roles = [row[0] for row in result]
    count = [row[1] for row in result]
    roles.append("delivery")
    count.append(approved_delivery[0])
    img = visualize.user_role_distribution_graph(roles, count)
    img = base64.b64encode(img.getvalue()).decode('utf8')
    return render_template('show_graph.html', img = img, context = {"graph_name" : "User Roles Distributions", "data" : [[roles[i], count[i]] for i in range(len(roles))], "Attributes": ["Roles", "Count"]})

@admin.route("/chart7")
@login_required
@is_admin
def show_chart7():
    state_order_counts = (db.session.query(User.state, func.count(Order.id).label("order_count")).join(Order, User.id == Order.customer_id).group_by(User.state).order_by(func.count(Order.id).desc()).all())
    states = [row[0] for row in state_order_counts]
    order_counts = [row[1] for row in state_order_counts]
    img = visualize.generate_state_order_distribution_graph(states, order_counts)
    img = base64.b64encode(img.getvalue()).decode('utf8')
    return render_template('show_graph.html', img = img, context = {"graph_name" : "State Order Distribution", "data" : [[states[i], order_counts[i]] for i in range(len(states))], "Attributes": ["State", "Order Count"]})

@admin.route('/get-stock-chart/<category>', methods = ["GET"])
@login_required
@is_admin
def get_chart(category):
    if request.method == "GET":
        products = Product.query.filter(Product.category == category).all()
        products_name = [product.name for product in products]
        products_stocks = [product.stock_quantity for product in products]

        img = visualize.generate_inventory_stocks_graph(products_name, products_stocks, category)
        img = base64.b64encode(img.getvalue()).decode('utf8')

        return jsonify({"image": img, "data": [products_name, products_stocks]})

# dummy to be removed later
@admin.route('/make_me_admin')
@login_required
def make_me_admin():
    if not current_user.isAdmin():
        current_user.role = 'admin'
        db.session.commit()
    return redirect(url_for('views.home'))


