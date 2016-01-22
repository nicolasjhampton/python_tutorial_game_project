from peewee import *
from playhouse.test_utils import test_database
import unittest

import server
from models import User


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.TEST_DB = SqliteDatabase(':memory:')
        self.TEST_DB.connect()
        self.TEST_DB.create_tables([User], safe=True)
        server.app.config['TESTING'] = True
        server.app.config['WTF_CSRF_ENABLED'] = False
        self.app = server.app.test_client()
        self.data = {
            'username': 'testUsername',
            'email': 'test@example.com',
            'password': 'password',
            'password2': 'password'
        }

    # def tearDown(self):
    #     os.close(self.db_fd)
    #     os.unlink(app.app.config['DATABASE'])
    
    def test_register_url(self):
        """Test for a 200 status code from our registration's GET route"""
        with test_database(self.TEST_DB, (User,)):
            rv = self.app.get('/register')
            self.assertEqual(rv.status_code, 200)
            
            
    # Saving this for later...
    # We'll need 
    # 1. a form file and 
    # 2. a post node on our view function (this may need another status test) and
    # 3. before and after request methods to connect and close the database 
    def test_registration(self):
        """Test User creation through our POST route"""
        with test_database(self.TEST_DB, (User,)):
            rv = self.app.post('/register', data=data)
            self.assertEqual(User.select().count(), 1)
            self.assertEqual(User.get().username, 'testUsername')
            self.assertEqual(User.get().email, 'test@example.com')
            self.assertNotEqual(User.get().password, 'password')
            self.assertEqual(rv.status_code, 200)
            
    
if __name__ == '__main__':
    unittest.main()
        