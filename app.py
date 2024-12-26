from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_login import UserMixin
from datetime import datetime
from flask_migrate import Migrate
from flask_login import current_user

app = Flask(__name__)

# Configurations for the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'Infosys-Springboard-5.0'

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)


with app.app_context():
    db.create_all()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    rating = db.Column(db.Float)
    ratting = db.Column(db.String(100))

    def __repr__(self):
        return f'<Product {self.name}>'

# Dummy Product Data (for rendering)
products = [
    {
        'id': 1,
        'name': 'Classic White Shirt',
        'price': 1999,
        'image': 'static/Products/white.jpeg',
        'description': 'A timeless classic for any wardrobe, perfect for both formal and casual occasions.',
        'details': [
            'Made from 100% premium cotton.',
            'Breathable and comfortable for all-day wear.',
            'Available in multiple sizes for the perfect fit.',
            'Machine washable and easy to maintain.',
            'Perfect for office, events, and everyday use.'
        ]
    },
    {
        'id': 2,
        'name': 'Denim Jacket',
        'price': 3499,
        'image': 'static/Products/dDenim Jacket.jpeg',
        'description': 'A stylish denim jacket that adds an edgy touch to your outfit.',
        'details': [
            'Durable and soft denim fabric.',
            'Slim-fit design with button closure.',
            'Features side pockets and a classic collar.',
            'Perfect for layering in any season.',
            'Hand-wash recommended for extended durability.'
        ]
    },
    {
        'id': 3,
        'name': 'Summer Floral Dress',
        'price': 2799,
        'image': 'static/Products/dSummer Floral Dress.jpeg',
        'description': 'A breezy floral dress ideal for summer outings and vacations.',
        'details': [
            'Lightweight, flowy material for comfort.',
            'Beautiful floral prints with vibrant colors.',
            'Adjustable straps for a customized fit.',
            'Perfect for brunches, picnics, or beach outings.',
            'Machine washable and fade-resistant.'
        ]
    },
    {
        'id': 4,
        'name': 'Leather Wallet',
        'price': 1299,
        'image': 'static/Products/Leather Wallet.jpeg',
        'description': 'A sleek and functional leather wallet for everyday use.',
        'details': [
            'Crafted from genuine leather for durability.',
            'Multiple compartments for cards and cash.',
            'Compact design to fit in any pocket.',
            'Available in black and brown colors.',
            'A great gift for friends and family.'
        ]
    },
    {
        'id': 5,
        'name': 'Running Shoes',
        'price': 3999,
        'image': 'static/Products/shoes.jpeg',
        'description': 'High-performance running shoes for athletes and fitness enthusiasts.',
        'details': [
            'Breathable mesh upper for ventilation.',
            'Cushioned sole for maximum comfort.',
            'Slip-resistant outsole for stability.',
            'Lightweight design for enhanced speed.',
            'Available in various sizes and colors.'
        ]
    }
]
@app.route("/")
@app.route('/home')
def home():
    return render_template('home.html', products=products)

@app.route('/product/<int:product_id>')
def product_details(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product is None:
        return "Product not found", 404
    return render_template('product.html', product=product)
@app.route('/cart')
def view_cart():
    # Get the current user's ID
    user_id = current_user.id
    
    # Query the Cart model to get cart items for the current user
    cart_items = Cart.query.filter_by(user_id=user_id).join(Product).all()
    
    # Calculate the total price
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    # Render the cart template with the cart items and total price
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)



if __name__ == '__main__':
    app.run(debug=True)
