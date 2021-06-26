from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref, relationship
from sqlalchemy import func, select, table, column
from datetime import datetime
from .. import db


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


class Group(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    subgroups = db.relationship('Subgroup', backref='group', lazy='dynamic')
    requests = db.relationship('Request', backref='group', lazy='dynamic')


class Subgroup(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    group_foreignkey = db.Column(db.Integer(), db.ForeignKey('group.id'))
    requests = db.relationship('Request', backref='subgroup', lazy='dynamic')


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    requests = db.relationship('Request', backref='type', lazy='dynamic')


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
