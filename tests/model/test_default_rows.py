"""The unittest module for the insertion of default rows.
"""

import unittest
from flask import current_app

from app import create_app, db
from app.models.administrator import Administrator
from app.models.review_status import ReviewStatus


class AdminBlueprintTestCase(unittest.TestCase):
    """The test class for the admin blueprint"""

    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_insert_review_status(self) -> None:
        """Test of insertion of default admin statuses"""
        ReviewStatus.insert_review_status()
        review_statuses = db.session.query(ReviewStatus).all()
        self.assertEqual(set(current_app.config.get('REVIEW_STATUSES')),
                         set(status.name for status in review_statuses))

    def test_insert_administrator_default(self) -> None:
        """Test of insertion of default administrator"""
        current_app.config['ADMIN_NAME'] = None
        current_app.config['ADMIN_PASSWORD'] = None
        Administrator.insert_administrator()
        administrator = db.session.query(Administrator).first()
        self.assertEqual('admin', administrator.name)
        self.assertTrue(administrator.verify_password('admin'))

    def test_insert_administrator_config(self) -> None:
        """Test of insertion of administrator by config"""
        name = 'customized_admin_name'
        password = 'customized_admin_password'
        current_app.config['ADMIN_NAME'] = name
        current_app.config['ADMIN_PASSWORD'] = password
        Administrator.insert_administrator()
        administrator = db.session.query(Administrator).first()
        self.assertEqual(name, administrator.name)
        self.assertTrue(administrator.verify_password(password))
