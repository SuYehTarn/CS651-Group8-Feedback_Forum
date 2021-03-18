"""The unittest module for Administrator model.
"""

import unittest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError
from app import create_app, db
from app.models.administrator import Administrator


class AdministratorModelTestCase(unittest.TestCase):
    """The test class for Administrator model"""

    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # create an Administrator for testing
        self.test_info = {
            'name': 'test',
            'password': 'test password',
        }
        db.session.add(Administrator(**self.test_info))
        db.session.commit()
        self.admin_in_db = db.session.query(Administrator) \
            .filter_by(name=self.test_info['name']).first()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_id_auto_set(self) -> None:
        """Test of id auto-setting"""
        self.assertIsNotNone(self.admin_in_db.id)

    def test_id_auto_increment(self) -> None:
        """Test of id auto-incrementing"""
        old_id = self.admin_in_db.id
        for i in range(5):
            name = f'test{i}'
            db.session.add(Administrator(name=name))
            db.session.commit()
            new_id = db.session.query(Administrator) \
                .filter_by(name=name).first().id
            self.assertEqual(old_id + 1, new_id)
            old_id = new_id

    def test_id_is_unique(self) -> None:
        """Test of id uniqueness"""
        db.session.add(Administrator(id=self.admin_in_db.id))
        with self.assertRaises(FlushError):
            db.session.commit()

    def test_name_can_set(self) -> None:
        """Test of setting name"""
        self.assertEqual(self.test_info['name'],
                         self.admin_in_db.name)

    def test_name_unique(self) -> None:
        """Test of name uniqueness"""
        db.session.add(Administrator(**self.test_info))
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_name_len_limit(self) -> None:
        """Test of name length restriction"""
        name = 'test' * 64
        with self.assertRaises(ValueError):
            Administrator(name=name)

    def test_password_setter(self) -> None:
        """Test of setting password"""
        self.assertTrue(self.admin_in_db.password_hash is not None)

    def test_password_inaccessible(self) -> None:
        """Test of password inaccessibility"""
        with self.assertRaises(AttributeError):
            _password = self.admin_in_db.password

    def test_password_verification(self) -> None:
        """Test of verifying password"""
        self.assertTrue(
            self.admin_in_db.verify_password(
                self.test_info['password']))
        self.assertFalse(self.admin_in_db.verify_password('wrong'))

    def test_password_hash_is_unique(self) -> None:
        """Test of password hash uniqueness"""
        same_password_admin = Administrator(
            password=self.test_info['password'])
        self.assertNotEqual(same_password_admin.password_hash,
                            self.admin_in_db.password_hash)
