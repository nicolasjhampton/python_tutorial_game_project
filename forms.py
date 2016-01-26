from flask_wtf import Form
from wtforms import PasswordField, StringField
from wtforms.validators import (DataRequired, Email, EqualTo,
                                Length, Regexp, ValidationError)

from models import User


def username_exists(form, field):
    """Custom validator checks database for duplicate username"""
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that username already exists.')


def email_exists(form, field):
    """Custom validator checks database for duplicate email"""
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


class RegistrationForm(Form):
    """Validation form for new User registration"""

    # Valid username field parameters
    username = StringField(
        'username',
        validators=[
            DataRequired(),
            Regexp(r'^[a-zA-Z0-9_]+$',
                   message=("Username should be one word, letters, "
                            "numbers, and underscores only.")),
            Length(min=4),
            Length(max=50),
            username_exists
            ])

    # Valid email field parameters
    email = StringField(
        'email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
            ])

    # Valid password field parameters
    password = PasswordField(
        'password',
        validators=[
            DataRequired(),
            Length(min=7),
            Length(max=20),
            ])

    # Valid confirm password field parameters
    password2 = PasswordField(
        'confirm password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ])


class LoginForm(Form):

    # Valid username field parameters
    username = StringField('username', validators=[DataRequired()])

    # Valid password field parameters
    password = PasswordField('password', validators=[DataRequired()])
    