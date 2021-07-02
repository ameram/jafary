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


class GetUser(Form):
    username = StringField('Username', validators=[
                           DataRequired(), Length(max=255)])


class GetGroup(Form):
    title = StringField('Group Title', validators=[
                           DataRequired(), Length(max=255)])


class DelGroupForm(Form):
    group = SelectField('Group', validators=[DataRequired()])

    def __init__(self):
        super(DelGroupForm, self).__init__()
        self.group.choices = [(c.id, c.title) for c in Group.query.all()]


class SubgroupForm(Form):
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    group = SelectField('Group', validators=[DataRequired()])

    def __init__(self):
        super(SubgroupForm, self).__init__()
        self.group.choices = [(c.id, c.title) for c in Group.query.all()]


class DelSubgroupForm(Form):
    subgroup = SelectField('Subgroup', validators=[DataRequired()])

    def __init__(self):
        super(DelSubgroupForm, self).__init__()
        self.subgroup.choices = [(c.id, c.title) for c in Subgroup.query.all()]


class PaymentForm(Form):
    value = FloatField('Price', validators=[NumberRange(0.00, 99999.99)])
    date = DateTimeField('Date', format='%d/%m/%y')
    method = BooleanField('Call')


class RespondForm(Form):
    content = TextAreaField(u'Content', validators=[DataRequired()])


class RequestForm(Form):
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    content = TextAreaField(u'Content', validators=[DataRequired()])
    group = SelectField('Group')
    subgroup = SelectField('Subgroup')
    paid = BooleanField('Paid')

    def __init__(self):
        super(RequestForm, self).__init__()
        self.group.choices = [(c.id, f'{c.id}. {c.title}') for c in Group.query.all()]
        self.subgroup.choices = [(c.id, f'{c.group_foreignkey}. {c.title}') for c in Subgroup.query.order_by(Subgroup.group_foreignkey).all()]
        # self.subgroup.choices = [(c.id, f'{c.group_foreignkey}. {c.title}') for c in Subgroup.query.filter_by(group_foreignkey=1).all()]
