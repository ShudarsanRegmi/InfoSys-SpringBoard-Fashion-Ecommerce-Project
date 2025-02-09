from flask_testing import TestCase
from app import create_app, db
from app.models import User, Order, Product, OrderItems
from werkzeug.security import generate_password_hash

class TestOrderManagement(TestCase):

    def create_app(self):
        """Configure the Flask app for testing."""
        app = create_app(config_class="TestConfig")
        return app
    
    def setUp(self):
        self.user = User(
                firstname="Test",
                lastname="User",
                email="test@example.com",
                address_line_1="123 Test St",
                state="Uttarakhand",
                city="Dehradun",
                role="delivery",
                pincode="123456",
                password=generate_password_hash('password', method='pbkdf2:sha256')
            )
        self.user.approved = True
        db.session.add(self.user)
        db.session.commit()
        self.client.post('/login', data={"email": "test@example.com", "password": "password"})

    def test_dashboard(self):
        response = self.client.get('/partner_dash')
        self.assertEqual(response.status_code, 200)

    def test_update_status(self):
        dummy_user = User(
                password=generate_password_hash('122', method = "pbkdf2:sha256"),
                email = "example.example.com",
                address_line_1 = "filmystan",
                role="user",
                firstname="Mr.X",
                lastname="Y",
                state =  "ASD",
                city="city11",
                pincode="123123"
            )
        db.session.add(dummy_user)
        db.session.commit()
        # Add sample products
        product1 = Product(name="Product A", stock_quantity=10, category="Category1", price=1023, brand="abx", size="M", target_user="bots", type="clothing", image="sample", description="sample", details="sample", colour="sample", rating=4)
        product2 = Product(name="Product B", stock_quantity=20, category="Category2", price=1023, brand="abx", size="M", target_user="bots", type="clothing", image="sample", description="sample", details="sample", colour="sample", rating=4)
        db.session.add_all([product1, product2])

        # Commit product data before adding orders
        db.session.commit()
        # Add sample orders
        order1 = Order(dummy_user.id, dummy_user.firstname, dummy_user.address_line_1, dummy_user.state, dummy_user.pincode, dummy_user.city, product1.price, "Pending")
        db.session.add(order1)
        db.session.commit()  # Commit so order1.id is available

        order1item = OrderItems(order1.id, product1.id, dummy_user.id, 1, product1.price)

        db.session.add(order1item)
        db.session.commit()

        response = self.client.post(f'/update_status/{order1.id}', data={'status': 'Delivered'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)


class TestProductRating(TestCase):
    def create_app(self):
        """Configure the Flask app for testing."""
        app = create_app(config_class="TestConfig")
        return app
    
    def setUp(self):
        self.user = User(
                firstname="Test",
                lastname="User",
                email="test@example.com",
                address_line_1="123 Test St",
                state="Uttarakhand",
                city="Dehradun",
                role="user",
                pincode="123456",
                password=generate_password_hash('password', method='pbkdf2:sha256')
            )
        db.session.add(self.user)
        db.session.commit()
        self.client.post('/login', data={"email": "test@example.com", "password": "password"})

    # def test_rate_product(self):
    #     product = Product(name='Test Rate', description='Test', details='Details', price=20.0,
    #                       stock_quantity=10, brand='Brand', size='L', target_user='Men',
    #                       type='Clothing', category='Fashion', rating='not rated', image='image.jpg', colour='Red')
    #     db.session.add(product)
    #     db.session.commit()
    #      # Add sample orders

    #     #add dummy user
    #     dummy_user = User(
    #         password=generate_password_hash('122', method = "pbkdf2:sha256"),
    #         email = "example.example.com",
    #         address_line_1 = "filmystan",
    #         role="user",
    #         firstname="Mr.X",
    #         lastname="Y",
    #         state =  "ASD",
    #         city="city11",
    #         pincode="123123"
    #     )
    #     db.session.add(dummy_user)
    #     db.session.commit()
    #     order1 = Order(dummy_user.id, dummy_user.firstname, dummy_user.address_line_1, dummy_user.state, dummy_user.pincode, dummy_user.city, product.price, "Pending")
    #     db.session.add(order1)
    #     db.session.commit()  # Commit so order1.id is available

    #     order1item = OrderItems(order1.id, product.id, dummy_user.id, 1, product.price)

    #     db.session.add(order1item)
    #     db.session.commit()

    #     response = self.client.post(f'/rate_product/{order1.id}', data={'rating': '5'}, follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)


