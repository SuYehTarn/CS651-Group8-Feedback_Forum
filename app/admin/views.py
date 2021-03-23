"""Module of back stage views
"""

from flask import render_template, flash, redirect, url_for
#from flask_login import login_required

from app import db
from app.admin.form import ReviewFeedbackForm
from app.models.feedback import Feedback

from app.admin import admin


@admin.route('/admin')
@admin.route('/admin/')
#@login_required
def index():
    """View of list all feedbacks"""
    all_feedbacks = db.session.query(Feedback).all()
    return render_template('/admin/index.html',
                           feedbacks=all_feedbacks)


@admin.route('/admin/<feedback_id>')
#@login_required
def read_feedback(feedback_id):
    """View of reading a feedback"""
    feedback = db.session.query(Feedback)\
        .filter_by(id=feedback_id).first()
    if not feedback:
        flash('Wrong feedback ID')
        return redirect(url_for('admin.index'))
    form = ReviewFeedbackForm()
    return render_template('/admin/feedback.html',
                           feedback=feedback,
                           form=form)
