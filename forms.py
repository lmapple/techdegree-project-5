import datetime

from models import User, Entry
from flask_wtf import Form

from wtforms import StringField, PasswordField, DateField, TextAreaField, IntegerField
from wtforms.validators import (DataRequired, Regexp, ValidationError,
                                Email, Length, EqualTo
                                )


def name_exists(form,field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('Username already exists.')

def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


class RegisterForm(Form):
    username = StringField(
        'Username', validators=[
            DataRequired(),
            name_exists,
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, using letters,"
                         "numbers, and underscores only.")
            )
        ])
    email = StringField(
        'Email', validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password', validators=[
            DataRequired(),
            Length(min=8),
            EqualTo('password2', message='Passwords must match.')
        ])
    password2 = PasswordField(
        'Confirm Password', validators=[
            DataRequired()
        ])


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class NewEntry(Form):
    title = StringField('Title', validators=[DataRequired()])
    date = DateField('YYYY-MM-DD', default=datetime.datetime.now,validators=[DataRequired()])
    time_spent = IntegerField('Time Spent (Minutes)', validators=[DataRequired()])
    what_i_learned = TextAreaField('What I Learned', validators=[DataRequired()])
    resources_to_remember = TextAreaField('Resources to Remember',
                                        validators=[DataRequired()])


class EditEntry(Form):
    title = StringField('Title', validators=[DataRequired()])
    date = DateField('YYYY-MM-DD',validators=[DataRequired()])
    time_spent = IntegerField('Time Spent', validators=[DataRequired()])
    what_i_learned = TextAreaField('What I Learned', validators=[DataRequired()])
    resources_to_remember = TextAreaField('Resources to Remember',
                                        validators=[DataRequired()])