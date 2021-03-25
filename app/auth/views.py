"""Module of the routes of the Auth blueprint
"""
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, current_user, login_required, logout_user

from app.auth import auth
from app.auth.forms import LoginForm
from app.models.administrator import Administrator


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    """View of login to the backstage"""
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))

    form = LoginForm()
    if form.validate_on_submit():
        admin = Administrator.query \
            .filter_by(name=form.name.data).first()
        if admin is not None and admin.verify_password(form.password.data):
            login_user(admin, form.remember_me.data)
            redirect_url = request.args.get('next')
            if redirect_url is None or not redirect_url.startswith('/'):
                redirect_url = url_for('admin.index')
            return redirect(redirect_url)

        flash('Invalid administrator name or password')

    return render_template('/auth/login.html', form=form)


@auth.route('/logout/')
@login_required
def logout():
    """View of logout"""
    logout_user()
    flash('Administrator Logged out')
    return redirect(url_for('main.index'))
