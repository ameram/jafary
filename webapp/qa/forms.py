from flask_wtf import FlaskForm as Form
from wtforms import StringField, TextAreaField, SelectField, PasswordField, IntegerField, FloatField, DateTimeField
from wtforms.fields.core import BooleanField
from wtforms.validators import DataRequired, Length, NumberRange
from .models import Group, Subgroup


class CounselorForm(Form):
    username = StringField('Username', validators=[
                           DataRequired(), Length(max=255)])
    password = PasswordField('Password')
    firstname = StringField('Firstname', validators=[
                            DataRequired(), Length(max=255)])
    lastname = StringField('Lastname', validators=[
                           DataRequired(), Length(max=255)])
    phonenumber = StringField('Phone Number')
    email = StringField('Email', validators=[
                        DataRequired(), Length(max=255)])
    degree = SelectField('Degree', choices=[
                         (1, 'Diploma'), (2, 'Bachelor'), (3, 'Masters'), (4, 'PhD')])


class CouselorInForm(Form):
    username = StringField('Username', validators=[
                           DataRequired(), Length(max=255)])
    password = PasswordField('Password')


class GroupForm(Form):
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])


class SubgroupForm(Form):
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])


class PaymentForm(Form):
    value = FloatField('Price', validators=[NumberRange(0.00, 99999.99)])


class RespondForm(Form):
    content = TextAreaField(u'Content', validators=[DataRequired()])


class ScheduleForm(Form):
    timedate = DateTimeField('Datetime', format='% Y-%m-%d')


class RequestForm(Form):
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    content = TextAreaField(u'Content', validators=[DataRequired()])
    group = SelectField('Group')
    subgroup = SelectField('Subgroup')
    paid = BooleanField('Paid', validators=[DataRequired()])

    def __init__(self):
        super(RequestForm, self).__init__()
        self.group.choices = [(c.id, c.title) for c in Group.query.all()]

    def __init__(self):
        super(RequestForm, self).__init__()
        self.subgroup.choices = [(c.id, c.title) for c in Subgroup.query.all()]
