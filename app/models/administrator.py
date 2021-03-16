"""Module of the administrator model
"""

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import synonym
from app import db


class Administrator(db.Model):
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
