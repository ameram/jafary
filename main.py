
# TODO: add str() to all classes

from flask import Flask, render_template, redirect, url_for, abort, flash, request, \
    current_app, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref, relationship
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import table, column, MetaData
from config import DevConfig
from datetime import datetime
from flask_migrate import Migrate

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

app = Flask(__name__)
app.config.from_object(DevConfig)
metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db, render_as_batch=True)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    email = db.Column(db.String(255))
    age = db.Column(db.Integer)
    requests = db.relationship('Request', backref='user', lazy='dynamic')
    payments = db.relationship('Payment', backref='user', lazy='dynamic')
    responds = db.relationship('Respond', backref='user', lazy='dynamic')
    schedule_foreignkey = db.relationship('Schedule', backref='user')

    def __init__(self, username):
        self.username = username


class Counselor(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    degree = db.Column(db.String(255))
    score = db.Column(db.Integer(), default=0)
    requests = db.relationship('Request', backref='counselor', lazy='dynamic')
    payments = db.relationship('Payment', backref='counselor', lazy='dynamic')
    responds = db.relationship('Respond', backref='counselor', lazy='dynamic')
    schedule_foreignkey = db.relationship('Schedule', backref='counselor')

    def __init__(self, username):
        self.username = username


class Group(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    subgroups = db.relationship('Subgroup', backref='group', lazy='dynamic')
    requests = db.relationship('Request', backref='group', lazy='dynamic')

    def __init__(self, title):
        self.title = title


class Subgroup(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    group_foreignkey = db.Column(db.Integer(), db.ForeignKey('group.id'))
    requests = db.relationship('Request', backref='subgroup', lazy='dynamic')

    def __init__(self, title):
        self.title = title


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    requests = db.relationship('Request', backref='type', lazy='dynamic')

    def __init__(self, name):
        self.name = name


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    requests = db.relationship('Request', backref='state')
    schedule_foreignkey = db.relationship('Schedule', backref='state')


class Request(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    content = db.Column(db.String(255))
    title = db.Column(db.String(255), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_foreignkey = db.Column(
        db.Integer(), db.ForeignKey('user.id'), nullable=False)
    counselor_foreignkey = db.Column(
        db.Integer(), db.ForeignKey('counselor.id'))
    group_foreignkey = db.Column(db.Integer(), db.ForeignKey(
        'group.id'), nullable=True)
    subgroup_foreignkey = db.Column(db.Integer(), db.ForeignKey('subgroup.id'))
    payment_foreignkey = db.Column(db.Integer(), db.ForeignKey('payment.id'))
    responds = db.relationship('Respond', backref='request', lazy='dynamic')
    state_foreignkey = db.Column(
        db.Integer, db.ForeignKey('state.id'), nullable=True)
    type_foreignkey = db.Column(
        db.Integer, db.ForeignKey('type.id'), nullable=True)
    schedule_foreignkey = db.relationship('Schedule', backref='request')

    def __init__(self, title):
        self.title = title


class Payment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    value = db.Column(db.Float(), nullable=False)
    pay_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_foreignkey = db.Column(
        db.Integer(), db.ForeignKey('user.id'), nullable=False)
    counselor_foreignkey = db.Column(
        db.Integer(), db.ForeignKey('counselor.id'))
    request_to = db.relationship('Request', backref='payment', lazy=True)
    responds = db.relationship('Respond', backref='payment', lazy='dynamic')


class Respond(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text)

    user_foreignkey = db.Column(
        db.Integer(), db.ForeignKey('user.id'), nullable=True)
    counselor_foreignkey = db.Column(
        db.Integer(), db.ForeignKey('counselor.id'))
    request_foreignkey = db.Column(db.Integer(), db.ForeignKey(
        'request.id'), nullable=False)
    payment_foreignkey = db.Column(
        db.Integer(), db.ForeignKey('payment.id'), nullable=True)


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    s_time = db.Column(db.DateTime)
    user_foreignkey = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    counselor_foreignkey = db.Column(
        db.Integer, db.ForeignKey('counselor.id'))
    request_foreignkey = db.Column(db.Integer, db.ForeignKey(
        'request.id'), nullable=False)
    state_foreignkey = db.Column(db.Integer, db.ForeignKey('state.id'))

# View code


def sidebar_data():
    recent = Request.query.filter_by(
        type_foreignkey='2').order_by(Request.pub_date.desc()).limit(5).all()

    return recent


@app.route('/')
@app.route('/<int:page>')
def home(page=1):
    requests = Request.query.order_by(Request.pub_date.desc()).paginate(
        page, app.config.get('POSTS_PER_PAGE', 10), False)
    recent = sidebar_data()

    return render_template('home.html', requests=requests, recent=recent)


@app.route('/group/<string:group_title>')
def requests_by_group(group_title):
    group = Group.query.filter_by(title=group_title).first_or_404()
    requests = group.requests.order_by(Request.pub_date.desc()).all()
    recent = sidebar_data()

    return render_template('group.html', requests=requests, group=group, recent=recent)


@app.route('/request/<int:request_id>', methods=('GET', 'POST'))
def request(request_id):
    request = Request.query.get_or_404(request_id)
    if (request.group is not None):
        group = request.group.title
    else:
        group = 'Unknown'
    recent = sidebar_data()

    return render_template('request.html', request=request, group=group, recent=recent,)


@app.route('/user/<string:username>')
def requests_by_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    requests = user.requests.order_by(
        Request.pub_date.desc()).all()
    recent = sidebar_data()
    return render_template('user.html', user=user, requests=requests, recent=recent)


if __name__ == '__main__':
    app.run()
