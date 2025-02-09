import unittest
from flask_testing import TestCase
from main import create_app, db
from werkzeug.security import generate_password_hash
from app.models import User, Product, Order, ProductAddLogs, OrderItems

class TestVisualization(TestCase):

    def create_app(self):
        """Configure the Flask app for testing."""
        app = create_app(config_class="TestConfig")
        return app

    def setUp(self):
        """Set up the test database and add sample data."""
        db.create_all()
        self.add_sample_data()

    def tearDown(self):
        """Tear down the test database."""
        db.session.remove()
        db.drop_all()

    def add_sample_data(self):
        """Add sample data for testing."""
        # Add admin user
        admin_user = User(
            password=generate_password_hash('123', method="pbkdf2:sha256"),
            email='admin@springboard.com',
            address_line_1='Admin Address',
            role='admin',
            firstname='Admin',
            lastname='User',
            pincode='123456',
            state='State1',
            city='City1'
        )
        db.session.add(admin_user)

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

        order2 = Order(dummy_user.id, dummy_user.firstname, dummy_user.address_line_1, dummy_user.state, dummy_user.pincode, dummy_user.city, product2.price, "Delivered")
        db.session.add(order2)
        db.session.commit()  # Commit so order2.id is available

        order2item = OrderItems(order2.id, product2.id, dummy_user.id, 12, product2.price)

        db.session.add_all([order1item, order2item])
        db.session.commit()

    def login_admin(self):
        """Log in as the admin user."""
        response = self.client.post('/login', data=dict(
            email="admin@springboard.com",
            password="123"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_show_chart1(self):
        """Test the 'New & Returning Customers' chart."""
        self.login_admin()

        response = self.client.get('/admin/stats')

        # Check for the chart heading and "View Chart" button
        self.assertIn(b'New & Returning Customers', response.data)
        self.assertIn(b'View Chart', response.data)

    def test_show_chart2(self):
        """Test the 'Revenue Over Time' chart."""
        self.login_admin()
        response = self.client.get('/admin/stats')
        
        # Check for the chart heading and "View Chart" button
        self.assertIn(b'Revenue Over Time', response.data)
        self.assertIn(b'View Chart', response.data)

    def test_show_chart3(self):
        """Test the 'Order Status Distribution' chart."""
        self.login_admin()
        response = self.client.get('/admin/stats')
        
        # Check for the chart heading and "View Chart" button
        self.assertIn(b'Order Status', response.data)
        self.assertIn(b'View Chart', response.data)

    def test_show_chart4(self):
        """Test the 'Inventory Stock Levels' chart."""
        self.login_admin()
        response = self.client.get('/admin/stats')
        
        # Check for the chart heading and "View Chart" button
        self.assertIn(b'Inventory Stock Levels', response.data)
        self.assertIn(b'View Chart', response.data)

    def test_show_chart5(self):
        """Test the 'Financial Overview' chart."""
        self.login_admin()
        response = self.client.get('/admin/stats')
        
        # Check for the chart heading and "View Chart" button
        self.assertIn(b'Financial Overview', response.data)
        self.assertIn(b'View Chart', response.data)

    def test_show_chart6(self):
        """Test the 'User Types Distribution' chart."""
        self.login_admin()
        response = self.client.get('/admin/stats')
        
        # Check for the chart heading and "View Chart" button
        self.assertIn(b'User Types Distribution', response.data)
        self.assertIn(b'View Chart', response.data)

    def test_show_chart7(self):
        """Test the 'Order Location Relation' chart."""
        self.login_admin()
        response = self.client.get('/admin/stats')
        print(response.location) 
        
        # Check for the chart heading and "View Chart" button
        self.assertIn(b'Order Location Relation', response.data)
        self.assertIn(b'View Chart', response.data)

    def test_get_stock_chart(self):
        """Test the '/get-stock-chart/<category>' endpoint."""
        self.login_admin()
        response = self.client.get('/admin/get-stock-chart/Category1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Product A', response.data)

if __name__ == '__main__':
    unittest.main()
