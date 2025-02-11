from flask import Flask, session, jsonify, redirect, url_for # added for appinit endpoint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from flask_migrate import Migrate
from .models import db, User
from itsdangerous import URLSafeTimedSerializer

# for appinit endpoint
import random
import string
from sqlalchemy.exc import IntegrityError
from .models import db, User, Product, Order, ProductAddLogs, OrderItems
from datetime import datetime, timezone, timedelta
from werkzeug.security import generate_password_hash

from .constants import STATES_CITY

login_manager = LoginManager()
migrate = Migrate()

# Initialize the serializer globally (used for URL token generation)
URL_SERIALIZER = None


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app(config_class="Config"):
    """Create and configure the Flask application."""
    app = Flask(__name__)    
    # Load the configuration from config.py
    app.config.from_object(f"config.{config_class}")

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Set the login view for flask-login
    
    # Initialize migration
    migrate.init_app(app, db)
    
    # Initialize URL serializer (used for token generation)
    global URL_SERIALIZER
    URL_SERIALIZER = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    # Register Blueprints
    from .views import bp as views_bp
    from .auth import auth as auth_bp
    from .admin import admin as admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(views_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Create the tables (if needed)
    with app.app_context():
        db.create_all()

    @app.route('/appinit')
    # @login_required
    def appinit():
        dummy_users = []
        failed_users = []
        dummy_products = []
        created_order_ids = []

        # Create admin user
        try:
            admin_user = User(
                firstname="Admin",
                lastname="Springboard",
                email="admin@springboard.com",
                address_line_1="Random Address",
                state="State1",
                city="City1",
                role="admin",
                pincode=123456,
                password=generate_password_hash('admin')
            )
            db.session.add(admin_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

        # Add 100 dummy users
        for _ in range(100):
            firstname, lastname, email, address_line_1, state, city, role, pincode, password, approved = generate_random_user_data()
            user = User(
                firstname=firstname,
                lastname=lastname,
                email=email,
                address_line_1=address_line_1,
                state=state,
                city=city,
                role=role,
                pincode=pincode,
                password=password
            )
            user.approved = approved
            try:
                db.session.add(user)
                db.session.commit()  # Commit inside try to catch IntegrityError
                dummy_users.append(email)
            except IntegrityError:
                db.session.rollback()  # Roll back the session to handle the exception
                failed_users.append(email)

        # Add dummy products
        from .constants import PRODUCTS
        for product in PRODUCTS:
            product_instance = Product(
                name=product['name'],
                price=product['price'],
                stock_quantity=product['stock_quantity'],
                brand=product['brand'],
                size=product['size'],
                target_user=product['target_user'],
                type=product['type'],
                image=product['image'],
                description=product['description'],
                details=product['details'],
                colour=product['colour'],
                category=product['category']
            )
            db.session.add(product_instance)
            db.session.commit()
            dummy_products.append(product['name'])
                
        # Create dummy orders
        # Filter users with role 'user'
        users = User.query.filter_by(role='user').all()
        
        #Filter delivery_persons
        delivery_persons = User.query.filter_by(role='delivery', approved=True).all()

        # Filter products with stock > 0
        products = Product.query.filter(Product.stock_quantity > 0).all()

        if not users or not products:
            print("Please ensure there are users with role 'user' and products with stock > 0 in the database.")
            return

        # Set the start date for 3 months ago
        start_date = datetime.now(timezone.utc) - timedelta(days=90)
        current_date = datetime.now(timezone.utc)

        # Generate orders for each day in the past 3 months
        while start_date <= current_date:
            orders_per_day = random.randint(10, 25)
            for _ in range(orders_per_day):
                # Select a random user and product
                user = random.choice(users)

                #generate order items
                order_items = []
                number_of_items = 0
                total_price_of_order = 0

                tryes = 0
                #one to 4 items per order
                while number_of_items < random.randint(1,3):
                    tryes += 1
                    if tryes >= 30:
                        print("tries more than 30")
                        break

                    product_choice = random.choice(products)
                    if product_choice.stock_quantity <= 0:
                        continue
                    if product_choice in order_items:
                        continue
                    total_price_of_order += product_choice.price
                    order_items.append(product_choice)
                    number_of_items+=1

                # Generate order details
                customer_name = f"{user.firstname} {user.lastname}"
                address_line_1 = user.address_line_1
                state = user.state
                city = user.city
                pincode = user.pincode
                price = total_price_of_order
                status = random.choice(["Pending", "Delivered", "Cancelled"])
                order_date = start_date + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
                delivery_date = None

                if status == "Delivered":
                    order_date = start_date + timedelta(days=random.randint(1, 90))
                    delivery_date = order_date + timedelta(days=random.randint(1, 7))
                mail = user.email
                

                # Create an Order instance
                order = Order(
                    customer_id=user.id,
                    customer_name=customer_name,
                    address_line_1=address_line_1,
                    state=state,
                    pincode=pincode,
                    city=city,
                    price=price,
                    status=status,
                    order_date=order_date,
                    mail=mail,
                )

                if delivery_date:
                    order.delivery_person_id = random.choice(delivery_persons).id
                    order.delivery_date = delivery_date

                db.session.add(order)
                db.session.flush()  # Get the order ID immediately after adding

                # Generate order item details

                
                for product in order_items:
                    max_quantity = min(5, product.stock_quantity)
                    quantity = random.randint(1, max_quantity)
                    order_item = OrderItems(
                        OrderID=order.id,
                        ProductID=product.id,
                        UserID=user.id,
                        Quantity=quantity,
                        Price=round(product.price * quantity, 2),
                    )
                    db.session.add(order_item)

                # Reduce the product stock
                product.stock_quantity -= quantity
                db.session.add(product)

            # Move to the next day
            start_date += timedelta(days=1)

        db.session.commit()

            
        # Route to create dummy entries for ProductAddLogs for products within the past 90 days
        # Track dummy log entries created
        created_logs = []

        # Get all products created in the past 90 days
        today = datetime.now(timezone.utc)
        start_date = today - timedelta(days=90)
        products = Product.query.all()

        for product in products:
            # Create random log entries for each product within the last 90 days
            for _ in range(random.randint(1, 5)):  # Randomly create 1 to 5 log entries per product
                quantity = random.randint(1, 50)  # Random quantity added
                cost = round(random.uniform(5, 1000), 2)  # Random cost between 5 and 1000

                log = ProductAddLogs(
                    product_id=product.id,
                    quantity=quantity,
                    cost=cost*quantity,
                    date_added=random.choice([start_date + timedelta(days=i) for i in range(90)])  # Random date within the last 90 days
                )

                try:
                    db.session.add(log)
                    db.session.commit()
                    created_logs.append(f"Product ID {product.id}, Quantity {quantity}, Cost {cost}")
                except IntegrityError:
                    db.session.rollback()  # In case of a database error

        return jsonify({
            "message": "App initialization complete.",
            "manual_users": ["admin@springboard.com", "user@user.com"],
            "created_users": dummy_users,
            "failed_users": failed_users,
            "created_products": dummy_products,
            "created_orders": created_order_ids,
            "product_added_logs": created_logs
        })

    @app.route('/make_me_admin')
    @login_required
    def make_me_admin():
        if not current_user.isAdmin():
            current_user.role = 'admin'
            db.session.commit()
        return redirect(url_for('views.home'))


    return app

def generate_random_user_data():
    firstname = ''.join(random.choices(string.ascii_letters, k=8)).capitalize()
    lastname = ''.join(random.choices(string.ascii_letters, k=10)).capitalize()
    email = f"{firstname.lower()}.{lastname.lower()}@example.com"
    address_line_1 = f"{random.randint(1, 999)} {random.choice(['Main St', 'Second St', 'Broadway'])}"
    state = random.choice(list(STATES_CITY.keys())[1:])
    city = random.choice(list(STATES_CITY[state]))
    role = random.choice(["user", "delivery"])
    pincode = f"{random.randint(10000, 99999)}"
    approved = random.choice([True, False]) if role == "delivery" else False
    password = generate_password_hash('password123')  # You can change the password
    return firstname, lastname, email, address_line_1, state, city, role, pincode, password, approved
