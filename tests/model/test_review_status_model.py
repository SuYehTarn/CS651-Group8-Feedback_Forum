"""The unittest module for ReviewStatus model.
"""

import unittest
from sqlalchemy.orm.exc import FlushError
from sqlalchemy.exc import IntegrityError
from app import create_app, db
from app.models.review_status import ReviewStatus


class ReviewStatusModelTestCase(unittest.TestCase):
    """The test class for ReviewStatus model"""

    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # create a ReviewStatus for testing
        self.test_info = {
            'name': 'test',
        }
        db.session.add(ReviewStatus(**self.test_info))
        db.session.commit()
        self.test_review_status_in_db = db.session \
            .query(ReviewStatus) \
            .filter_by(name=self.test_info['name']) \
            .first()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_id_auto_set(self) -> None:
        """Test of id auto-setting"""
        self.assertIsNotNone(
            self.test_review_status_in_db.id)

    def test_id_auto_increment(self) -> None:
        """Test of id auto-incrementing"""
        old_id = self.test_review_status_in_db.id
        for i in range(5):
            name = f'test{i}'
            db.session.add(ReviewStatus(name=name))
            db.session.commit()
            new_id = db.session.query(ReviewStatus) \
                .filter_by(name=name).first().id
            self.assertEqual(old_id + 1, new_id)
            old_id = new_id

    def test_id_is_unique(self) -> None:
        """Test of id uniqueness"""
        db.session.add(ReviewStatus(
            id=self.test_review_status_in_db.id))
        with self.assertRaises(FlushError):
            db.session.commit()

    def test_name_can_set(self) -> None:
        """Test of setting name"""
        self.assertEqual(self.test_info['name'],
                         self.test_review_status_in_db.name)

    def test_name_unique(self) -> None:
        """Test of name uniqueness"""
        db.session.add(
            ReviewStatus(name=self.test_info['name']))
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_name_len_limit(self) -> None:
        """Test of name length restriction"""
        name = 'test' * 64
        with self.assertRaises(ValueError):
            ReviewStatus(name=name)
