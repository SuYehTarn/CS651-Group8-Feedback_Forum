"""The unittest module for Feedback model.
"""

import unittest
from sqlalchemy.exc import IntegrityError
from app import create_app, db
from app.models.feedback import Feedback


class FeedbackModelTestCase(unittest.TestCase):
    """The test class for Feedback model"""

    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_id_auto_set(self) -> None:
        """Test of id auto-setting"""
        email = 'test@email.com'
        db.session.add(Feedback(email=email))
        db.session.commit()
        feedback = db.session.query(Feedback) \
            .filter_by(email=email).first()
        self.assertIsNotNone(feedback.id)

    def test_id_auto_increment(self) -> None:
        """Test of id auto-incrementing"""
        old_id = None
        for i in range(5):
            email = f'test{i}@email.com'
            db.session.add(Feedback(email=email))
            db.session.commit()
            new_id = db.session.query(Feedback) \
                .filter_by(email=email).first().id
            if i > 0:
                self.assertEqual(old_id + 1, new_id)
            old_id = new_id

    def test_id_is_unique(self) -> None:
        """Test of id uniqueness"""
        email = 'test@email.com'
        db.session.add(Feedback(email=email))
        db.session.commit()
        target_id = db.session.query(Feedback) \
            .filter_by(email=email).first().id
        db.session.add(Feedback(id=target_id))
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_email_can_set(self) -> None:
        """Test of setting email"""
        email = 'test@email.com'
        feedback = Feedback(email=email)
        db.session.add(feedback)
        db.session.commit()
        feedback_in_db = db.session.query(Feedback) \
            .filter_by(email=email).first()
        self.assertEqual(feedback.email, feedback_in_db.email)

    def test_email_unique(self) -> None:
        """Test of email uniqueness"""
        email = 'test@email.com'
        db.session.add_all([Feedback(email=email),
                            Feedback(email=email)])
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_email_len_limit(self) -> None:
        """Test of email length restriction"""
        email = 'test@email.com' + 'n' * 64
        with self.assertRaises(ValueError):
            Feedback(email=email)

    def test_title_can_set(self) -> None:
        """Test of setting title"""
        title = 'this is title'
        feedback = Feedback(title=title)
        db.session.add(feedback)
        db.session.commit()
        feedback_in_db = db.session.query(Feedback) \
            .filter_by(title=title).first()
        self.assertEqual(feedback.title, feedback_in_db.title)

    def test_title_len_limit(self) -> None:
        """Test of title length restriction"""
        title = 'n' * 129
        with self.assertRaises(ValueError):
            Feedback(title=title)

    def test_content_can_set(self) -> None:
        """Test of setting content"""
        content = u'this is content'
        feedback = Feedback(content=content)
        db.session.add(feedback)
        db.session.commit()
        feedback_in_db = db.session.query(Feedback) \
            .filter_by(content=content).first()
        self.assertEqual(feedback.content, feedback_in_db.content)
