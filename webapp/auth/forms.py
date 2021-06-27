from flask_wtf import FlaskForm as Form
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, IntegerField, SelectField
from wtforms import validators
from wtforms.validators import DataRequired, Length, URL, EqualTo, NumberRange
from ..qa.models import User


class LoginForm(Form):
    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField("Remember Me")

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        if not check_validate:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username or password')
            return False
        if not user.check_password(self.password.data):
            self.username.errors.append('Invalid username or password')
            return False
        return True


class RegisterForm(Form):
    username = StringField('Username', validators=[
                           DataRequired(), Length(max=255)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8)])
    confirm = PasswordField('Confirm the password', validators=[
                                     DataRequired(), EqualTo('password')])
    firstname = StringField('Firstname', validators=[
                            DataRequired(), Length(max=255)])
    lastname = StringField('Lastname', validators=[
                           DataRequired(), Length(max=255)])
    phonenumber = StringField('Phone Number')
    email = StringField('Email', validators=[
                        DataRequired(), Length(max=255)])
    age = IntegerField('Age', validators=[NumberRange(min=12, max=99)])

    def validate(self):
        check_validate = super(RegisterForm, self).validate()
        if not check_validate:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("User with that name already exists")
            return False
        return True


class RequestForm(Form):
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    content = TextAreaField(u'Content', validators=[DataRequired()])
    group = SelectField(u'Group', coerce=int)
    subggroup = SelectField(u'Subgroup', coerce=int)
