from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from config import DevConfig
from datetime import datetime

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)


@app.route('/')
def home():
    return '<h1>Hello World!</h1>'


if __name__ == '__main__':
    app.run()


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


# class RequestState(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     title = db.Column(db.String(255))
#     requests = db.relationship(
#         'Request', backref='requeststate', lazy='dynamic')


# class RequestType(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     title = db.Column(db.String(255))
#     requests = db.relationship(
#         'Request', backref='requesttype', lazy='dynamic')


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

    # state = db.Column(db.Integer(), db.ForeignKey('requeststate.id'))
    # type = db.Column(db.Integer(), db.ForeignKey('requesttype.id'))

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
        db.Integer(), db.ForeignKey('user.id'), nullable=False)
    counselor_foreignkey = db.Column(
        db.Integer(), db.ForeignKey('counselor.id'))
    request_foreignkey = db.Column(db.Integer(), db.ForeignKey(
        'request.id'), nullable=False)
    payment_foreignkey = db.Column(
        db.Integer(), db.ForeignKey('payment.id'), nullable=True)
