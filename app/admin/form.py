"""The module of the flask form of back stages.
"""

from flask_wtf import FlaskForm
from wtforms import (SubmitField, TextAreaField,
                     SelectField, IntegerField,
                     StringField)


class ReviewFeedbackForm(FlaskForm):
    """The class of the flask form for reviewing feedback"""
    id = IntegerField(render_kw={'disabled': ""})
    email = StringField(render_kw={'disabled': ""})
    title = StringField(render_kw={'disabled': ""})
    content = TextAreaField(render_kw={'disabled': ""})
    review_status = SelectField()
    response = TextAreaField()
    submit = SubmitField()
