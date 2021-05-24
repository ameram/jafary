from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig

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

    def __init__(self, username, password, firstname, lastname, phone_number, email, age):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.phone_number = phone_number
        self.email = email
        self.age = age


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

    def __init__(self, username, firstname, lastname, phone_number, email, password, degree, score=0):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.phone_number = phone_number
        self.email = email
        self.password = password
        self.degree = degree
        self.score = score


class Group(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    subgroups = db.relationship('Subgroup', backref='group', lazy='dynamic')

    def __init__(self, title):
        self.title = title


class Subgroup(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    group_foreignkey = db.Column(db.Integer(), db.ForeignKey('group.id'))

    def __init__(self, title):
        self.title = title

# un1 = User('aaa', '123', 'what', 'what', '9879879876', 'afds@asdf.asdf', 22)
# cn1 = Counselor('conone', 'conA', 'conB', 'conNum', 'conMail', 'conPass', 'conDe')

