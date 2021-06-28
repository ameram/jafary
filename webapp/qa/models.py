from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref, relationship
from sqlalchemy import func, select, table, column
from datetime import datetime
from .. import db
from ..auth import bcrypt, AnonymousUserMixin

roles = db.Table(
    'role_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


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

    roles = db.relationship(
        'Role',
        secondary=roles,
        backref=db.backref('users', lazy='dynamic')
    )

    def __init__(self, username=""):
        default = Role.query.filter_by(name="default").one()
        self.roles.append(default)
        self.username = username

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def has_role(self, name):
        for role in self.roles:
            if role.name == name:
                return True
        return False

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @property
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return str(self.id)


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
    responds = db.relationship('Respond', backref='counselor', lazy='dynamic')


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
    arrangements = db.relationship('Payment', backref='request', lazy=True)
    responds = db.relationship('Respond', backref='request', lazy='dynamic')
    state_foreignkey = db.Column(
        db.Integer, db.ForeignKey('state.id'), nullable=True)
    type_foreignkey = db.Column(
        db.Integer, db.ForeignKey('type.id'), nullable=True)


class Payment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    value = db.Column(db.Float(), nullable=False)
    pay_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    call = db.Column(db.Boolean, default=False, nullable=False)
    counselor_foreignkey = db.Column(
        db.Integer(), db.ForeignKey('user.id'), nullable=False)
    request_foreignkey = db.Column(db.Integer(), db.ForeignKey('request.id'))



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

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role {}>'.format(self.name)
