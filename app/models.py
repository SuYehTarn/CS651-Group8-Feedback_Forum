"""Module of the database models
"""
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import synonym
from app import db


class Feedback(db.Model):
    """The Feedback model"""
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    _email = db.Column(db.String(length=64), unique=True, index=True)
    _title = db.Column(db.Unicode(128))
    content = db.Column(db.UnicodeText)
    _token = db.Column(db.String(64), unique=True, index=True)
    review_status_id = db.Column(db.Integer, db.ForeignKey('reviewStatuses.id'))
    reviewer_id = db.Column(db.Integer, db.ForeignKey('administrators.id'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = None

    @property
    def email(self) -> str:
        """The email getter"""
        return self._email

    @email.setter
    def email(self, email) -> None:
        """The email setter"""
        if len(email) > 64:
            raise ValueError('exceed the email length limit of 64.')
        self._email = email

    email = synonym('_email', descriptor=email)

    @property
    def title(self) -> str:
        """The title getter"""
        return self._title

    @title.setter
    def title(self, title) -> None:
        if len(title) > 64:
            raise ValueError('exceed the title length limit of 128.')
        self._title = title

    title = synonym('_title', descriptor=title)

    @property
    def token(self) -> bytes:
        """The token getter"""
        return self._token

    @token.setter
    def token(self, _data=None) -> None:
        self._token = uuid.uuid4().bytes
        assert len(self._token) <= 64, 'exceed the token length limit of 64.'

    token = synonym('_token', descriptor=token)

    def __repr__(self) -> str:
        return f'<Feedback {self.id}>'


class ReviewStatus(db.Model):
    """The ReviewStatus model"""
    __tablename__ = 'reviewStatuses'
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(64), unique=True)
    feedbacks = db.relationship('Feedback', backref='reviewStatus')

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

    def __repr__(self) -> str:
        return f'<ReviewStatus {self.name}>'


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
