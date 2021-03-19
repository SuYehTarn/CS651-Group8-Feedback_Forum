"""The unittest module for Feedback model.
"""

import unittest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError
from app import create_app, db
from app.models.feedback import Feedback


class FeedbackModelTestCase(unittest.TestCase):
    """The test class for Feedback model"""

    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # create an Feedback for testing
        self.test_info = {
            'email': 'test@email.com',
            'title': 'this is title',
            'content': u'this is content',
        }
        self.test_feedback = Feedback(**self.test_info)
        db.session.add(self.test_feedback)
        db.session.commit()
        self.test_feedback_in_db = db.session.query(Feedback) \
            .filter_by(email=self.test_feedback.email).first()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_id_auto_set(self) -> None:
        """Test of id auto-setting"""
        self.assertIsNotNone(self.test_feedback.id)

    def test_id_auto_increment(self) -> None:
        """Test of id auto-incrementing"""
        old_id = self.test_feedback.id
        emails = [f'test{i}@email.com' for i in range(5)]
        feedbacks = [Feedback(email=email) for email in emails]
        for feedback in feedbacks:
            db.session.add(feedback)
            db.session.commit()
            new_id = db.session.query(Feedback) \
                .filter_by(email=feedback.email).first().id
            self.assertEqual(old_id + 1, new_id)
            old_id = new_id

    def test_id_is_unique(self) -> None:
        """Test of id uniqueness"""
        same_id = Feedback(id=self.test_feedback_in_db.id)
        db.session.add(same_id)
        with self.assertRaises(FlushError):
            db.session.commit()

    def test_email_can_set(self) -> None:
        """Test of setting email"""
        self.assertEqual(self.test_feedback.email,
                         self.test_feedback_in_db.email)

    def test_email_len_limit(self) -> None:
        """Test of email length restriction"""
        email = 'test@email.com' + 'n' * 64
        with self.assertRaises(ValueError):
            Feedback(email=email)

    def test_title_can_be_set(self) -> None:
        """Test of setting title"""
        self.assertEqual(self.test_feedback.title,
                         self.test_feedback_in_db.title)

    def test_title_len_limit(self) -> None:
        """Test of title length restriction"""
        title = 'n' * 129
        with self.assertRaises(ValueError):
            Feedback(title=title)

    def test_content_can_be_set(self) -> None:
        """Test of setting content"""
        self.assertEqual(self.test_feedback.content,
                         self.test_feedback_in_db.content)

    def test_response_is_initially_empty(self) -> None:
        """Test of the blankness of the response
        when a feedback is initially created.
        """
        self.assertIsNone(self.test_feedback_in_db.response)

    def test_response_can_be_set(self) -> None:
        """Test of setting response"""
        self.assertIsNone(self.test_feedback_in_db.response)
        response = 'some response'
        db.session.query(Feedback) \
            .filter_by(email=self.test_feedback.email) \
            .update({'response': response},
                    synchronize_session="fetch")
        self.assertEqual(self.test_feedback_in_db.response,
                         response)

    def test_token_auto_set(self) -> None:
        """Test of the token auto-setting"""
        self.assertIsNotNone(self.test_feedback_in_db.token)

    def test_token_is_unique(self) -> None:
        """Test of the uniqueness of the token"""
        email = 'test2@email.com'
        feedback = Feedback(email=email)
        db.session.add(feedback)
        db.session.commit()
        with self.assertRaises(IntegrityError):
            db.session.query(Feedback) \
                .filter_by(email=email) \
                .update({'token': self.test_feedback_in_db.token})

    def test_review_status_default_one(self) -> None:
        """Test of the default value of review status"""
        self.assertEqual(1, self.test_feedback_in_db.review_status_id)
