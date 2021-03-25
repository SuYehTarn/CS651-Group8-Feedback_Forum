"""Module contains the flask forms for Main blueprint
"""
from flask_wtf import FlaskForm
from wtforms import  StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, Length


class FeedbackForm(FlaskForm):
    """The class of the flask form for providing
    a feedback from the client side
    """
    email = StringField('Email', validators=[DataRequired(),
                                             Length(1, 64),
                                             Email()])
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')


class FeedbackCheck(FlaskForm):
    """The class of the flask form for checking
    a feedback from the client side
    """
    token = StringField('Token', validators=[DataRequired()])
    submit = SubmitField('Submit')


class FeedbackResponse(FlaskForm):
    """The class of the flask for for presenting
    the feedback information to the client
    """
    id = IntegerField(render_kw={'disabled': ""})
    email = StringField(render_kw={'disabled': ""})
    title = StringField(render_kw={'disabled': ""})
    content = TextAreaField(render_kw={'disabled': ""})
    Status = StringField(render_kw={'disabled': ""})
    Response = StringField(render_kw={'disabled': ""})
