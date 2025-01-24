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
    category = db.Column(db.String(100),nullable=False)
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
    _tablename_ = 'orders'

    id = db.Column(db.Integer, primary_key=True)


    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    customer_name = db.Column(db.String(100), nullable=False)
    place = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.Float, nullable=False)
    district = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)

    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    #another required attributes
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable = False)
    order_date = db.Column(db.DateTime, nullable = False, default = datetime.now(timezone.utc))

    #establising the relationsip
    user = db.relationship('User', backref = db.backref('orders', lazy = True))
    product = db.relationship('Product', backref = db.backref('orders', lazy = True))

    def __init__(self, customer_id, price, status, product_id, order_date = datetime.now(timezone.utc)):
        self.customer_id = customer_id
        self.product_id = product_id
        self.price = price
        self.status = status
        self.order_date = order_date

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
