import datetime
from flask.ext.bcrypt import check_password_hash, generate_password_hash
# from flask.ext.login import UserMixin
from peewee import *
import re

DATABASE = SqliteDatabase('users.db')


class User(Model):  # add UserMixin to this class later
    """Database schema for the User table. All database objects
       descend from 'Model' class."""
    username = CharField(max_length=50, unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=20)
    joined_at = DateTimeField(default=datetime.datetime.now)
    invalidValueError = "email"

    class Meta:
        database = DATABASE

    def hash_password(password):
        """Generate new password hash"""
        if password is not None:
            # generate_password_hash(password=password, rounds=12)
            # this will produce a hash that starts with $2a$
            return generate_password_hash(password)

    def check_password_against_hash(cls, password):
        """Check user's password hash against input"""
        return check_password_hash(cls.password, password)

    def check_new_username(cls, username):
        pattern = re.compile(r'^[a-zA-Z0-9_]+$')
        """Username validity check"""
        if len(username) > 3 and len(username) < 51 and pattern.match(username):
            return username
        else:
            cls.error = "username"
            return None

    def check_new_password(cls, password):
        """Password validity check"""
        if len(password) > 6 and len(password) < 20:
            return password
        else:
            cls.error = "password"
            return None

    @classmethod
    def create_user(cls, username, email, password):
        """Method to safely create a new User entry.
           Sqlite3 does not enforce character length
           limits on VARCHAR fields, so we have to
           manually block and throw errors."""

        usernameChecked = cls.check_new_username(cls, username)

        passwordChecked = cls.check_new_password(cls, password)

        try:
            cls.create(
                username=usernameChecked,
                email=email,
                password=cls.hash_password(passwordChecked))
        except IntegrityError:
            raise ValueError("User already exists")
        except UnboundLocalError:
            # Thrown if the username, password, or email are invalid
            raise ValueError("Invalid {}".format(cls.invalidValueError))


def initialize():
    """Called when the program starts if not called as an imported module"""
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()
