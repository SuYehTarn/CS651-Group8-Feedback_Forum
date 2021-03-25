"""The module of the routes of the Main blueprint
"""
from flask import render_template, flash
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.main import main
from app.models.feedback import Feedback
from app.models.review_status import ReviewStatus
from app.main.forms import FeedbackForm, FeedbackCheck, FeedbackResponse

from app.email import send_email


@main.route('/', methods=['GET', 'POST'])
def index():
    """View of providing a feedback from the client side"""
    form = FeedbackForm()
    if form.validate_on_submit():
        try:
            data = {
                'email': form.email.data,
                'title': form.title.data,
                'content': form.content.data,
            }
            new_feedback = Feedback(**data)
            db.session.add(new_feedback)
            db.session.commit()

            committed_feedback = Feedback.query \
                .filter_by(**data).first()
            token = committed_feedback.token

            send_email(data['email'],
                       'Thank you for your feedback.',
                       'main/mail/new_feedback',
                       token=token)

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


@main.route('/check/', methods=['GET', 'POST'])
def check():
    """View of checking the feedback information
    from the client side
    """
    form = FeedbackCheck()
    if form.validate_on_submit():
        token = form.token.data
        feedback = Feedback.query.filter_by(token=token).first()
        if feedback is not None:
            status = ReviewStatus.query \
                .filter_by(id=feedback.review_status_id).first()
            feedback_response = FeedbackResponse()
            feedback_response.id.default = feedback.id
            feedback_response.title.default = feedback.title
            feedback_response.content.default = feedback.content
            feedback_response.email.default = feedback.email
            feedback_response.Status.default = status.name
            feedback_response.Response.default = feedback.response
            feedback_response.process()
            return render_template('/main/response.html',
                                   form=feedback_response)
        flash('Feedback not found.')
    return render_template('/main/check.html',
                           form=form)
