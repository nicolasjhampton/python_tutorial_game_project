import datetime

# Peewee convention is to make this very broad import
from peewee import *

# This will define the database to be connected to / created 
DATABASE = SqliteDatabase('users.db')

# User is based on the 'Model' class, as all our database 
# objects will be.
class User(Model):
    """Database schema for the User table. All database objects descend from 'Model' class."""
    username = CharField(max_length=50, unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=20)
    joined_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = DATABASE
    
    @classmethod
    def create_user(cls, username, email, password):
        """Method to safely create a new User entry.
           Sqlite3 does not enforce character length
           limits on VARCHAR fields, so we have to 
           manually block and throw errors."""
           
        error = "email"
        
        # Username length check
        if(len(username) > 3 and len(username) < 51):
            usernameChecked = username
        else:
            error = "username"
         
        # Password length check    
        if(len(password) > 6 and len(password) < 20):
            passwordChecked = password
        else:
            error = "password"
            
        try:
            cls.create(
                username=usernameChecked,
                email=email,
                password=passwordChecked)
        except IntegrityError:
            raise ValueError("User already exists")
        except UnboundLocalError:
            raise ValueError("Invalid {}".format(error))
            
             
def initialize():
    """Called when the program starts if not called as an imported module"""
    
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    User.create_user(username='testUsername',
                email='testEmail@testEmail.com',
                password='testPassword')
    DATABASE.close()
    

if __name__ == "__main__":
    """Called when the program starts if not called as an imported module"""
    initialize()

        
