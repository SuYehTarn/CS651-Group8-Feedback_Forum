"""The unittest module for Main blueprint
"""

import unittest
from urllib.parse import urlparse
from flask import escape

from app import create_app, db
from app.models.feedback import Feedback
from app.models.review_status import ReviewStatus


class MainBlueprintTestCase(unittest.TestCase):
    """The test class for Main blueprint"""

    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        ReviewStatus.insert_review_status()
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

    def test_client_check_feedback_with_token(self) -> None:
        """Test of checking feedback with the token"""
        feedback_data = {
            'email': 'test@gmail.com',
            'title': 'This is the test title',
            'content': 'This is the test content',
            'response': 'The response content',
            'review_status_id': 2
        }
        db.session.add(Feedback(**feedback_data))
        db.session.commit()
        feedback_in_db = db.session.query(Feedback) \
            .filter_by(**feedback_data).first()

        # post token to check feedback
        token = feedback_in_db.token
        response = self.client.post('/check/', data={'token': token})

        status = ReviewStatus.query \
            .filter_by(id=feedback_data['review_status_id']).first()
        text = response.get_data(as_text=True)

        # assure the check page return the expected information
        self.assertTrue(response.status_code - 200 in range(0, 100),
                        ('wrong status code. Expect 2XX, '
                         f'got {response.status_code}'))
        self.assertTrue(feedback_data['email'] in text,
                        'email not found')
        self.assertTrue(feedback_data['title'] in text,
                        'title not found')
        self.assertTrue(feedback_data['content'] in text,
                        'content not found')
        self.assertTrue(feedback_data['response'] in text,
                        'wrong response')
        self.assertTrue(status.name in text,
                        'wrong review status')

    def test_check_feedback_with_wrong_token(self) -> None:
        """Test check feedback with wrong token"""
        feedback_data = {
            'email': 'test@gmail.com',
            'title': 'This is the test title',
            'content': 'This is the test content',
            'response': 'The response content',
            'review_status_id': 2
        }
        db.session.add(Feedback(**feedback_data))
        db.session.commit()
        feedback_in_db = db.session.query(Feedback) \
            .filter_by(**feedback_data).first()
        token = feedback_in_db.token
        wrong_token = token[:-1]
        response = self.client.post('/check/',
                                    data={'token': wrong_token})
        self.assertEqual(200, response.status_code)
        text = response.get_data(as_text=True)
        self.assertTrue('Feedback not found.' in text,
                        'warning message not found')
