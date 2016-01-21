from flask import Flask
import unittest

import forms
from models import User

class FormTestCase(unittest.TestCase):

    setupTestApp = Flask(__name__)
    setupTestApp.config['TESTING'] = True
    setupTestApp.config['WTF_CSRF_ENABLED'] = False
    
    @setupTestApp.route('/', methods=['POST'])
    def sample_route():
        """Test route returns string of boolean value for if form does/does not validate"""
        form = forms.RegistrationForm()
        return str(form.validate_on_submit())

    def setUp(self):
        self.testApp = self.setupTestApp.test_client()
        """Data designed to pass that we can modify to fail. Reset each test."""
        self.data = {
            'username': 'testUsername',
            'email': 'test@example.com',
            'password': 'password',
            'password2': 'password'
        }
    
    #Username has to be over 3 and under 50 ascii characters, and unique
        
    def test_username_min_length_validation(self):
        """Test that our form rejects invalid usernames"""
        self.data['username'] = 'bob'
        response = self.testApp.post('/', data=self.data)
        assert 'False' in str(response.data)
        
if __name__ == '__main__':
    unittest.main()
        
        
        
#Username has to be over 3 and under 50 ascii characters, and unique

#email has to be present and be in email format, and unique

#password has to be over 6 and under 20 characters

#password2 has to match password
        
    # def test_username_max_length_validation(self):
    #     """Test that our form rejects invalid usernames"""
    #     self.data['username'] = 'b'*52
    #     with test_database(self.TEST_DB, (User,)):
        
    # def test_username_ascii_validation(self):
    #     """Test that our form rejects invalid usernames"""
    #     self.data['username'] = '********'
    #     with test_database(self.TEST_DB, (User,)):
        
    
               
    # def test_email_validation(self):
    #     """Test that our form rejects invalid emails"""
        
    # def test_username_validation(self):
    #     """Test that our form rejects invalid usernames"""
        
    
        