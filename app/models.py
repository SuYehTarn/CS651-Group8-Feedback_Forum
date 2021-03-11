from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    title = db.Column(db.Unicode(128))
    content = db.Column(db.UnicodeText)
    token = db.Column(db.String(128), unique=True, index=True)
    review_status_id = db.Column(db.Integer, db.ForeignKey('reviewStatuses.id'))
    reviewer_id = db.Column(db.Integer, db.ForeignKey('administrators.id'))

    def __repr__(self):
        return f'<Feedback {self.id}>'


class ReviewStatus(db.Model):
    __tablename__ = 'reviewStatuses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    feedbacks = db.relationship('Feedback', backref='reviewStatus')

    def __repr__(self):
        return f'<ReviewStatus {self.name}>'


class Administrator(db.Model):
    __tablename__ = 'administrators'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    feedbacks = db.relationship('Feedback', backref='reviewer')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Administrator {self.name}>'
