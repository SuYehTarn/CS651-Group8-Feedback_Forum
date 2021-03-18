"""Module of the feedback model
"""

import uuid
from sqlalchemy.orm import synonym
from app import db


class Feedback(db.Model):
    """The Feedback model"""
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    _email = db.Column(db.String(length=64), index=True)
    _title = db.Column(db.Unicode(128))
    content = db.Column(db.UnicodeText)
    _token = db.Column(db.String(64), unique=True, index=True)
    response = db.Column(db.UnicodeText)
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
