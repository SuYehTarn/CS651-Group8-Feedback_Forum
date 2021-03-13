"""The unittest module for ReviewStatus model.
"""

import unittest
from sqlalchemy.exc import IntegrityError
from app import create_app, db
from app.models import ReviewStatus


class ReviewStatusModelTestCase(unittest.TestCase):
    """The test class for ReviewStatus model"""

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
        name = 'test'
        db.session.add(ReviewStatus(name=name))
        db.session.commit()
        target = db.session.query(ReviewStatus) \
            .filter_by(name=name).first()
        self.assertIsNotNone(target.id)

    def test_id_auto_increment(self) -> None:
        """Test of id auto-incrementing"""
        old_id = None
        for i in range(5):
            name = f'test{i}'
            db.session.add(ReviewStatus(name=name))
            db.session.commit()
            new_id = db.session.query(ReviewStatus) \
                .filter_by(name=name).first().id
            if i > 0:
                self.assertEqual(old_id + 1, new_id)
            old_id = new_id

    def test_id_is_unique(self) -> None:
        """Test of id uniqueness"""
        name = 'test'
        db.session.add(ReviewStatus(name=name))
        db.session.commit()
        target_id = db.session.query(ReviewStatus) \
            .filter_by(name=name).first().id
        db.session.add(ReviewStatus(id=target_id))
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_name_can_set(self) -> None:
        """Test of setting name"""
        name = 'test'
        review_status = ReviewStatus(name=name)
        db.session.add(review_status)
        db.session.commit()
        review_status_in_db = db.session.query(ReviewStatus) \
            .filter_by(name=name).first()
        self.assertEqual(review_status.name, review_status_in_db.name)

    def test_name_unique(self) -> None:
        """Test of name uniqueness"""
        name = 'test'
        db.session.add_all([ReviewStatus(name=name),
                            ReviewStatus(name=name)])
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_name_len_limit(self) -> None:
        """Test of name length restriction"""
        name = 'test' * 64
        with self.assertRaises(ValueError):
            ReviewStatus(name=name)
