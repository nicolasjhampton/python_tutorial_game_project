from flask_wtf import Form
from wtforms import PasswordField, StringField

from models import User

class RegistrationForm(Form):
    username = StringField('username')
    email = StringField('email')
    password = PasswordField('password') 
    password2 = PasswordField('password2')