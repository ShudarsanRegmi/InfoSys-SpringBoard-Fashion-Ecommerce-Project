from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone
db = SQLAlchemy()

#to be changed as per the ER Diagram Provided by the team
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address_line_1 = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    approved = db.Column(db.Boolean, default=False)

    def __init__(self, password, email, address_line_1, role, firstname, lastname, pincode, state, city):
        self.password = password
        self.email = email
        self.address_line_1 = address_line_1
        self.role = role
        self.firstname = firstname
        self.lastname = lastname
        self.pincode = pincode
        self.state = state
        self.city = city

    def isAdmin(self):
        return self.role == 'admin' and self.id == 1 and self.email == "admin@springboard.com"

    def isDeliveryPerson(self):
        return self.role.lower() == 'delivery' and self.approved == True

    cart_items = db.relationship('CartItem', back_populates='user')
# Product Model (new)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    target_user = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255))
    description = db.Column(db.Text)
    details = db.Column(db.Text)
    colour = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    # Relationships
    cart_items = db.relationship('CartItem', back_populates='product')

    def __init__(self, name, price, stock_quantity, brand, size, target_user, type, image, description, details, colour, category):
        self.name = name
        self.price = price
        self.stock_quantity = stock_quantity
        self.brand = brand
        self.size = size
        self.target_user = target_user
        self.type = type
        self.image = image
        self.description = description
        self.details = details
        self.colour = colour
        self.category = category

    def __repr__(self):
        return self.name


class Order(db.Model):
    __tablename__ = 'orders'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    # Foreign Key from User table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Extracted from User table
    address_line_1 = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    # Derived from Stats table
    total_cost = db.Column(db.Float, nullable=False)
    # Date and status
    order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    delivered_date = db.Column(db.DateTime, nullable=True)  # Set when delivery is complete
    status = db.Column(db.String(50), nullable=False)  # Pending, Delivered, etc.
    # Foreign key reference to Product model
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    # Relationship to Product (if you want to access product from order)
    product = db.relationship('Product', back_populates='orders')

    # Relationships
    user = db.relationship('User', backref='orders')
    product = db.relationship('Product', backref='orders')

    def __init__(self, user_id, product_id, address_line_1, state, city, pincode, total_cost, status):
        self.user_id = user_id
        self.product_id = product_id
        self.address_line_1 = address_line_1
        self.state = state
        self.city = city
        self.pincode = pincode
        self.total_cost = total_cost
        self.status = status

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # Ensure this is present
    product_name = db.Column(db.String(120), nullable=False)
    product_image = db.Column(db.String(255), nullable=False)

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # Foreign key to User table
    product_id = db.Column(db.Integer, nullable=False)  # Foreign key to Product table

    def __repr__(self):
        return f'<Wishlist user_id={self.user_id}, product_id={self.product_id}>'
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    user = db.relationship('User', back_populates='cart_items')
    product = db.relationship('Product', back_populates='cart_items')
