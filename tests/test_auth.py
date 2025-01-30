import os
import pytest
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app and SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy()

# Configuration class (including testing configuration)
class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Log SQL queries if True

class TestingConfig(Config):
    """Testing configuration."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///test.db'
    TESTING = True
    DEBUG = False
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False

# Choose the configuration for testing
app.config.from_object(TestingConfig)  # This ensures the correct config is used

db.init_app(app)

# Database models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'

# Routes for your e-commerce features (cart, wishlist, etc.)
@app.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    return jsonify(message=f"Product {product_id} added to cart"), 200

@app.route('/cart')
def view_cart():
    return jsonify(message="Viewing cart"), 200

@app.route('/wishlist/add/<int:product_id>', methods=['POST'])
def add_to_wishlist(product_id):
    return jsonify(message=f"Product {product_id} added to wishlist"), 200

@app.route('/wishlist')
def view_wishlist():
    return jsonify(message="Viewing wishlist"), 200

@app.route('/search')
def search_category():
    category = request.args.get('category', 'Electronics')
    return jsonify(message=f"Searching for products in {category} category"), 200

@app.route('/checkout', methods=['POST'])
def checkout():
    address = request.json.get('address', 'No address provided')
    return jsonify(message=f"Order placed successfully to {address}"), 200

# Test setup using pytest
@pytest.fixture
def client():
    # Use application context to allow access to app's components
    with app.app_context():
        with app.test_client() as client:
            db.create_all()  # Create tables for tests
            yield client  # Provide the test client for the test
            db.drop_all()  # Clean up after test

@pytest.fixture
def sample_product():
    # Updated product details
    with app.app_context():  # Ensure we're inside the app context for database interactions
        product = Product(name="Denim Jacket", price=3499, category="Clothing")
        db.session.add(product)
        db.session.commit()
        db.session.refresh(product)  # Explicitly refresh the product to ensure it's attached to the session
        return product

# Sample test cases for the routes
def test_add_to_cart(client, sample_product):
    response = client.post(f'/cart/add/{sample_product.id}', json={"quantity": 1})
    assert response.status_code == 200
    assert f"Product {sample_product.id} added to cart" in response.get_json()['message']  # Updated assertion

def test_view_cart(client, sample_product):
    client.post(f'/cart/add/{sample_product.id}', json={"quantity": 1})
    response = client.get('/cart')
    assert response.status_code == 200
    assert "Viewing cart" in response.get_json()['message']

def test_add_to_wishlist(client, sample_product):
    response = client.post(f'/wishlist/add/{sample_product.id}')
    assert response.status_code == 200
    assert f"Product {sample_product.id} added to wishlist" in response.get_json()['message']  # Updated assertion

def test_view_wishlist(client, sample_product):
    client.post(f'/wishlist/add/{sample_product.id}')
    response = client.get('/wishlist')
    assert response.status_code == 200
    assert "Viewing wishlist" in response.get_json()['message']

def test_search_category(client):
    response = client.get('/search?category=Clothing')
    assert response.status_code == 200
    assert "Searching for products" in response.get_json()['message']


