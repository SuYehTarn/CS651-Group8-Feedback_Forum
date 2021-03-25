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

        # check the content of each feedback
        for feedback in feedbacks:
            response = self.client.get(f'/admin/{feedback.id}')
            text = response.get_data(as_text=True)
            self.assertTrue(str(feedback.id) in text,
                            ('cannot find the correct '
                             'feedback id in the response'))
            self.assertTrue(feedback.title in text,
                            ('cannot find the correct '
                             'feedback title in the response'))
            self.assertTrue(feedback.content in text,
                            ('cannot find the correct '
                             'feedback content in the response'))
            status = ReviewStatus.query \
                .filter_by(id=feedback.review_status_id).first()
            self.assertTrue(status.name in text,
                            ('cannot find the correct '
                             'review status name in the response'))
            if feedback.response:
                self.assertTrue(feedback.response in text,
                                ('cannot find the correct '
                                 'admin response in the response'))

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

    def test_reply_to_a_feedback(self) -> None:
        """Test for the POST method to the route /admin/<feedback_id>"""

        # login administrator and save the session
        with self.client as client:
            client.post('/login/', data={
                'name': 'admin',
                'password': 'admin',
            })

        review_status = ReviewStatus.query.all()
        data_list = [{
            'review_status': status.id,
            'response': f'response{status.id}',
        } for status in review_status]
        feedbacks = Feedback.query.all()[:len(data_list)]

        # post the response and review statuses
        for data, feedback in zip(data_list, feedbacks):
            self.client.post(f'/admin/{feedback.id}',
                             data=data)

            # check if the database is modified as expectation
            feedback_in_db = Feedback.query \
                .filter_by(id=feedback.id).first()
            self.assertEqual(data['response'],
                             feedback_in_db.response,
                             'response not correct')
            self.assertEqual(data['review_status'],
                             feedback_in_db.review_status_id,
                             'review status not correct')

            # check if the view is renewed
            response = self.client.get(f'/admin/{feedback.id}')
            text = response.get_data(as_text=True)
            status = ReviewStatus.query \
                .filter_by(id=data['review_status']).first()
            self.assertTrue(status.name in text,
                            ('cannot find the correct '
                             'review status name in the response'))
            self.assertTrue(data['response'] in text,
                            ('cannot find the correct '
                             'admin response in the response'))
