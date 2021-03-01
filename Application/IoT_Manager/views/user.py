from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required

from IoT_Manager import db_session
from IoT_Manager.sql_models import (
    User,
    Device,
    Trigger,
    Event
)
from IoT_Manager.forms import LoginForm, SignUpForm

User_Blueprint = Blueprint('user', __name__)


@User_Blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # redirect if alread authenticated
    if current_user.is_authenticated:
        return redirect(url_for('management.gen_panel'))

    # Check if post request and if form is filled
    if request.method == 'POST' and form.validate_on_submit():
        user = db_session.query(User).filter_by(email=form.email.data).first()
        # check hash
        if user and user.check_password(form.password.data):
            # create new session
            login_user(user)
            return redirect(url_for('manage.gen_panel'))
        else:
            flash("Invalid login details")

    return render_template('login.html', form=form)



@User_Blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    # create signup form
    form = SignUpForm()
    # CHECK IF USER IS ALL READY SIGNED IN
    if current_user.is_authenticated:
        return redirect(url_for('manage.gen_panel'))

    # check if valid creation request
    if request.method == 'POST' and form.validate_on_submit():
        new_user = User(email=form.email.data,
                        password=form.password.data)
        db_session.add(new_user)
        db_session.commit()
        # create new session
        login_user(new_user)
        # REDIRECT AUTHED USER TO GENERAL PANEL
        return redirect(url_for('management.gen_panel'))
    # RETURN THE SIGNUP HTML PAGE
    return render_template('signup.html', form=form)



@User_Blueprint.route("/logout")
def logout():
    """
    LOGOUT USER
    """
    x = logout_user()
    print('user logout: ' + str(x))
    return redirect(url_for('home'))

