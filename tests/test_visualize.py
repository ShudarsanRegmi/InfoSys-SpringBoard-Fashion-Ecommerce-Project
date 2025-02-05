import unittest
from flask_testing import TestCase
from main import create_app, db
from app.visualization import Visualize
from io import BytesIO

class TestVisualization(TestCase):

    WTF_CSRF_ENABLED = False
    def create_app(self):
        """Configure the Flask app for testing."""
        app = create_app(config_class="TestConfig")
        return app

    def setUp(self):
        """Set up the test """
        db.create_all()

    def tearDown(self):
        """Tear down the test database."""
        db.session.remove()
        db.drop_all()
        
    def test_generate_new_old_customers_graph(self):
        with self.app.app_context():
            dates = ["2024-01-01", "2024-01-02", "2024-01-03"]
            new_customers = [10, 20, 30]
            returning_customers = [5, 10, 15]
            img = Visualize.generate_new_old_customers_graph(dates, new_customers, returning_customers)
            self.assertIsInstance(img, BytesIO)
        
    def test_generate_revenue_overtime_graph(self):
        with self.app.app_context():
            dates = ["2024-01-01", "2024-01-02", "2024-01-03"]
            revenue = [1000, 2000, 3000]
            img = Visualize.generate_revenue_overtime_graph(dates, revenue)
            self.assertIsInstance(img, BytesIO)
        
    def test_generate_order_status_graph(self):
        with self.app.app_context():
            statuses = ["Pending", "Completed", "Cancelled"]
            values = [10, 50, 5]
            img = Visualize.generate_order_status_graph(statuses, values)
            self.assertIsInstance(img, BytesIO)
        
    def test_generate_inventory_stocks_graph(self):
        with self.app.app_context():
            products = ["Product A", "Product B", "Product C"]
            stocks = [50, 30, 20]
            img = Visualize.generate_inventory_stocks_graph(products, stocks)
            self.assertIsInstance(img, BytesIO)
        
    def test_generate_finantial_overview_graph(self):
        with self.app.app_context():
            dates = ["2024-01-01", "2024-01-02", "2024-01-03"]
            expenses = [500, 1000, 1500]
            revenue = [1000, 2000, 3000]
            img = Visualize.generate_finantial_overview_graph(dates, expenses, revenue)
            self.assertIsInstance(img, BytesIO)
        
    def test_user_role_distribution_graph(self):
        with self.app.app_context():
            roles = ["Admin", "Customer", "Vendor"]
            counts = [5, 20, 10]
            img = Visualize.user_role_distribution_graph(roles, counts)
            self.assertIsInstance(img, BytesIO)
        
    def test_generate_state_order_distribution_graph(self):
        with self.app.app_context():
            states = ["State A", "State B", "State C"]
            counts = [100, 200, 150]
            img = Visualize.generate_state_order_distribution_graph(states, counts)
            self.assertIsInstance(img, BytesIO)

if __name__ == "__main__":
    unittest.main()