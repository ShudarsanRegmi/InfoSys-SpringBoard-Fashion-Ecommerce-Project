import pytest
from flask import session
from app import create_app
from app.models import db,Wishlist,CartItem,User
@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite://',  
        'SECRET_KEY': 'test-secret-key',
    })

    with app.app_context():
        db.create_all()  # Set up the database
    yield app  # Provide the app to the tests
@pytest.fixture()
def client(app):
    return app.test_client()
def test_add_to_cart(client):
    """Test adding a product to the cart."""
    response = client.post('/add_to_cart/1', follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction() as session:
        assert session['cart'] == {1: 1}


def test_update_cart_quantity(client):
    """Test updating the quantity of a product in the cart."""
    with client.session_transaction() as session:
        session['cart'] = {1: 1}
    
    response = client.post('/update_quantity/1', json={'quantity': 3})
    assert response.status_code == 200
    assert response.json['success'] is True
    assert response.json['new_quantity'] == 3


def test_remove_from_cart(client):
    """Test removing a product from the cart."""
    with client.session_transaction() as session:
        session['cart'] = {1: 1}
    
    response = client.post('/remove-from-cart/1', follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction() as session:
        assert 'cart' in session
        assert 1 not in session['cart']


def test_add_to_wishlist(client):
    """Test adding a product to the wishlist."""
    user = User(id=1, username='test_user')
    db.session.add(user)
    db.session.commit()
    with client.session_transaction() as session:
        session['user_id'] = 1

    response = client.post('/add_to_wishlist/1', follow_redirects=True)
    assert response.status_code == 200
    wishlist_item = Wishlist.query.filter_by(user_id=1, product_id=1).first()
    assert wishlist_item is not None


def test_remove_from_wishlist(client):
    """Test removing a product from the wishlist."""
    user = User(id=1, username='test_user')
    db.session.add(user)
    db.session.commit()

    wishlist_item = Wishlist(user_id=1, product_id=1)
    db.session.add(wishlist_item)
    db.session.commit()

    with client.session_transaction() as session:
        session['user_id'] = 1

    response = client.post('/remove-from-wishlist/1', follow_redirects=True)
    assert response.status_code == 200
    wishlist_item = Wishlist.query.filter_by(user_id=1, product_id=1).first()
    assert wishlist_item is None


def test_search(client):
    """Test the search functionality."""
    response = client.get('/search?query=shirt')
    assert response.status_code == 200
    assert b"Classic White Shirt" in response.data
if __name__ == '__main__':
    pytest.main()
