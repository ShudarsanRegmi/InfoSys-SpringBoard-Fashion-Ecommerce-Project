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

    #RelationShips 
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
    rating = db.Column(db.String(100))

    # Relationsships
    cart_items = db.relationship('CartItem', back_populates='product')


    def __init__(self, name, price, stock_quantity, brand, size, target_user, type, image, description, details, colour, category, rating=None):
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
        self.rating = rating

    def __repr__(self):
        return self.name
        

class Order(db.Model):
    __tablename__ = 'orders'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    delivery_person_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, default = None)

    # Order Details
    price = db.Column(db.Float, nullable=False)
    delivery_date = db.Column(db.DateTime, nullable=True, default=None)
    status = db.Column(db.String(50), nullable=False, default = "Pending")
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    # Additional Columns
    customer_name = db.Column(db.String(100), nullable=False)
    address_line_1 = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.Float, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(50), nullable=False)

    # Establishing the relationship
    user = db.relationship('User', foreign_keys=[customer_id],backref=db.backref('orders', lazy=True))
    delivery_person = db.relationship('User', foreign_keys=[delivery_person_id], backref = 'deliveries')

    def __init__(
        self,
        customer_id,
        customer_name,
        address_line_1,
        state,
        pincode,
        city,
        price,
        status,
        order_date=datetime.now(timezone.utc),
        mail=None
    ):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.state = state
        self.pincode = pincode
        self.city = city
        self.price = price
        self.status = status
        self.order_date = order_date
        self.address_line_1 = address_line_1
        self.mail = mail or f"customer{customer_id}@example.com"  # Default email if not provided


class OrderItems(db.Model):
    # primary key
    OrderItemID = db.Column(db.Integer, primary_key=True)
    # foreign keys
    OrderID = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    UserID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #other attributes
    Quantity = db.Column(db.Integer, nullable=False)
    Price = db.Column(db.Float, nullable=False)
    #estb. of relationship
    user = db.relationship('User', backref=db.backref('ordersitem', lazy=True))
    product = db.relationship('Product', backref=db.backref('ordersitem', lazy=True))
    order = db.relationship('Order', backref=db.backref('ordersitem', lazy=True))

    def __init__(self, OrderID, ProductID, UserID, Quantity, Price):
        self.OrderID = OrderID
        self.ProductID = ProductID
        self.UserID = UserID
        self.Quantity = Quantity
        self.Price = Price

    def __repr__(self):
        return f"{self.OrderID}"



class ProductAddLogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    quantity = db.Column(db.Integer, nullable=False) 
    cost = db.Column(db.Float, nullable=False)
    product = db.relationship('Product', backref=db.backref('product_add_logs', lazy=True))

    def __init__(self, product_id, quantity, cost, date_added=None):
        self.product_id = product_id
        self.quantity = quantity
        self.cost = cost
        self.date_added = date_added if date_added else datetime.now(timezone.utc)



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

class ProductRatings(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    rate = db.Column(db.Float)
    description = db.Column(db.String(250), nullable=True)


    user = db.relationship('User')
    product = db.relationship('Product')

    def __init__(self, user_id, product_id, rating, desc):
        self.user_id=user_id
        self.product_id=product_id
        self.rate = rating
        self.description = desc