import datetime

from flask.ext.bcrypt import check_password_hash, generate_password_hash
from flask.ext.login import UserMixin
from peewee import * # Peewee convention is to make this very broad import

# This will define the database to be connected to / created 
DATABASE = SqliteDatabase('users.db')

# User is based on the 'Model' class, as all our database 
# objects will be.
class User(UserMixin, Model):
    """Database schema for the User table. All database objects descend from 'Model' class."""
    username = CharField(max_length=50, unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=20)
    joined_at = DateTimeField(default=datetime.datetime.now)
    invalidValueError = "email"
    
    class Meta:
        database = DATABASE
        
    def hash_password(password):
        """Generate new password hash"""
        if password != None:
                  #generate_password_hash(password=password, rounds=12)
                  #this will produce a hash that starts with $2a$
            return generate_password_hash(password)
  
    def check_password(cls, password):
        """Check user's password hash against input""" 
        return check_password_hash(cls.password, password)
        
    def check_new_username_length(cls, username):
        """Username length check"""
        if len(username) > 3 and len(username) < 51:
            return username
        else:
            cls.error = "username"
            return None
            
    def check_new_password_length(cls, password):
        """Password length check"""
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
        
        usernameChecked = cls.check_new_username_length(cls, username)
         
        passwordChecked = cls.check_new_password_length(cls, password)
        
        try:
            cls.create(
                username=usernameChecked,
                email=email,
                password= cls.hash_password(passwordChecked))
        except IntegrityError:
            raise ValueError("User already exists")
        except UnboundLocalError:
            raise ValueError("Invalid {}".format(cls.invalidValueError))
            
             
def initialize():
    """Called when the program starts if not called as an imported module"""
    
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()