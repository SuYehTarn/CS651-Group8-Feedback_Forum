from . import main
from app.models.feedback import Feedback
from .forms import *
from flask import render_template, redirect, request, url_for, flash,session
from app import db



@main.route('/', methods=['GET', 'POST'])
def index():
    form = Feedback()
    if form.validate_on_submit():
       #  NewFeedback = Feedback(_email=form.Email.data,_title=form.Title.data,content=form.Content.data)
       #  flash('Your FeedBack is added Successfully')
       #  db.session.add(NewFeedback)
       #  db.session.commit()
       #  newFeedback = Feedback.query.filterby(email=form.Email.data).first()
         return render_template('success.html')
    return render_template('base.html', form=form, name=session.get('Email'))

@main.route('/about')
def hello1():
    return render_template('about.html')

@main.route('/check',methods=['GET', 'POST'])
def hello2():
    form = FeedbackCheck()
    if form.validate_on_submit():
        session['Token'] = form.Token.data
        return render_template('Response.html',form=FeedbackResponse())
    return render_template('check.html', form=form, name=session.get('Token'))


