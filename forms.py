from flask_wtf import Form
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

#Username has to be over 3 and under 50 ascii characters, and unique

#email has to be present and be in email format, and unique

#password has to be over 6 and under 20 characters

#password2 has to match password

class RegistrationForm(Form):
    username = StringField(
        'username',
        validators=[
            DataRequired(),
            Regexp(r'^[a-zA-Z0-9_]+$',
                   message=("Username should be one word, letters, "
                            "numbers, and underscores only.")),
            Length(min=4),
            Length(max=50)
            ])
    email = StringField(
        'email',
        validators=[
            DataRequired(),
            Email()
            ])
    password = PasswordField(
        'password',
        validators=[
            DataRequired(),
            Length(min=7),
            Length(max=20),  
            ]) 
    password2 = PasswordField(
        'password2',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ])