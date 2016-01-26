## Step 6 - I HAVE DATA!!! Uh, now what do I do with it?

(1/20/16) I know we have this data object that is coming in
from our POST request. I know we have a database that we
can store this data in. I also know that...

- flask received our data...

- connects to the database, and

- stores the data we recevied


Wait, I actually don't know any of that! Yeah, none of that 
is happening, and I live in a dream world. But I could tell 
you the sky is falling, and if you didn't test it you might 
believe me, so we have to...


- (test that) flask received our data...

- (test that the data flask received is valid)

- (test that it) connects to the database, and

- (test that it) stores the data we recevied


Yeah, I'm skipping that form part for a second. (No, I'm not
sure if I can skip forms right now and make this work, but I'd 
rather try to start this as simple as possible.) We can go 
ahead and plug this into our plan now.


- By then, I can build the flask server that will serve our first route... (Uh, yeah, sure, let's do this)

    1. There will be a url to get to a register page 
        * We can test for basic connectivity (Done)
            - We need a 200 response from our /register GET route (Done)
            - We need a status code response from our /register POST route (Done)
           
    2. Connect our POST route to our database
        * We can test that flask received our data in the request object (Where we are now)
        * We can test that flask is connected to the database during our request
        * We can test that flask stored the data we received
            
- Forms
     
     1. Our user form will validate our user information upon submission
        * We can test that the User data is in valid format
        
        (blah blah blah...)
        

### 1. Testing that the data showed up


I found myself a little stumped as to what could be a
testable sign that the server had received our data, so I
went back to the tests for Kenneth's tacocat project. I didn't
find my eventual strategy in the user tests, however. It 
was in the tests for the tacos...

```python

    def test_taco_create(self):
        taco_data = {
            'protein': 'chicken',
            'shell': 'flour',
            'cheese': False,
            'extras': 'Gimme some guac.'
        }
        with test_database(TEST_DB, (User, Taco)):
            UserModelTestCase.create_users(1)
            self.app.post('/login', data=USER_DATA)

            taco_data['user'] = User.select().get()
            rv = self.app.post('/taco', data=taco_data)
            self.assertEqual(rv.status_code, 302)
            self.assertEqual(rv.location, 'http://localhost/')
            self.assertEqual(Taco.select().count(), 1)
            
```


Why waste time testing if flask got our information??? Flask
is our inbetween for the user and the database. Let's just 
check the database! So... 


```python

    def test_user_create(self):
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
            
```


Now, with this test looking only one line away from our 
```test_registration``` test in [_server_tests.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/cb14fba931e43fcfcf12e4faf7e10a42a16e73d7/_server_tests.py), I think
it would be perfectly acceptable to combine the two...


```python

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
            
```


Perfect! The test is designed to test everything in our objectives
for the database connection, and a little more...


    2. Connect our POST route to our database
        * We can test that flask received our data in the request object (Where we are now)
        * We can test that flask is connected to the database during our request
        * We can test that flask stored the data we received
        

And the test fails just like it should...


```
(vpython)Nicolass-MacBook-Pro:GameProject nicolasjhampton$ coverage run _server_tests.py
.F
======================================================================
FAIL: test_registration (__main__.AppTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "_server_tests.py", line 62, in test_registration
    self.assertEqual(User.select().count(), 1)
AssertionError: 0 != 1

----------------------------------------------------------------------
Ran 2 tests in 0.195s

FAILED (failures=1)
```


So let's go make a User count in our table go from zero to one!


### 2. Making the User instance in the database from POST


A couple things about doing this you should review from 
Kenneth's "Build A Social Network With Flask" course:

- We open the database connection with flask's ```before_request``` decorator method

- We attach the database to flask's ```g``` global object inside ```before_request```

- Then the route is ran. The route accesses the database on the ```g``` object

- After the route is ran, flask's ```after_request``` method takes the response, closes the database connection, and returns the ```response```


(This is all in [this video](https://teamtreehouse.com/library/build-a-social-network-with-flask/takin-names/before-and-after-requests))


Why am I reviewing this step by step for you? Because I wanted
to illistrate the amount of code we've written a test for. That's 
a fairly large process, but the all the flask parts have been 
tested by the developers of flask. We just need to test that 
when we put them together, we get the one result that we
want. The before and after are pretty boilerplate, and
there's a few new imports we have to bring into our server,
including our User model and flask's ```request``` object to get
our post data. That said, our POST route alone
looks something like this...


```python

@app.route('/register', methods=['POST'])
def post_registration():
    """POST route for our register page to create a User"""
    userinfo = dict(request.form.items()) # The request.form attribute returns an immutable multidict object
    
    models.User.create_user(username= userinfo.username,
                            email= userinfo.email,
                            password= userinfo.password)
    return "{} is now Registered!".format(models.User.get(email = userinfo.email))
    
```


Then I ran my tests...


```
(vpython)Nicolass-MacBook-Pro:GameProject nicolasjhampton$ coverage run _server_tests.py
.E
======================================================================
ERROR: test_registration (__main__.AppTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "_server_tests.py", line 61, in test_registration
    rv = self.app.post('/register', data=data)
  File "/Users/nicolasjhampton/GitHub/vpython/lib/python3.5/site-packages/werkzeug/test.py", line 788, in post
    return self.open(*args, **kw)
  File "/Users/nicolasjhampton/GitHub/vpython/lib/python3.5/site-packages/flask/testing.py", line 108, in open
    follow_redirects=follow_redirects)
  File "/Users/nicolasjhampton/GitHub/vpython/lib/python3.5/site-packages/werkzeug/test.py", line 751, in open
    response = self.run_wsgi_app(environ, buffered=buffered)
  File "/Users/nicolasjhampton/GitHub/vpython/lib/python3.5/site-packages/werkzeug/test.py", line 668, in run_wsgi_app
    rv = run_wsgi_app(self.application, environ, buffered=buffered)
  File "/Users/nicolasjhampton/GitHub/vpython/lib/python3.5/site-packages/werkzeug/test.py", line 871, in run_wsgi_app
    app_rv = app(environ, start_response)
  File "/Users/nicolasjhampton/GitHub/vpython/lib/python3.5/site-packages/flask/app.py", line 1836, in __call__
    return self.wsgi_app(environ, start_response)
  File "/Users/nicolasjhampton/GitHub/vpython/lib/python3.5/site-packages/flask/app.py", line 1820, in wsgi_app
    response = self.make_response(self.handle_exception(e))
  File "/Users/nicolasjhampton/GitHub/vpython/lib/python3.5/site-packages/flask/app.py", line 1403, in handle_exception
    reraise(exc_type, exc_value, tb)
  File "/Users/nicolasjhampton/GitHub/vpython/lib/python3.5/site-packages/flask/_compat.py", line 33, in reraise
    raise value
  File "/Users/nicolasjhampton/GitHub/vpython/lib/python3.5/site-packages/flask/app.py", line 1817, in wsgi_app
    response = self.full_dispatch_request()
  File "/Users/nicolasjhampton/GitHub/vpython/lib/python3.5/site-packages/flask/app.py", line 1477, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/Users/nicolasjhampton/GitHub/vpython/lib/python3.5/site-packages/flask/app.py", line 1381, in handle_user_exception
    reraise(exc_type, exc_value, tb)
  File "/Users/nicolasjhampton/GitHub/vpython/lib/python3.5/site-packages/flask/_compat.py", line 33, in reraise
    raise value
  File "/Users/nicolasjhampton/GitHub/vpython/lib/python3.5/site-packages/flask/app.py", line 1475, in full_dispatch_request
    rv = self.dispatch_request()
  File "/Users/nicolasjhampton/GitHub/vpython/lib/python3.5/site-packages/flask/app.py", line 1461, in dispatch_request
    return self.view_functions[rule.endpoint](**req.view_args)
  File "/Users/nicolasjhampton/GitHub/GameProject/server.py", line 34, in post_registration
    models.User.create_user(username= userinfo.username,
AttributeError: 'dict' object has no attribute 'username'

----------------------------------------------------------------------
Ran 2 tests in 0.269s

FAILED (errors=1)
```


Aaannnd... I forget how to properly access data structures.

Me say Dictionaries good.```userinfo.username``` bad. ```userinfo['email']``` good.

How did I figure that out? I threw ```import pdb; pdb.set_trace()``` inside the route
and checked the variable.


```
(vpython)Nicolass-MacBook-Pro:GameProject nicolasjhampton$ coverage run _server_tests.py
.> /Users/nicolasjhampton/GitHub/GameProject/server.py(35)post_registration()
-> models.User.create_user(username= userinfo.username,
(Pdb) dir(userinfo)
['__class__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values']
(Pdb) userinfo
{'email': 'test@example.com', 'username': 'testUsername', 'password': 'password', 'password2': 'password'}
(Pdb) userinfo.username
*** AttributeError: 'dict' object has no attribute 'username'
(Pdb) userinfo['username']
'testUsername'
(Pdb) quit()
```


Well, that was simple. Let's make that syntax change and try this again...


```
(vpython)Nicolass-MacBook-Pro:GameProject nicolasjhampton$ coverage run _server_tests.py
..
----------------------------------------------------------------------
Ran 2 tests in 0.740s

OK
```


BOOM! 2 tests passed and 95% test coverage. We can cross off a
few of these items here...


    2. Connect our POST route to our database (Freakin' DONE yo!)
        * We can test that flask received our data in the request object (Done)
        * We can test that flask is connected to the database during our request (Done)
        * We can test that flask stored the data we received (Done)
        

Told ya we'd start to move faster later on.
        
Moving on to [step # 7, forms...](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/master/blog/step7.md)





