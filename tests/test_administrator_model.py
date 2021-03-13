"""The unittest module for Administrator model.
"""

import unittest
from sqlalchemy.exc import IntegrityError
from app import create_app, db
from app.models import Administrator


class AdministratorModelTestCase(unittest.TestCase):
    """The test class for Administrator model"""

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
        db.session.add(Administrator(name=name))
        db.session.commit()
        target = db.session.query(Administrator) \
            .filter_by(name=name).first()
        self.assertIsNotNone(target.id)

    def test_id_auto_increment(self) -> None:
        """Test of id auto-incrementing"""
        old_id = None
        for i in range(5):
            name = f'test{i}'
            db.session.add(Administrator(name=name))
            db.session.commit()
            new_id = db.session.query(Administrator) \
                .filter_by(name=name).first().id
            if i > 0:
                self.assertEqual(old_id + 1, new_id)
            old_id = new_id

    def test_id_is_unique(self) -> None:
        """Test of id uniqueness"""
        name = 'test'
        db.session.add(Administrator(name=name))
        db.session.commit()
        target_id = db.session.query(Administrator) \
            .filter_by(name=name).first().id
        db.session.add(Administrator(id=target_id))
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_name_can_set(self) -> None:
        """Test of setting name"""
        name = 'test'
        db.session.add(Administrator(name=name))
        db.session.commit()
        admin_in_db = db.session.query(Administrator)\
            .filter_by(name=name).first()
        self.assertEqual(name, admin_in_db.name)

    def test_name_unique(self) -> None:
        """Test of name uniqueness"""
        name = 'test'
        db.session.add_all([Administrator(name=name),
                            Administrator(name=name)])
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_name_len_limit(self) -> None:
        """Test of name length restriction"""
        name = 'test' * 64
        with self.assertRaises(ValueError):
            Administrator(name=name)

    def test_password_setter(self) -> None:
        """Test of setting password"""
        admin = Administrator(password='test')
        self.assertTrue(admin.password_hash is not None)

    def test_password_inaccessible(self) -> None:
        """Test of password inaccessibility"""
        admin = Administrator(password='test')
        with self.assertRaises(AttributeError):
            _password = admin.password

    def test_password_verification(self) -> None:
        """Test of verifying password"""
        admin = Administrator(password='test')
        self.assertTrue(admin.verify_password('test'))
        self.assertFalse(admin.verify_password('wrong'))

    def test_password_hash_is_unique(self) -> None:
        """Test of password hash uniqueness"""
        admin1 = Administrator(password='test')
        admin2 = Administrator(password='test')
        self.assertNotEqual(admin1.password_hash,
                            admin2.password_hash)
