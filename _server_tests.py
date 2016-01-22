from peewee import *
from playhouse.test_utils import test_database
import unittest

import server
from models import User


class AppTestCase(unittest.TestCase):
    """Test suite for our Flask server app"""

    #####################
    # test conditions
    #####################

    def setUp(self):
        """Connects to a test database, sets test server settings,
           defines mock user info, and runs a test client before
           every test (Doesn't close TEST_DB in memory)"""
        # Creates a mock database in memory
        self.TEST_DB = SqliteDatabase(':memory:')
        self.TEST_DB.connect()
        self.TEST_DB.create_tables([User], safe=True)
        # Sets server test conditions
        server.app.config['TESTING'] = True
        server.app.config['WTF_CSRF_ENABLED'] = False
        self.app = server.app.test_client()
        # Defines valid mock data for testing
        self.data = {
            'username': 'testUsername',
            'email': 'test@example.com',
            'password': 'password',
            'password2': 'password'
        }

    #####################
    # GET method tests
    #####################

    def test_register_url(self):
        """Test for a 200 status code from our registration's GET route"""
        with test_database(self.TEST_DB, (User,)):
            rv = self.app.get('/register')
            self.assertEqual(rv.status_code, 200)

    #####################
    # POST method tests
    #####################

    def test_registration(self):
        """Test User creation through our POST route"""
        with test_database(self.TEST_DB, (User,)):
            rv = self.app.post('/register', data=self.data)
            self.assertEqual(User.select().count(), 1)
            self.assertEqual(User.get().username, 'testUsername')
            self.assertEqual(User.get().email, 'test@example.com')
            self.assertNotEqual(User.get().password, 'password')
            self.assertEqual(rv.status_code, 200)


if __name__ == '__main__':
    unittest.main()
