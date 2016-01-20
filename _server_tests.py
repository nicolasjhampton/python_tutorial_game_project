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
        # flask lays out these instructions for using app.config
        # to redirect the tests to our test database.
        # I've opted to use test_database instead...
        # self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        # app.app.config['TESTING'] = True
        # self.app = app.app.test_client()
        # flaskr.init_db()

    # def tearDown(self):
    #     os.close(self.db_fd)
    #     os.unlink(app.app.config['DATABASE'])
    
    def test_register_url(self):
        with test_database(self.TEST_DB, (User,)):
            rv = self.app.get('/register')
            self.assertEqual(rv.status_code, 200)
            
            
    # Saving this for later...
    # def test_registration(self):
    #     data = {
    #         'username': 'testUsername',
    #         'email': 'test@example.com',
    #         'password': 'password',
    #         'password2': 'password'
    #     }
    #     with test_database(TEST_DB, (User,)):
    #         rv = self.app.post(
    #             '/register',
    #             data=data)
    #         self.assertEqual(rv.status_code, 302)
    #         self.assertEqual(rv.location, 'http://localhost/')

if __name__ == '__main__':
    unittest.main()
        