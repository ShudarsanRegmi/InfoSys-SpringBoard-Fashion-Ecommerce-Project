from flask_testing import TestCase
import unittest
from app import create_app  # Assuming `create_app` is a factory function for your app.
from app.models import db, Product, User, CartItem
from werkzeug.security import generate_password_hash

class AdminTestCase(TestCase):
    def create_app(self):
        """Configure the Flask app for testing."""
        app = create_app(config_class="TestConfig")
        return app
    
    def setUp(self):
        """Set up a temporary Flask application and database for testing."""
        with self.app.app_context():
            db.create_all()
            self.add_sample_data()

    def tearDown(self):
        """Tear down the database after each test."""
        with self.app.app_context():
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
        db.session.commit()
    
    def login_admin(self):
        """Log in as the admin user."""
        response = self.client.post('/login', data=dict(
            email="admin@springboard.com",
            password="123"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_add_product(self):
        """Test adding a new product."""
        with self.app.app_context():
            self.login_admin()
            response = self.client.post('admin/product/new', data={
                'name': 'Test Product',
                'price': 19.99,
                'stock_quantity': 10,
                'brand': 'Test Brand',
                'size': 'M',
                'target_user': 'Men',
                'type': 'Shirt',
                'image': 'image_url',
                'description': 'Test product description',
                'details': 'Detailed information about the product.',
                'colour': 'Red',
                'category': 'Clothing',
                'rating': '4.5'
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            product = Product.query.filter_by(name='Test Product').first()
            self.assertIsNotNone(product)
            self.assertEqual(product.price, 19.99)

    def test_update_product(self):
        """Test updating an existing product."""
        with self.app.app_context():
            self.login_admin()
            product = Product(name='Old Product', price=15.00, stock_quantity=5, brand='Old Brand', size='L', 
                              target_user='Women', type='Dress', image='old_image', description='Old description',
                              details='Old details', colour='Blue', category='Clothing', rating='3.0')
            db.session.add(product)
            db.session.commit()

            response = self.client.post(f'/admin/product/edit/{product.id}', data={
                'name': 'Updated Product',
                'price': 20.00,
                'stock_quantity': 8,
                'brand': 'Updated Brand',
                'size': 'XL',
                'target_user': 'Men',
                'type': 'Shirt',
                'image': 'new_image',
                'description': 'Updated description',
                'details': 'Updated details',
                'colour': 'Green',
                'category': 'Clothing'
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            updated_product = Product.query.filter_by(id = product.id).first()
            self.assertEqual(updated_product.name, 'Updated Product')

    def test_delete_product(self):
        """Test deleting a product."""
        with self.app.app_context():
            self.login_admin()
            product = Product(name='To Be Deleted', price=10.00, stock_quantity=3, brand='Brand', size='S',
                              target_user='Women', type='T-shirt', image='image_url', description='To be deleted',
                              details='Product details', colour='Black', category='Clothing', rating='3.5')
            db.session.add(product)
            db.session.commit()

            response = self.client.post(f'/admin/product/delete/{product.id}', follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            deleted_product = Product.query.filter_by(id = product.id).first()
            self.assertIsNone(deleted_product)

    def test_view_products(self):
        """Test viewing all products."""
        with self.app.app_context():
            self.login_admin()
            product1 = Product(name='Product1', price=10.00, stock_quantity=5, brand='Brand1', size='M',
                               target_user='Men', type='Shirt', image='product1_image', description='Product 1 description',
                               details='Details of Product 1', colour='Red', category='Clothing', rating='4.0')
            product2 = Product(name='Product2', price=20.00, stock_quantity=8, brand='Brand2', size='L',
                               target_user='Women', type='Dress', image='product2_image', description='Product 2 description',
                               details='Details of Product 2', colour='Blue', category='Clothing', rating='4.5')
            db.session.add_all([product1, product2])
            db.session.commit()

            response = self.client.get('/admin/products')

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Product1', response.data)
            self.assertIn(b'Product2', response.data)

    
    def test_view_orders(self):
        """Test viewing all orders."""
        self.login_admin()
        response = self.client.get('/admin/view_orders')
        self.assertEqual(response.status_code, 200)

            
if __name__ == '__main__':
    unittest.main()
