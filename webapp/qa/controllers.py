from flask import Flask, render_template, redirect, url_for, abort, flash, request, \
    current_app, make_response, Blueprint, session, g
from sqlalchemy import func
from  .models import db, Request, User, Counselor, Respond, Payment, Schedule, Type, Group, Subgroup, State
from .forms import UserInForm, UserForm



qa_blueprint = Blueprint(
    'qa',
    __name__,
    template_folder='../templates/qa/',
    url_prefix="/qa"
)


def sidebar_data():
    recent = Request.query.filter_by(
        type_foreignkey='2').order_by(Request.pub_date.desc()).limit(5).all()

    return recent


@qa_blueprint.route('/')
@qa_blueprint.route('/<int:page>')
def home(page=1):
    requests = Request.query.order_by(Request.pub_date.desc()).paginate(
        page, current_app.config.get('POSTS_PER_PAGE', 10), False)
    recent = sidebar_data()

    return render_template('home.html', requests=requests, recent=recent)


@qa_blueprint.route('/group/<string:group_title>')
def requests_by_group(group_title):
    group = Group.query.filter_by(title=group_title).first_or_404()
    requests = group.requests.order_by(Request.pub_date.desc()).all()
    recent = sidebar_data()

    return render_template('group.html', requests=requests, group=group, recent=recent)


@qa_blueprint.route('/request/<int:request_id>', methods=('GET', 'POST'))
def request(request_id):
    request = Request.query.get_or_404(request_id)
    if (request.group is not None):
        group = request.group.title
    else:
        group = 'Unknown'
    recent = sidebar_data()

    return render_template('request.html', request=request, group=group, recent=recent,)


@qa_blueprint.route('/user/<string:username>')
def requests_by_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    requests = user.requests.order_by(
        Request.pub_date.desc()).all()
    recent = sidebar_data()
    return render_template('user.html', user=user, requests=requests, recent=recent)


@qa_blueprint.route('/create')
def create_request():
    return render_template('create.html')


@qa_blueprint.route('/signup', methods=('GET', 'POST'))
def signup():
    user_form = UserForm()
    if user_form.validate_on_submit():
        new_user = User()
        new_user.username = user_form.username.data
        new_user.password = user_form.password.data
        new_user.firstname = user_form.firstname.data
        new_user.lastname = user_form.lastname.data
        new_user.phone_number = user_form.phonenumber.data
        new_user.email = user_form.email.data
        new_user.age = user_form.age.data
        v = User.query.filter_by(username=new_user.username).first()
        if v is None:
            flash('Username is taken', 'error')
            db.session.rollback()
            return redirect(url_for('signup'))
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            flash('Error signing you up: %s' % str(e), 'error')
            db.session.rollback()
            return redirect(url_for('signup'))
        else:
            flash('Sign-up was successful', 'info')
        return redirect(url_for('requests_by_user', username=new_user.username))

    return render_template('signup.html', form=user_form)
