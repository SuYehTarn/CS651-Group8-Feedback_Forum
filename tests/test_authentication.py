"""The unittest module for the admin blueprint.
"""

import unittest
from urllib.parse import urlparse
from flask_login import current_user

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
        Administrator.insert_administrator()
        ReviewStatus.insert_review_status()

        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_and_logout_success(self) -> None:
        """Test login with right authentication data"""

        # login administrator and save the session
        with self.client as client:
            response = client.post('/login/', data={
                'name': 'admin',
                'password': 'admin',
            })
            self.assertTrue(current_user.is_authenticated,
                            'authentication failed')
            self.assertTrue(response.status_code - 300 in range(0, 100),
                            'wrong http status code')
            url = urlparse(response.location)
            self.assertTrue(url.path in ['/admin', '/admin/'],
                            f'wrong redirection url: {url.path}')

            response = client.get('/logout/')
            self.assertFalse(current_user.is_authenticated,
                             'fail to logout')
            self.assertTrue(response.status_code - 300 in range(0, 100),
                            'wrong http status code')
            # is None, due to same url
            url = urlparse(response.location)
            self.assertTrue(url.path in ['/', ''],
                            f'wrong redirection url: {response.location}')

    def test_login_fail(self) -> None:
        """Test login with wrong authentication data"""

        # login administrator and save the session
        with self.client as client:
            response = client.post('/login/', data={
                'name': 'wrong',
                'password': 'wrong',
            })
            self.assertFalse(current_user.is_authenticated,
                             'should not able to login')
            self.assertTrue(response.status_code - 200 in range(0, 100),
                            'wrong http status code')
            # is None, due to same url
            self.assertIsNone(response.location,
                              f'wrong redirection url: {response.location}')
