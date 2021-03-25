"""The unittest module for the admin blueprint.
"""

import unittest
from urllib.parse import urlparse

from app import create_app, db
from app.models.feedback import Feedback
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

        # create some feedbacks for testing
        self.test_info = [{
            'email': f'test{i}@email.com',
            'title': f'title{i}',
            'content': f'some content{i}',
        } for i in range(5)]

        for info in self.test_info:
            db.session.add(Feedback(**info))
            db.session.commit()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_review_all_feedback_page(self) -> None:
        """Test for the route /admin/"""

        # login administrator and save the session
        with self.client as client:
            client.post('/login/', data={
                'name': 'admin',
                'password': 'admin',
            })

        response = self.client.get('/admin')
        self.assertTrue(response.status_code - 300 in range(0, 100),
                        'miss of redirection')

        for url in ['/admin', '/admin/']:
            response = self.client.get(url,
                                       follow_redirects=True)
            self.assertEqual(response.status_code, 200,
                             'wrong status code')
            text = response.get_data(as_text=True)
            for info in self.test_info:
                self.assertTrue(info['title'] in text,
                                f'feedback not found: {info["title"]}')

    def test_review_a_feedback(self) -> None:
        """Test for the route /admin/<feedback_id>"""

        # login administrator and save the session
        with self.client as client:
            client.post('/login/', data={
                'name': 'admin',
                'password': 'admin',
            })

        feedbacks = db.session.query(Feedback).all()
        for feedback in feedbacks:
            response = self.client.get(f'/admin/{feedback.id}')
            text = response.get_data(as_text=True)
            self.assertTrue(feedback.title in text,
                            ('cannot find the correct '
                             'feedback title in the response'))
            self.assertTrue(feedback.content in text,
                            ('cannot find the correct '
                             'feedback content in the response'))

        # test for the wrong id
        existed_id = [feedback.id for feedback in feedbacks]
        id_not_exists = 0
        while id_not_exists in existed_id:
            id_not_exists += len(existed_id)

        response = self.client.get(f'/admin/{id_not_exists}')
        self.assertTrue(response.status_code - 300 in range(0, 100),
                        'wrong http status code')

        url = urlparse(response.location)
        self.assertTrue(url.path in ('/admin/', '/admin'),
                        'wrong routing')
