from flask import render_template
from .forms import *
from . import auth


@auth.route('/auth')
def hello():
    form = LoginForm()

    return render_template('auth.html', form=form)
