"""Module of email sending functionality
"""
from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from app import mail


def send_async_email(app, msg):
    """The function of triggering the send of email"""
    with app.app_context():
        mail.send(msg)


def send_email(email, subject, template, **kwargs):
    """The function of sending email with a thread"""
    app = current_app._get_current_object()
    msg = Message(subject=f'{app.config["FEEDBACK_FORUM_MAIL_SUBJECT_PREFIX"]} {subject}',
                  sender=app.config['FEEDBACK_FORUM_MAIL_SENDER'],
                  recipients=[email])
    msg.body = render_template(f'{template}.txt', **kwargs)
    msg.html = render_template(f'{template}.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
