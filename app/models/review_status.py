"""Module of the review status model
"""

from sqlalchemy.orm import synonym
from app import db


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
