from flask_wtf import FlaskForm as Form
from wtforms import StringField, TextAreaField, SelectField, PasswordField, IntegerField, FloatField, DateTimeField
from wtforms.validators import DataRequired, Length, NumberRange


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
