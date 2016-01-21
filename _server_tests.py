# I've deleted the imports for tempfile and os
# since they were for creating a tempfile for a database
# and I'm going to make one in memory instead
import unittest

# Redirects the database file from our model's  
# database file declaration to a test location
from playhouse.test_utils import test_database
from peewee import *

import server
from models import User

# Instead of running models.initialize, which would 
# use the model's DATABASE variable directed at the
# 'models.db' file, we're going to direct everything
# to our TEST_DB in memory. I also decided to put all
# of this in the setUp method. I have no idea if it
# works there, but if it does, it will get these 
# variables out of the global scope, which a 
# principal of functional programming
# TEST_DB = SqliteDatabase(':memory:')
# TEST_DB.connect()
# TEST_DB.create_tables([User], safe=True)


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.TEST_DB = SqliteDatabase(':memory:')
        self.TEST_DB.connect()
        self.TEST_DB.create_tables([User], safe=True)
        server.app.config['TESTING'] = True
        server.app.config['WTF_CSRF_ENABLED'] = False
        self.app = server.app.test_client()

    # def tearDown(self):
    #     os.close(self.db_fd)
    #     os.unlink(app.app.config['DATABASE'])
    
    def test_register_url(self):
        """Test to for a 200 status code from our registration url"""
        with test_database(self.TEST_DB, (User,)):
            rv = self.app.get('/register')
            self.assertEqual(rv.status_code, 200)
            
            
    # Saving this for later...
    # We'll need 
    # 1. a form file and 
    # 2. a post node on our view function (this may need another status test) and
    # 3. before and after request methods to connect and close the database 
    def test_registration(self):
        data = {
            'username': 'testUsername',
            'email': 'test@example.com',
            'password': 'password',
            'password2': 'password'
        }
        with test_database(self.TEST_DB, (User,)):
            rv = self.app.post('/register', data=data)
            self.assertEqual(User.select().count(), 1)
            self.assertEqual(User.get().username, 'testUsername')
            self.assertEqual(User.get().email, 'test@example.com')
            self.assertNotEqual(User.get().password, 'password')
            self.assertEqual(rv.status_code, 200)
 

if __name__ == '__main__':
    unittest.main()
        