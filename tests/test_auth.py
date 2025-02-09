import unittest
from flask_testing import TestCase
from main import create_app, db, models
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from app.models import User

class TestSignupPage(TestCase):
    def create_app(self):
        app = create_app(config_class="TestConfig")
        return app
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_signup_page_loads(self):
        """Test if the signup page loads correctly."""
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Signup Page", response.data)

    def test_signup_form_elements_present(self):
        """Test if the signup form contains all required elements."""
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'name="firstname"', response.data)
        self.assertIn(b'name="lastname"', response.data)
        self.assertIn(b'name="email"', response.data)
        self.assertIn(b'name="password"', response.data)
        self.assertIn(b'name="confirm_password"', response.data)
        self.assertIn(b'name="address_line_1"', response.data)
        self.assertIn(b'name="state"', response.data)
        self.assertIn(b'name="city"', response.data)
        self.assertIn(b'name="role"', response.data)
        self.assertIn(b'name="pincode"', response.data)

    def test_error_message_display(self):
        """Test if error messages are displayed for invalid input."""
        response = self.client.post('/signup', data={
            'firstname': '',  # Missing first name
            'lastname': 'User',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'address_line_1': '123 Test St',
            'state': 'Uttarakhand',
            'city': 'Dehradun',
            'pincode': '123456',
            'role': 'user'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This field is required.', response.data)

    def test_signup_password_mismatch(self):
        """Test if error message appears for password mismatch."""
        response = self.client.post('/signup', data={
            'firstname': 'Test',
            'lastname': 'User',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'wrongpassword',  # Mismatched password
            'address_line_1': '123 Test St',
            'state': 'Uttarakhand',
            'city': 'Dehradun',
            'pincode': '123456',
            'role': 'user'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Field must be equal to password.', response.data)

    def test_signup_email_already_exists(self):
        """Test if error message appears when email already exists."""
        # First, create a user with the same email
        try:
            existing_user = models.User(
                firstname="Existing",
                lastname="User",
                email="test@example.com",
                password=generate_password_hash("password123", method='pbkdf2:sha256'),
                address_line_1="123 Test St",
                state="Uttarakhand",
                city="Dehradun",
                role="user",
                pincode="123456"
            )
            db.session.add(existing_user)
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            self.assertTrue(True, "saved to save data from database")

        #retry to save the data
        try:
            existing_user = models.User(
                firstname="Existing",
                lastname="User",
                email="test@example.com",
                password=generate_password_hash("password123", method='pbkdf2:sha256'),
                address_line_1="123 Test St",
                state="Uttarakhand",
                city="Dehradun",
                role="user",
                pincode="123456"
            )
            db.session.add(existing_user)
            db.session.commit()
            self.assertTrue(False, "save data into database")

        except IntegrityError:
            db.session.rollback()
            self.assertTrue(True, "saved to save data from database")
        
        self.assertTrue(existing_user, "User created successfully")

class TestLogin(TestCase):
    def create_app(self):
        app = create_app(config_class="TestConfig")
        return app

    def setUp(self):
        db.create_all()

        # Create a test user
        hashed_password = generate_password_hash("password")
        try:
            user = models.User(
                firstname="Test",
                lastname="User",
                email="test@example.com",
                address_line_1="123 Test St",
                state="Uttarakhand",
                city="Dehradun",
                role="user",
                pincode="123456",
                password=hashed_password
            )
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login Page", response.data)
    
    def test_login(self):
        """Test user login."""
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'StyleVerse - Home', response.data)

    def test_empty_email_and_password(self):
        """Test submitting empty email and password."""
        response = self.client.post('/login', data={
            'email': '',
            'password': ''
        }, follow_redirects=True)

        # Check that the form validation fails
        self.assertIn(b'This field is required.', response.data)
        self.assertEqual(response.status_code, 200)

    def test_login_redirect_when_authenticated(self):
        """Test that a user cannot access the login page if already logged in."""
        self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        })

        # Try accessing the login page again
        response = self.client.get('/login', follow_redirects=True)

        # Check that the user is redirected to home page
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)
            
class TestForgetPassword(TestCase):
    def create_app(self):
        app = create_app(config_class="TestConfig")
        return app

    def setUp(self):
        db.create_all()

        # Create a test user
        try:
            user = models.User(
                firstname="Test",
                lastname="User",
                email="test@example.com",
                password=generate_password_hash("password123", method='pbkdf2:sha256'),
                address_line_1="123 Test St",
                state="Uttarakhand",
                city="Dehradun",
                role="user",
                pincode="123456"
            )
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_forgetpassword_page_loads(self):
        """Test if the forget password page loads correctly."""
        response = self.client.get('/forgetpassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Forgot Password", response.data)

    def test_forgetpassword_form_empty_email(self):
        """Test submitting the form with an empty email field."""
        response = self.client.post('/forgetpassword', data={'email': ''})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This field is required.", response.data)  # Assuming this is the error message for empty email

    def test_forgetpassword_form_invalid_email(self):
        """Test submitting the form with an invalid email format."""
        response = self.client.post('/forgetpassword', data={'email': 'invalid-email'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid email address.", response.data)  # Assuming this is the error message for invalid email



class UserRoleTestCase(TestCase):
    def create_app(self):
        app = create_app(config_class="TestConfig")
        return app

    def setUp(self):
        # Create tables and a sample dataset
        db.create_all()
        self.add_sample_users()

    def tearDown(self):
        # Drop all tables after each test
        db.session.remove()
        db.drop_all()

    def add_sample_users(self):
        """Add sample users to the test database"""
        admin_user = User(
            password='admin123',
            email='admin@springboard.com',
            address_line_1='Admin Address',
            role='admin',
            firstname='Admin',
            lastname='User',
            pincode='123456',
            state='State1',
            city='City1'
        )
        normal_user = User(
            password='user123',
            email='user@example.com',
            address_line_1='User Address',
            role='user',
            firstname='Normal',
            lastname='User',
            pincode='654321',
            state='State2',
            city='City2'
        )
        delivery_user = User(
            password='delivery123',
            email='delivery@example.com',
            address_line_1='Delivery Address',
            role='delivery',
            firstname='Delivery',
            lastname='Person',
            pincode='789101',
            state='State3',
            city='City3'
        )
        delivery_user.approved = True
        db.session.add(admin_user)
        db.session.add(normal_user)
        db.session.add(delivery_user)
        db.session.commit()

    def test_is_admin(self):
        """Test the isAdmin method"""
        admin_user = User.query.filter_by(email='admin@springboard.com').first()
        assert admin_user.isAdmin() is True

    def test_is_delivery_person(self):
        """Test the isDeliveryPerson method"""
        delivery_user = User.query.filter_by(email='delivery@example.com').first()
        assert delivery_user.isDeliveryPerson() is True

    def test_is_not_delivery_person(self):
        """Ensure unapproved delivery person is not identified as delivery person"""
        unapproved_user = User(
            password='unapproved123',
            email='unapproved@example.com',
            address_line_1='Unapproved Address',
            role='delivery',
            firstname='Unapproved',
            lastname='Person',
            pincode='111111',
            state='State4',
            city='City4'
        )
        db.session.add(unapproved_user)
        db.session.commit()
        assert unapproved_user.isDeliveryPerson() is False

    def test_is_normal_user(self):
        """Test that a normal user is not identified as admin or delivery person"""
        normal_user = User.query.filter_by(email='user@example.com').first()
        assert normal_user.isAdmin() is False
        assert normal_user.isDeliveryPerson() is False

if __name__ == '__main__':
    unittest.main()

