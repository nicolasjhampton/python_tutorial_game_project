# We have to import the unittest library
import unittest

# We'll import our models here. 
import models
                
class UserTableTests(unittest.TestCase):
    """Tests the User table"""
    
    
    #####################
    # test conditions
    ##################### 

    def setUp(self):
        """Runs before every test, creating the User table and one entry if either are not present"""
        models.initialize()
        self.user = models.User.get(email='testEmail@testEmail.com')
                
    def tearDown(self):
        """Runs after every test, deleting the entry from the User table"""
        try:
            models.User.delete().execute()
        except:
            pass
        
        
    #####################
    # CRUD Tests
    ##################### 
    
       
    def test_check_user_table(self):
        """Tests that the User table exists"""
        assert models.User.table_exists()    
        
    
        
    def test_drop_table(self):
        """Tests that the User table can be dropped"""
        models.DATABASE.drop_table(models.User)
        assert models.User.table_exists() == False
        
    def test_delete_user(self):
        """Tests that a User entry can be deleted"""
        models.User.get(username="testUsername").delete_instance()
        with self.assertRaises(Exception):
            models.User.get(username="testUsername").delete_instance()
        
             
          
    def test_username(self):
        """Tests that a User entry can be recalled by username"""
        user = models.User.get(username='testUsername')
        self.assertEqual(user.email, 'testEmail@testEmail.com')
        
        
    def test_email(self):
        """Tests that a User entry can be recalled by email"""
        self.assertEqual(self.user.username, 'testUsername')
        
    # def test_password(self):
    #     """Tests that a User entry can be recalled by email"""
    #     user = models.User.get(username="testUsername")
    #     self.assertEqual(user.password, 'testPassword')
    
    def test_password_hashed(self):
        """Tests that any recalled password is not equal to the original password text (assumed hashed)"""
        self.assertNotEqual(self.user.password, 'testPassword')
        
    def test_password_equality(self):
        """Tests that any recalled password is not equal to the original password text (assumed hashed)"""
        assert self.user.check_password('testPassword')
        
        
        
    def test_user_id_exists(self):
        """Tests that a User entry is created with a user_id property"""
        assert 'id' in dir(self.user)
        
    def test_get_id_exists(self):
        """Tests that a User entry is created with a get_id method for flask-login to use"""
        assert 'get_id' in dir(self.user)

    def test_get_id_result(self):
        """Tests that a User entry's get_id method returns the user id for flask-login to use"""
        assert str(self.user.id) == self.user.get_id()

        
        
    # def test_login_property_exists(self):
    #     """Tests that a User entry is created with a login property"""
    #     user = models.User.get(email='testEmail@testEmail.com')
    #     assert 'loggedin' in dir(user)

    # def test_login_property_truthy(self):
    #     """Tests that the login property is either True or False"""
    #     user = models.User.get(email='testEmail@testEmail.com')
    #     assert user.loggedin in [True, False]

    # def test_user_id_property_exists(self):
    #     """Tests that a User entry is created with a user_id property"""
    #     user = models.User.get(email='testEmail@testEmail.com')
    #     assert 'user_id' in dir(user)
            
    
    #####################
    # Error tests
    #####################   
    
    def test_table_safe(self):
        """Tests the database to check that a duplicate User table cannot be created"""
        with self.assertRaises(models.OperationalError):
            models.DATABASE.create_table(models.User)
 
    def test_entry_repeat_username(self):
        """Tests the unique constrant placed on the username field of our User model"""
        with self.assertRaises(ValueError):
            models.User.create_user(
                username='testUsername',
                email='Email@testEmail.com',
                password='testPassword')
                
    def test_entry_repeat_email(self):
        """Tests the unique constrant placed on the email field of our User model"""
        with self.assertRaises(ValueError):
            models.User.create_user(
                username='Username',
                email='testEmail@testEmail.com',
                password='testPassword')
                
    def test_username_max_length_limit(self):
        """Tests the length limit placed on the username field of our User model"""
        with self.assertRaises(ValueError):
            models.User.create_user(
                username='u'*51,
                email='Email@testEmail.com',
                password='testPassword')
           
    def test_password_max_length_limit(self):
        """Tests the length limit placed on the password field of our User model"""
        with self.assertRaises(ValueError):
            models.User.create_user(
                username='Username',
                email='Email@testEmail.com',
                password='p'*21)
                
    def test_username_min_length_limit(self):
        """Tests the minimum length requirement placed on the username field of our User model"""
        with self.assertRaises(ValueError):
            models.User.create_user(
                username='u'*3,
                email='Email@testEmail.com',
                password='testPassword')
           
    def test_password_min_length_limit(self):
        """Tests the minimum length requirement placed on the password field of our User model"""
        with self.assertRaises(ValueError):
            models.User.create_user(
                username='Username',
                email='Email@testEmail.com',
                password='p'*6)
        

# This is a convention that runs if this module is called
# directly, and not as a dependency of another script
if __name__ == '__main__':
    unittest.main()



