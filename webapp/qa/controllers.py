from flask import Flask, render_template, redirect, url_for, abort, flash, request, \
    current_app, make_response, Blueprint, session, g
from sqlalchemy import func
from  .models import db, Request, User, Counselor, Respond, Payment, Schedule, Type, Group, Subgroup, State



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

