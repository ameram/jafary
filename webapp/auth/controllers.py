from flask.helpers import flash, url_for
from werkzeug.utils import redirect
from .forms import LoginForm
from flask_login import login_user, logout_user
from flask import Blueprint, render_template
from .forms import LoginForm, RegisterForm
from ..qa.models import User
from ..qa.models import db

auth_blueprint = Blueprint(
    'auth',
    __name__,
    template_folder='../templates/auth',
    url_prefix="/auth"
)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    log_form = LoginForm()
    if log_form.validate_on_submit():
        user = User.query.filter_by(username=log_form.username.data).first()
        login_user(user, remember=log_form.remember.data)
        flash('Logged in.')
        return redirect(url_for('main.index'))

    return render_template('login.html', form=log_form)


@auth_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash("You have been logged out.", category="success")
    return redirect(url_for('main.index'))


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    uform = RegisterForm()
    if uform.validate_on_submit():
        new_user = User()
        new_user.username = uform.username.data
        new_user.set_password(uform.password.data)
        new_user.firstname = uform.firstname.data
        new_user.lastname = uform.lastname.data
        new_user.phone_number = uform.phonenumber.data
        new_user.email = uform.email.data
        new_user.age = uform.age.data
        db.session.add(new_user)
        db.session.commit()
        flash("Your user has been created, please login.", category="success")
        return redirect(url_for('.login'))
    return render_template('register.html', form=uform)
