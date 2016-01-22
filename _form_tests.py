from flask import Flask
from peewee import *
from playhouse.test_utils import test_database
import unittest

import forms
import models


class FormTestCase(unittest.TestCase):
    """Test suite for our RegistrationForm class"""
    
    
    #####################
    # test conditions
    ##################### 
    
    
    setupTestApp = Flask(__name__)
    setupTestApp.config['TESTING'] = True
    setupTestApp.config['WTF_CSRF_ENABLED'] = False
    
    @setupTestApp.route('/', methods=['POST'])
    def sample_route():
        """Mock route returns string of boolean value for if form does/does not validate"""
        form = forms.RegistrationForm()
        return str(form.validate_on_submit())

    def setUp(self):
        """Connects to the database, creates tables, defines two sets of mock
           user info, creates a mock user and a test client before every test"""
        models.DATABASE.connect()
        models.DATABASE.create_tables([models.User], safe=True)
        # Data designed to pass that we can modify to fail. Reset each test.
        self.data = {
            'username': 'testUsername',
            'email': 'test@example.com',
            'password': 'password',
            'password2': 'password'
        }
        # Data2 is a mock user entered into database for duplicate entry tests
        self.data2 = {
            'username': 'testUsername2',
            'email': 'test2@example.com',
            'password': 'password',
            'password2': 'password'
        }
        models.User.create_user(username=self.data2['username'],
                                email=self.data2['email'],
                                password=self.data2['password'])
        # run test client
        self.testApp = self.setupTestApp.test_client()
        
    def tearDown(self):
        """Deletes the user created and closes the database after every test"""
        models.User.delete().execute()
        models.DATABASE.close()
        
        
    #####################
    # Error tests
    ##################### 
    
        
    def test_username_min_length_validation(self):
        """Test that our form rejects usernames that are too short (3 characters or less)"""
        self.data['username'] = 'bob'
        response = self.testApp.post('/', data=self.data)
        assert 'False' in str(response.data)
        
    def test_username_max_length_validation(self):
        """Test that our form rejects usernames that are too long (over 50 characters)"""
        self.data['username'] = 'b'*52
        response = self.testApp.post('/', data=self.data)
        assert 'False' in str(response.data)
        
    def test_username_ascii_validation(self):
        """Test that our form rejects usernames with non-ascii characters"""
        self.data['username'] = '********'
        response = self.testApp.post('/', data=self.data)
        assert 'False' in str(response.data)
        
    def test_email_at_validation(self):
        """Test that our form rejects emails without an @ symbol"""
        self.data['email'] = 'noatcharacter.com'
        response = self.testApp.post('/', data=self.data)
        assert 'False' in str(response.data)
        
    def test_email_domain_validation(self):
        """Test that our form rejects emails without domain names"""
        self.data['email'] = 'nodomain@inemail'
        response = self.testApp.post('/', data=self.data)
        assert 'False' in str(response.data)
        
    def test_email_duplicate_validation(self):
        """Test that our form rejects duplicate emails"""
        self.data2['username'] = 'uniqueusername'
        response = self.testApp.post('/', data=self.data2)
        assert 'False' in str(response.data)
    
    def test_username_duplicate_validation(self):
        """Test that our form rejects duplicate usernames"""
        self.data2['email'] = 'email@unique.com'
        response = self.testApp.post('/', data=self.data2)
        assert 'False' in str(response.data)
    
    def test_password_min_length_validation(self):
        """Test that our form rejects short passwords (under 7 characters)"""
        self.data['password'] = 'sixsix'
        self.data['password2'] = 'sixsix'
        response = self.testApp.post('/', data=self.data)
        assert 'False' in str(response.data)
        
    def test_password_max_length_validation(self):
        """Test that our form rejects long passwords (over 20 characters)"""
        self.data['password'] = '22'*11
        self.data['password2'] = '22'*11
        response = self.testApp.post('/', data=self.data)
        assert 'False' in str(response.data)
        
    def test_password_fidelity_validation(self):
        """Test that our form rejects passwords that don't match"""
        self.data['password'] = 'password'
        self.data['password2'] = 'drowssap'
        response = self.testApp.post('/', data=self.data)
        assert 'False' in str(response.data)
        
if __name__ == '__main__':
    unittest.main()
        
    
        