## Step 7 - Nobody likes an audit, so how do we test a Form?

(1/21/16) There's a few reasons why I've deviated from Kenneth 
Love's project instructions in "Build A Social Network With Flask" 
course, and none of them have to do at all with it being a bad 
way to go about things. However, for me...

- Some of the joints of the project seemed to be obscured.

- As a student I had a hard time isolating each piece of the stack.

- I needed to break this down to write tests for it later on.

This problem for me becomes most pronounced
when it comes to forms. Forms are designed to rest inside
the routes of our server, so already I run into trouble pulling
them apart. To illistrate what I'm talking about, let's take a 
look at this snippet of source code from the ["Registration View"](https://teamtreehouse.com/library/build-a-social-network-with-flask/takin-names/registration-view) 
video...

```python

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
      flash("Yay, you registered!", "success")
      models.User.create_user(username = form.username.data,
                              email = form.email.data, 
                              password = form.password.data)
      return redirect(url_for('index'))
    return render_template('register.html', form=form)
    
```

So, looking at this, I can see that ```validate_on_submit()``` seems
to be a method that returns a ```True``` value when a form is valid.
I can also see that our ```form``` variable comes from our form
import, and that ```RegisterForm()``` seems to be from that. If you know
even more, you know that we're going to write ```RegisterForm```, and
that class is what we're testing. 


Question:


- Where is our data being entered into ```forms.RegsiterForm()```?


Answer:


- flask-wtf inserts our request.form data automatically from flask. [See the docs](https://flask-wtf.readthedocs.org/en/latest/quickstart.html#validating-forms).


If you're like me, this is where you start to cuss. If flask is
automatically passing this request data to flask-wtf (or flask-wtf
is automatically pulling this data from flask, however you want to 
look at it), then it suddenly puts a kink in us trying to isolate
our form test from the server test. I don't like that. 

Unfortunately, I couldn't become a lazy developer and just mimic
one of Kenneth's tacocat tests, because he didn't isolate his
form tests. I really didn't find much in [flask-wtf docs](https://flask-wtf.readthedocs.org/en/latest/index.html), 
[wtforms docs](https://wtforms.readthedocs.org/en/latest/index.html), [flask's special docs for testing applications](http://flask.pocoo.org/docs/0.10/testing/), 
or google either.

What did help for ideas were our previous tests for the server that
used a test database. So, with a willingness to roll up my sleeves 
and get dirty, I started a ```_form_tests.py``` file, and started down
a small, uncharted territory...


### 1. The Architecture of a test


What I really needed, because of the flask / flask-wtf link, was
a clean, mock test route to stick a form into and test against.
I knew that we had created a test client before in our server
tests, and after digging around in [flask's special docs for testing applications](http://flask.pocoo.org/docs/0.10/testing/),
I was fairly certain I could create an adaquete mock server.
So I started up a python shell and started playing around...

```python
(vpython)Nicolass-MacBook-Pro:GameProject nicolasjhampton$ python
Python 3.5.0 (#################, Sep 12 2015, 11:00:19) 
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from flask import Flask
>>> from models import User
>>> setupTestApp = Flask(__name__)
>>> setupTestApp.config['TESTING'] = True
>>> setupTestApp.config['WTF_CSRF_ENABLED'] = False
>>> testApp = setupTestApp.test_client()
>>> @testApp.route('/', methods=['POST'])
... def test_route():
...     return True
... 
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'FlaskClient' object has no attribute 'route'
```

Eh, hit a wall. Seems as though I can't attach a route to 
the test client. At first, I thought it was because of the 
decorator syntax or something, but that really shouldn't be
the problem here. What's really going on is that I shouldn't
be attaching the route to the FlaskClient object, but to 
```setupTestApp```, the Flask object we attached to the FlaskClient. 
I try again...


```python
(vpython)Nicolass-MacBook-Pro:GameProject nicolasjhampton$ python
Python 3.5.0 (v#################, Sep 12 2015, 11:00:19) 
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from flask import Flask
>>> from models import User
>>> setupTestApp = Flask(__name__)
>>> @setupTestApp.route('/', methods=['POST'])
... def test_route():
...     return True
... 
>>> setupTestApp.config['TESTING'] = True
>>> setupTestApp.config['WTF_CSRF_ENABLED'] = False
>>> testApp = setupTestApp.test_client()
>>> data = {'username': 'testUsername','email': 'test@example.com','password': 'password','password2': 'password'}
>>> response = testApp.post('/', data=data)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/nicolasjhampton/GitHub/vpython/lib/python3.5/site-packages/werkzeug/test.py", line 788, in post
    return self.open(*args, **kw)
  File "/Users/nicolasjhampton/GitHub/vpython/lib/python3.5/site-packages/flask/testing.py", line 108, in open
    follow_redirects=follow_redirects)
  
  # ...a whole crapload of other stuff I don't understand...
  
  File "/Users/nicolasjhampton/GitHub/vpython/lib/python3.5/site-packages/werkzeug/wrappers.py", line 847, in force_type
    response = BaseResponse(*_run_wsgi_app(response, environ))
  File "/Users/nicolasjhampton/GitHub/vpython/lib/python3.5/site-packages/werkzeug/wrappers.py", line 57, in _run_wsgi_app
    return _run_wsgi_app(*args)
  File "/Users/nicolasjhampton/GitHub/vpython/lib/python3.5/site-packages/werkzeug/test.py", line 871, in run_wsgi_app
    app_rv = app(environ, start_response)
TypeError: 'bool' object is not callable
```


Soooo, WTF???!!! None of these errors seem to lead back to 
our file! Lesson to learn: try not to make errors sound 
more complicated than they are. Let's look at the last 
line of the error...


```TypeError: 'bool' object is not callable```


What's the only boolean I'm really 'calling'? Could it
be the route's return value of True? 


```python
>>> @setupTestApp.route('/', methods=['POST'])
... def test_route():
...     return True
```


Maybe I can't return a boolean from a route? Let's try
again...


```python
(vpython)Nicolass-MacBook-Pro:GameProject nicolasjhampton$ python
Python 3.5.0 (v##################, Sep 12 2015, 11:00:19) 
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from flask import Flask
>>> from models import User
>>> setupTestApp = Flask(__name__)
>>>  @setupTestApp.route('/', methods=['POST'])
  File "<stdin>", line 1
    @setupTestApp.route('/', methods=['POST'])
    ^
IndentationError: unexpected indent
>>> @setupTestApp.route('/', methods=['POST'])
... def test_route():
...     return "The Bus"
... 
>>> setupTestApp.config['TESTING'] = True
>>> setupTestApp.config['WTF_CSRF_ENABLED'] = False
>>> testApp = setupTestApp.test_client()
>>> data = {'username': 'testUsername','email': 'test@example.com','password': 'password','password2': 'password'}
>>> response = testApp.post('/', data=data)
>>>
```


Sweet, we've got a response! Now what the heck is in there?


```python
>>> dir(response)
['__call__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_ensure_sequence', '_get_mimetype_params', '_on_close', '_status', '_status_code', 'accept_ranges', 'add_etag', 'age', 'allow', 'autocorrect_location_header', 'automatically_set_content_length', 'cache_control', 'calculate_content_length', 'call_on_close', 'charset', 'close', 'content_encoding', 'content_language', 'content_length', 'content_location', 'content_md5', 'content_range', 'content_type', 'data', 'date', 'default_mimetype', 'default_status', 'delete_cookie', 'direct_passthrough', 'expires', 'force_type', 'freeze', 'from_app', 'get_app_iter', 'get_data', 'get_etag', 'get_wsgi_headers', 'get_wsgi_response', 'headers', 'implicit_sequence_conversion', 'is_sequence', 'is_streamed', 'iter_encoded', 'last_modified', 'location', 'make_conditional', 'make_sequence', 'mimetype', 'mimetype_params', 'response', 'retry_after', 'set_cookie', 'set_data', 'set_etag', 'status', 'status_code', 'stream', 'vary', 'www_authenticate']
```


Typical response. ```get_data()``` seems like a sure bet...


```python
>>> response.get_data()
b'The Bus'
```


'The Bus'. That's great! That's what I sent. Except for that 
```b``` right before it. For those that don't know, that 
indicates a byte type. Not trying to work with a byte type.
Let's string that up...


```python
>>> str(response.get_data())
"b'True'"
>>> str(response.data)
"b'True'"
```


Alright. Not exactly what I want, but if I wanted to test for
The Bus...


```python
>>> 'Bus' in str(response.data)
True
```


BOOM! Something testable. Let's think on this for a sec, then
try to make this into something useful...


```python
Python 3.5.0 (v##################, Sep 12 2015, 11:00:19) 
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from flask import Flask
>>> setupTestApp = Flask(__name__)
>>> @setupTestApp.route('/', methods=['POST'])
... def test_route():
...     return str(True)
... 
>>> setupTestApp.config['TESTING'] = True
>>> setupTestApp.config['WTF_CSRF_ENABLED'] = False
>>> testApp = setupTestApp.test_client()
>>> data = {'username': 'testUsername','email': 'test@example.com','password': 'password','password2': 'password'}
>>> response = testApp.post('/', data=data)
>>> 'True' in str(response.data)
True
```


Oh, that's pretty much our test. By this point, it's just a
little rearraigning here and there, replacing a boolean with
a expression that returns a boolean, and...


```python

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
        """Test that our form rejects usernames that are too short"""
        self.data['username'] = 'bob'
        response = self.testApp.post('/', data=self.data)
        assert 'False' in str(response.data)
        
if __name__ == '__main__':
    unittest.main()     

```


Alright. I think that's set up, but I don't expect to get any
good results until I have a [forms.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/bfcb671b178d31f9e2f62f8428d6213bc02bb8f1/forms.py) file to import, so let's
quick set up the boilerplate. I originally went to the [wtforms docs](https://wtforms.readthedocs.org/en/latest/fields.html#field-definitions)
to try and reason what would be the absolute least amount of info I
needed to make a form, but ultimately found Kenneth's [Flask-WTF](https://teamtreehouse.com/library/build-a-social-network-with-flask/takin-names/flaskwtf-forms)
class to give the clearest answer...


```python

from flask_wtf import Form
from wtforms import PasswordField, StringField

from models import User

class RegistrationForm(Form):
    username = StringField('username')
    email = StringField('email')
    password = PasswordField('password') 
    password2 = PasswordField('password2')
    
```


Seems right, right??? Nothing to do but to run the [_form_tests.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/bfcb671b178d31f9e2f62f8428d6213bc02bb8f1/_form_tests.py) file and see...


```
(vpython)Nicolass-MacBook-Pro:GameProject nicolasjhampton$ python _form_tests.py
F
======================================================================
FAIL: test_username_min_length_validation (__main__.FormTestCase)
Test that our form rejects invalid usernames
----------------------------------------------------------------------
Traceback (most recent call last):
  File "_form_tests.py", line 35, in test_username_min_length_validation
    assert 'False' in str(response.data)
AssertionError

----------------------------------------------------------------------
Ran 1 test in 0.058s

FAILED (failures=1)
```


Perfect! Now, just to be sure, I'm going to see if we got 
our other possible boolean answer by changing our final
assertion from ```assert 'False' in str(response.data)``` to 
```assert 'False' in str(response.data)```, and...


```
(vpython)Nicolass-MacBook-Pro:GameProject nicolasjhampton$ python _form_tests.py
.
----------------------------------------------------------------------
Ran 1 test in 0.098s

OK
```


Great! So our test is sending a boolean for each case, we're
testing from as simple an enviornment as we can, and we're ready
to write some code. I'm going to make a few more tests in [_form_tests.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/bed17c290be272fda1cfd8a4bc5b490156be68be/_form_tests.py) 
to test all our other fields in the forms.py file. Take a 
look if you want, but a lot of it looks pretty repeative. 


### 2. How does a form work with the database?


My goal with these 8 tests is to make fields that only validate
after satisfying certain constraints:


- Usernames have to be over 3 and under 50 ascii characters 

- Emails have to be present and be in email format

- Password have to be over 6 and under 20 characters

- password2 has to match password


However, I do have two  other requirements...


- Usernames have to be unique in the database

- Emails have to be unique in the database


and two extra tests commented out:


```python

    def test_email_duplicate_validation(self):
        """Test that our form rejects duplicate emails"""
        # Don't know what to put here yet
        response = self.testApp.post('/', data=self.data)
        assert 'False' in str(response.data)
    
    def test_username_duplicate_validation(self):
        """Test that our form rejects duplicate usernames"""
        # Don't know what to put here yet
        response = self.testApp.post('/', data=self.data)
        assert 'False' in str(response.data)
    
```


These last two tests in [_form_tests.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/bed17c290be272fda1cfd8a4bc5b490156be68be/_form_tests.py) are supposed to make sure our username
and email fields won't allow duplicates of other entries in
the database. In order to make that test, though, we need a 
greater understanding not only of the form itself, but
how it interacts with the database. For now, I'm putting 
these two off while I satisfy the rest of my constraints.

Again, I referred to instructions in Kenneth's [Flask-WTF](https://teamtreehouse.com/library/build-a-social-network-with-flask/takin-names/flaskwtf-forms)
class to create my ```RegistrationForm()``` class in [_forms.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/bed17c290be272fda1cfd8a4bc5b490156be68be/forms.py),
adding each constraint one at a time, then running my tests to
make sure that each constraint did what I wanted it to do. 


Wait, couldn't these constraints fill in our plan?...


- I'll design the database table that stores the user data... (done)

    1. I need to create and delete a User Table (done)
        * I'll write 2 tests for this (done)
            - Test that the User table exists (done)
            - Test that the User table can be dropped  (done)
    
    3. I need to be able to create, retrieve, and delete User entries (done)
        * I'll write a few tests for this (done)
            - Test that User entries exist and can be recalled by username and email (done)
            - Test that each entry is uniquely defined by a user_id (done)
    
    2. I need to preserve the integrity of the User Table (done)
        * This will involve testing values and possible errors (done)
            - Test that passwords are stored, hashed, and comparable (done)
            - Test that errors are thrown for data limits (done)


- ...then add login,logout, and password hash information to that database. (mostly done)

    1. Use B-crypt to hash the password stored in our User model (done)
        * I'll start this by writing 2 tests (done)
            - one to check the password is hashed (done)
            - another to check we can check a hashed password entry against it (done)
            
    2. Use flask-login User mixin to check login id and status (kinda done)
        *  I'll write a few tests (not sure how many, at least 2) (done)
            - one to check a user id is present after user creation (done)
            - **another to check a login status (in or out) is present (pushing this to later)**


- By then, I can build the flask server that will serve our first route... (Done)

    1. There will be a url to get to a register page (Done)
        * We can test for basic connectivity (Done)
            - We need a 200 response from our /register GET route (Done)
            - We need a status code response from our /register POST route (Done)
           
    2. Connect our POST route to our database (Done)
        * We can test that flask received our data in the request object (Done)
        * We can test that flask is connected to the database during our request (Done)
        * We can test that flask stored the data we received (Done)
            
            
- ...and a form to validate the registration data sent via post...
     
     1. Our user form will validate our user information upon submission
        * We have to test all our built in validators (Done)
            - Usernames have to be over 3 and under 50 ascii characters (Done) 
            - Emails have to be present and be in email format (Done)
            - Password have to be over 6 and under 20 characters (Done)
            - password2 has to match password (Done)
        * We have to test our custom validators (Where we are now)
            - Usernames have to be unique in the database
            - Emails have to be unique
        
        
- ...from the HTML registration screen that creates new users.

    1. We need a register prompt (oh, this makes sense)
        * We can test for the presence of username, email, and password fields
        * We can test... (Blah blah blah)


Our partial plan is getting to be a more complete set of instructions
for how to work our way from the back-end to the front...

Watching the video, I realized that we have to create our own
validator functions in order to check for duplicates in the database,
and that requires importing the User model. In order to mock this,
I think we can use the ```test_database``` method from our playhouse
package to create a test database to query against for our tests...

with a little work to our ```setUp``` method...


```python

    def setUp(self):
        self.TEST_DB = SqliteDatabase(':memory:')
        self.TEST_DB.connect()
        self.TEST_DB.create_tables([User], safe=True)
        """Data designed to pass that we can modify to fail. Reset each test."""
        self.data = {
            'username': 'testUsername',
            'email': 'test@example.com',
            'password': 'password',
            'password2': 'password'
        }
        self.data2 = {
            'username': 'testUsername2',
            'email': 'test2@example.com',
            'password': 'password',
            'password2': 'password'
        }
        with test_database(self.TEST_DB, (User,)):
            User.create_user(username=self.data2['username'],
                                    email=self.data2['email'],
                                    password=self.data2['password'])
        self.testApp = self.setupTestApp.test_client()

```


and some work to our tests to bring reality to our theories...


```python

    def test_email_duplicate_validation(self):
        """Test that our form rejects duplicate emails"""
        self.data2['username'] = 'uniqueusername'
        with test_database(self.TEST_DB, (User,)):
            response = self.testApp.post('/', data=self.data2)
            assert 'False' in str(response.data)
    
    def test_username_duplicate_validation(self):
        """Test that our form rejects duplicate usernames"""
        self.data2['email'] = 'email@unique.com'
        with test_database(self.TEST_DB, (User,)):
            response = self.testApp.post('/', data=self.data2)
            assert 'False' in str(response.data)
            
```


...write some code to enable us to access the database from
within our form...


```python

#This import is how the form accesses the database
from models import User

def username_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that username already exists.')

def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')
```


and run our tests...

But here's the thing. It didn't work. 

I still couldn't get the tests to pass, and I'm pretty certain
it's because I could never get the form to reference the mocked
test database. Instead, the form is creating it's own database 
and referencing that, which would kind of be correct in a real world
instance. I decided to scrap the mock database for now and 
just use the real one (which is really our development db,
but this setup still limits our ability to test production
code...)


```python

from flask import Flask
from peewee import *
from playhouse.test_utils import test_database
import unittest

import forms
import models


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
        # self.TEST_DB = SqliteDatabase(':memory:')
        # self.TEST_DB.connect()
        # self.TEST_DB.create_tables([User], safe=True)
        models.DATABASE.connect()
        models.DATABASE.create_tables([models.User], safe=True)
        """Data designed to pass that we can modify to fail. Reset each test."""
        self.data = {
            'username': 'testUsername',
            'email': 'test@example.com',
            'password': 'password',
            'password2': 'password'
        }
        self.data2 = {
            'username': 'testUsername2',
            'email': 'test2@example.com',
            'password': 'password',
            'password2': 'password'
        }
        # with test_database(self.TEST_DB, (User,)):
        models.User.create_user(username=self.data2['username'],
                                email=self.data2['email'],
                                password=self.data2['password'])
        self.testApp = self.setupTestApp.test_client()
        
    def tearDown(self):
        models.User.delete().execute()
        models.DATABASE.close()
    
    #Username has to be over 3 and under 50 ascii characters, and unique
        
    def test_username_min_length_validation(self):
        """Test that our form rejects invalid usernames"""
        self.data['username'] = 'bob'
        response = self.testApp.post('/', data=self.data)
        assert 'False' in str(response.data)
        
    def test_username_max_length_validation(self):
        """Test that our form rejects invalid usernames"""
        self.data['username'] = 'b'*52
        response = self.testApp.post('/', data=self.data)
        assert 'False' in str(response.data)
        
    def test_username_ascii_validation(self):
        """Test that our form rejects invalid usernames"""
        self.data['username'] = '********'
        response = self.testApp.post('/', data=self.data)
        assert 'False' in str(response.data)
        
    def test_email_at_validation(self):
        """Test that our form rejects emails without at symbols"""
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
        #with test_database(self.TEST_DB, (User,)):
        response = self.testApp.post('/', data=self.data2)
        assert 'False' in str(response.data)
    
    def test_username_duplicate_validation(self):
        """Test that our form rejects duplicate usernames"""
        self.data2['email'] = 'email@unique.com'
        #with test_database(self.TEST_DB, (User,)):
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
        
```


Using this implementation and running the tests gave us the
passing tests we should have gotten before.


```
(vpython)Nicolass-MacBook-Pro:GameProject nicolasjhampton$ coverage run _form_tests.py
..........
----------------------------------------------------------------------
Ran 10 tests in 5.917s

OK
```

And 100% coverage. Well, that took a little more than expected.
I might go back later and try working out the bugs in the 
mock database, just so I don't rewrite the database everytime
I test the forms, but for now, this will work, and pretty well
considering I had no how to do it.

We'll have to actually use this form and clean up our route in
[Step 8...](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/master/blog/step8.md)






