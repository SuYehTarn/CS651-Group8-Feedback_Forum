"""The module of the routes of the Main blueprint
"""
from flask import render_template, flash, session
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.main import main
from app.models.feedback import Feedback
from app.main.forms import FeedbackForm, FeedbackCheck, FeedbackResponse


@main.route('/', methods=['GET', 'POST'])
def index():
    """View of providing a feedback from the client side"""
    form = FeedbackForm()
    if form.validate_on_submit():
        try:
            new_feedback = Feedback(email=form.Email.data,
                                    title=form.Title.data,
                                    content=form.Content.data)
            db.session.add(new_feedback)
            db.session.commit()

            committed_feedback = Feedback.query \
                .filter_by(email=form.Email.data).first()
            token = committed_feedback.token

            flash('Your Feedback is added Successfully')
            return render_template('/main/success.html',
                                   token=token)

        except SQLAlchemyError:
            flash('Failed to give a Feedback')

    return render_template('/main/index.html',
                           form=form)


@main.route('/about')
def about():
    """View of presenting the about us page"""
    return render_template('/main/about.html')


@main.route('/check', methods=['GET', 'POST'])
def check():
    """View of checking the feedback information
    from the client side
    """
    form = FeedbackCheck()
    if form.validate_on_submit():
        session['Token'] = form.Token.data
        return render_template('/main/response.html',
                               form=FeedbackResponse())
    return render_template('/main/check.html',
                           form=form,
                           name=session.get('Token'))
