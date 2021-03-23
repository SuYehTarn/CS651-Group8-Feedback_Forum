"""The unittest module for Main blueprint
"""

import unittest
from urllib.parse import urlparse
from flask import escape

from app import create_app, db
from app.models.feedback import Feedback


class MainBlueprintTestCase(unittest.TestCase):
    """The test class for Main blueprint"""

    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_client_provide_feedback(self) -> None:
        """Test of client providing a feedback"""
        feedback_data = {
            'email': 'test@gmail.com',
            'title': 'This is the test title',
            'content': 'This is the test content',
        }
        data = {'submit': 'Submit'}
        data.update(feedback_data)
        response = self.client.post('/', data=data,
                                    follow_redirects=True)
        self.assertEqual(200, response.status_code)

        feedback_in_db = db.session.query(Feedback) \
            .filter_by(**feedback_data).first()
        self.assertEqual(data['email'], feedback_in_db.email)
        self.assertEqual(data['title'], feedback_in_db.title)
        self.assertEqual(data['content'], feedback_in_db.content)

        text = response.get_data(as_text=True)
        token = escape(str(feedback_in_db.token))
        self.assertTrue(token in text)

        url = urlparse(response.location)
        self.assertEqual(b'', url.path)
