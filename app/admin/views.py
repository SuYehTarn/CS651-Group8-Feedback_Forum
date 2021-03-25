"""Module of back stage views
"""

from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from app import db
from app.admin.form import ReviewFeedbackForm
from app.models.feedback import Feedback
from app.models.review_status import ReviewStatus

from app.admin import admin


@admin.route('/admin')
@admin.route('/admin/')
@login_required
def index():
    """View of list all feedbacks"""
    all_feedbacks = db.session.query(Feedback).all()
    return render_template('/admin/index.html',
                           feedbacks=all_feedbacks)


@admin.route('/admin/<feedback_id>', methods=['GET', 'POST'])
@login_required
def read_feedback(feedback_id):
    """View of reading a feedback"""
    feedback = db.session.query(Feedback)\
        .filter_by(id=feedback_id).first()

    if not feedback:
        flash('Wrong feedback ID')
        return redirect(url_for('admin.index'))

    form = ReviewFeedbackForm()

    # set choices of review statuses
    review_statuses = ReviewStatus.query.all()
    choices = [(status.id, status.name)
               for status in review_statuses]
    form.review_status.choices = choices

    if form.validate_on_submit():
        feedback.response = form.response.data
        feedback.review_status_id = form.review_status.data
        db.session.commit()
        flash('Modification saved.')

    # set default values
    form.review_status.default = feedback.review_status_id
    form.response.default = feedback.response
    form.id.default = feedback.id
    form.title.default = feedback.title
    form.content.default = feedback.content
    form.process()

    return render_template('/admin/feedback.html',
                           form=form)
