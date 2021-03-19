"""Module of the administrator model
"""

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import synonym
from sqlalchemy.orm.exc import FlushError
from flask_login import UserMixin

from app import db, login_manager


@login_manager.user_loader
def load_admin(admin_id):
    """Load the specified administrator from the database"""
    return Administrator.query.get(int(admin_id))


class Administrator(UserMixin, db.Model):
    """The Administrator model"""
    __tablename__ = 'administrators'
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    feedbacks = db.relationship('Feedback', backref='reviewer')

    @property
    def name(self) -> str:
        """The name getter"""
        return self._name

    @name.setter
    def name(self, name) -> None:
        if len(name) > 64:
            raise ValueError('exceed the name length limit of 64.')
        self._name = name

    name = synonym('_name', descriptor=name)

    @property
    def password(self) -> None:
        """The forbidden password getter."""
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password) -> None:
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password) -> bool:
        """The method of verifying password"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f'<Administrator {self.name}>'

    @staticmethod
    def insert_administrator() -> None:
        """Insert default administrator"""
        admin_name = current_app.config.get('ADMIN_NAME')
        admin_password = current_app.config.get('ADMIN_PASSWORD')
        if admin_name is None and admin_password is None:
            print('Missing admin name or password.')
            print('Use default settings.')
            admin_name = 'admin'
            admin_password = 'admin'
        try:
            admin = Administrator(name=admin_name,
                                  password=admin_password)
            db.session.add(admin)
            db.session.commit()
        except (IntegrityError, FlushError) as exc:
            print(exc)
