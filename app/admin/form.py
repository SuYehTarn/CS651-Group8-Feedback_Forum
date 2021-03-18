"""The module of the flask form of back stages.
"""

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField


class ReviewFeedbackForm(FlaskForm):
    """The class of the flask form for reviewing feedback"""
    response = TextAreaField()
    submit = SubmitField()
