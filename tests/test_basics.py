""""Module of the basic tests
"""
import unittest
from flask import current_app
from app import create_app


class BasicsTestCase(unittest.TestCase):
    """Class of basic tests"""
    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self) -> None:
        self.app_context.pop()

    def test_app_exists(self) -> None:
        """Test of the web app existence"""
        self.assertIsNotNone(current_app)

    def test_app_is_testing(self) -> None:
        """Test of the environment configuration"""
        self.assertIsNotNone(current_app.config['TESTING'])
