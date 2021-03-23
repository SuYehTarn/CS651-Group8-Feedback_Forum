"""Module of the routes of the Auth blueprint
"""
from flask import render_template
from app.auth import auth
from app.auth.forms import LoginForm


@auth.route('/login/')
def login():
    """View of login to the backstage"""
    form = LoginForm()
    return render_template('/auth/login.html', form=form)
