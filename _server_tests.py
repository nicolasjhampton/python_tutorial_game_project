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
        self.login = {
                'username': 'testUsername',
                'password': 'password'
            }

    #####################
    # GET method tests
    #####################

    def test_register_page(self):
        """Test for a 200 status code from our registration's GET route"""
        with test_database(self.TEST_DB, (User,)):
            rv = self.app.get('/register')
            self.assertIn("username", rv.get_data(as_text=True).lower())
            self.assertIn("email", rv.get_data(as_text=True).lower())
            self.assertIn("password", rv.get_data(as_text=True).lower())
            self.assertIn("confirm password", rv.get_data(as_text=True).lower())
            self.assertEqual(rv.status_code, 200)
            
    def test_login_page(self):
        """Test for a 200 status code from our registration's GET route"""
        with test_database(self.TEST_DB, (User,)):
            rv = self.app.get('/login')
            self.assertIn("username", rv.get_data(as_text=True).lower())
            self.assertIn("password", rv.get_data(as_text=True).lower())
            self.assertEqual(rv.status_code, 200)        

    #####################
    # POST method tests
    #####################

    def test_registration(self):
        """Test User creation through our POST route"""
        with test_database(self.TEST_DB, (User,)):
            rv = self.app.post('/register', data=self.data)
            self.assertIn("login", rv.get_data(as_text=True).lower())
            self.assertEqual(User.select().count(), 1)
            self.assertEqual(User.get().username, 'testUsername')
            self.assertEqual(User.get().email, 'test@example.com')
            self.assertNotEqual(User.get().password, 'password')
            self.assertEqual(rv.status_code, 302)

    def test_login(self):
        """Test User creation through our POST route"""
        with test_database(self.TEST_DB, (User,)):
            self.app.post('/register', data=self.data)
            rv = self.app.post('/login', data=self.login)
            # Need something to test login status
            self.assertEqual(rv.status_code, 302)

    def test_bad_username_login(self):
        """Test User creation through our POST route"""
        with test_database(self.TEST_DB, (User,)):
            self.login['username'] = 'badusername'
            self.app.post('/register', data=self.data)
            rv = self.app.post('/login', data=self.login)
            self.assertIn("login", rv.get_data(as_text=True).lower())
            self.assertEqual(rv.status_code, 200)

    def test_bad_email_login(self):
        """Test User creation through our POST route"""
        with test_database(self.TEST_DB, (User,)):
            self.login['email'] = 'bademail@email.com'
            self.app.post('/register', data=self.data)
            rv = self.app.post('/login', data=self.login)
            self.assertIn("login", rv.get_data(as_text=True).lower())
            self.assertEqual(rv.status_code, 302)

    def test_bad_username(self):
        """Test username error through our POST route"""
        self.data['username'] = 'non*ascii*character'
        with test_database(self.TEST_DB, (User,)):
            rv = self.app.post('/register', data=self.data)
            self.assertEqual(User.select().count(), 0)
            self.assertEqual(rv.status_code, 200)

    def test_bad_email(self):
        """Test email error through our POST route"""
        self.data['email'] = 'noatsymbolordomain'
        with test_database(self.TEST_DB, (User,)):
            rv = self.app.post('/register', data=self.data)
            self.assertEqual(User.select().count(), 0)
            self.assertEqual(rv.status_code, 200)

    def test_bad_password(self):
        """Test password error through our POST route"""
        self.data['password'] = 'short'
        self.data['password2'] = 'short'
        with test_database(self.TEST_DB, (User,)):
            rv = self.app.post('/register', data=self.data)
            self.assertEqual(User.select().count(), 0)
            self.assertEqual(rv.status_code, 200)

    def test_bad_password_confirmation(self):
        """Test password confirmation error through our POST route"""
        self.data['password2'] = 'notpassword1'
        with test_database(self.TEST_DB, (User,)):
            rv = self.app.post('/register', data=self.data)
            self.assertEqual(User.select().count(), 0)
            self.assertEqual(rv.status_code, 200)


if __name__ == '__main__':
    unittest.main()
