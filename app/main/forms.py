from flask_wtf import FlaskForm

from wtforms import *
from wtforms.validators import *


class Feedback(FlaskForm):
    Email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    Title = StringField('Title', validators=[DataRequired()])
    Content =TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

class FeedbackCheck(FlaskForm):
    Token = StringField('Token',validators=[DataRequired()])
    submit = SubmitField('Submit')


class FeedbackResponse(FlaskForm):
    Status = StringField('Status')
    Response = StringField('Response')


