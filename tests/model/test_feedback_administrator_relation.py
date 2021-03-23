"""The unittest module for model relations.
"""

import unittest
from app import create_app, db
from app.models.administrator import Administrator
from app.models.feedback import Feedback
from app.models.review_status import ReviewStatus


class ModelRelationTestCase(unittest.TestCase):
    """The test class for model relations"""

    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # create a administrator
        reviewer_name = 'admin'
        admin = Administrator(name=reviewer_name)
        db.session.add(admin)
        db.session.commit()
        self.reviewer_in_db = db.session.query(Administrator)\
            .filter_by(name=reviewer_name).first()

        # create a admin status
        status_name = 'status'
        review_status = ReviewStatus(name=status_name)
        db.session.add(review_status)
        db.session.commit()
        self.review_status_in_db = db.session.query(ReviewStatus) \
            .filter_by(name=status_name).first()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_feedback_can_set_reference(self) -> None:
        """Test of setting reviewer for a feedback"""
        email = 'test@email.com'
        feedback = Feedback(email=email,
                            reviewer_id=self.reviewer_in_db.id,
                            review_status_id=self.review_status_in_db.id)
        db.session.add(feedback)
        db.session.commit()
        feedback_in_db = db.session.query(Feedback)\
            .filter_by(email=email).first()

        self.assertEqual(feedback_in_db.reviewer_id,
                         self.reviewer_in_db.id,
                         'fail to refer a reviewer for a feedback')

        self.assertEqual(feedback_in_db.review_status_id,
                         self.review_status_in_db.id,
                         'fail to refer a admin status for a feedback')

    def test_link_all_feedbacks(self) -> None:
        """Test of access all feedbacks reviewed by a administrator"""
        for _ in range(5):
            feedback = Feedback(reviewer_id=self.reviewer_in_db.id,
                                review_status_id=self.review_status_in_db.id)
            db.session.add(feedback)
            db.session.commit()

        feedback_ids_in_db = [f.id for f in db.session.query(Feedback).all()]

        related_feedback_ids = [f.id for f in self.reviewer_in_db.feedbacks]
        self.assertEqual(set(feedback_ids_in_db),
                         set(related_feedback_ids),
                         'the related feedbacks not correct for a administrator')

        related_feedback_ids = [f.id for f in self.review_status_in_db.feedbacks]
        self.assertEqual(set(feedback_ids_in_db),
                         set(related_feedback_ids),
                         'the related feedbacks not correct for a admin status')
