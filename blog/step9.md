## Step 9 - Rendering Our Template

(1/24/16) Now that the Back-End is ready to take all our information
from users, we can actually build a front end. In Flask, 
this is done with Jinga2's template rendering engine. Really,
it's just glorified HTML with a little inline logic so we
can make a few changes to what would be static files, but 
it gives us a pretty large range with our HTML, and we'll
get a lot of mileage out if it. 

But that's step 2. Step 1 is testing (and step 3 is always
profit.) We can use a pretty simple syntax to test that certain 
words are included in the HTML that's served...


```python

    def test_register_page(self):
        """Test for a 200 status code from our registration's GET route"""
        with test_database(self.TEST_DB, (User,)):
            rv = self.app.get('/register')
            self.assertIn("username", rv.get_data(as_text=True).lower())
            self.assertIn("email", rv.get_data(as_text=True).lower())
            self.assertIn("password", rv.get_data(as_text=True).lower())
            self.assertIn("confirm password", rv.get_data(as_text=True).lower())
            self.assertEqual(rv.status_code, 200)
    
```


Since we already had a test for the register url, I just
added some more requirements to make it test the page content.
```get_data``` is going to return plain text when we add 
the ```as_text``` flag. Even if that plain text is HTML, 
we can still test like plain string text because, basically, 
that's what HTML is. We'll just make sure the text we get
back is coverted to lower case and compare it to the names
of the fields we expect to be on the page. In case you're
wondering, I pulled this from Kenneth Love's Tacocat tests
again. Nothing wrong with that. Read source, read source,
read source, use source.

Now that we can test the registration page, it's time to 
make a registration page that can pass our tests. There's
a whole video called ["Registration View"](https://teamtreehouse.com/library/build-a-social-network-with-flask/takin-names/registration-view) in Kenneth's 
"Build A Social Network With Flask" that covers this exactly.
We use flask's ```render_template``` method to use template
files, and flask automatically is looking for a /templates
folder that contains all the templates for our sites. I'm 
not going to go over the details of templates because, well,
it's covered in class. If you need help on what means 
what, go back to ["Registration View"](https://teamtreehouse.com/library/build-a-social-network-with-flask/takin-names/registration-view) in Kenneth's class. I will say that the ```render_template```
method gets passed our form so it can use it in the POST, 
so make sure to do that. 

If the template does confuse you, know that what's happening
is that we passed the form to the template, and the template
engine is creating the fields from the form, using for loops
to loop over the form attributes, and if statements to check 
the form values. Knowing that, and having written my template,
I run my tests on it, and...

It fails. Can you tell me why?

The tests we've written are looking for the placeholder text that
should be in the form. Since the template went to the form for 
all the values for the placeholder text, whatever is in 
```field.label.text``` is going to be what prints. That's a 
problem the way we wrote the last field in our form...


```python

# Valid confirm password field parameters
    password2 = PasswordField(
        'password2',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ])
        
```


The field.label.text corresponds to that first 'password2' string,
so that's what prints out. We want it to say "Confirm Password", so
in order to pass our tests, we need to go change this in our form
data.

Also, at this point, don't forget to add an ```app.secret_key = 'whateverrandomlongstring'```
line to your server.py file. Maybe soon I'll update this with an 
explanation as to why, but for now, just do what you're told.

With these modifications, we can not pass our simple tests. Run 
```python server.py``` and check out what we've got. It ain't much.
Now is the time to break out the old HTML/CSS skills and really make 
something more out of this. Remember, I'm doing this to make a simple
online RPG. I don't know what you did this for, but I'm going to 
style it with fun and games in mind. 

I'm going to give you the links to my current


[layout.html](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/8a5d958afb09522a911058e13d75ad4f494f43c7/templates/layout.html)
[login.html](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/8a5d958afb09522a911058e13d75ad4f494f43c7/templates/login.html)
[register.html](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/8a5d958afb09522a911058e13d75ad4f494f43c7/templates/register.html)
[macros.html](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/8a5d958afb09522a911058e13d75ad4f494f43c7/templates/register.html)
[application.css](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/8a5d958afb09522a911058e13d75ad4f494f43c7/static/application.css)


files. I also made some new tests in 


[_server_tests.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/8a5d958afb09522a911058e13d75ad4f494f43c7/_server_tests.py)
[_form_tests.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/8a5d958afb09522a911058e13d75ad4f494f43c7/_form_tests.py)


With that out of the way, lets take a look at this new ```login```
route in [server.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/8a5d958afb09522a911058e13d75ad4f494f43c7/server.py)...


```python

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm() # Populate our request.form data into our form 
    if form.validate_on_submit():
        try: # Try to get the user that's trying to log in
            user = models.User.get(username=form.username.data)
        except: # If that fails, do a flash message or something, take us back to login
            pass
        else: # If it succeeds, then check the password using the user method
            if user.check_password_against_hash(form.password.data):
                # if password checks out, then login the user (somehow)
                # later, we'll redirect to the main page
                return redirect(url_for('login'))
    return render_template("login.html", form=form)
    
```


If you took the "Build A Social Network With Flask" course, you'll 
notice that I changed the way we do password verification. Instead of
bringing the entire process to the server level, I made a method on the
database object to compare the hashes internally. I think this is 
a little more secure, since the server has absolutely know idea how
the passwords are compared. Also, if we wanted to increase the rounds,
we could rewrite our database method a little to take a login count, and 
start counting login attempts at the server level, passing the count
as an argument to the method. Just food for thought. Either way, this
avoids importing bcrypt more than we have to.

But now, speaking of the database, now is the time we have to return to
that layer. Going back to ["The UserMixin From Flask-Login"](https://teamtreehouse.com/library/build-a-social-network-with-flask/making-strong-users/the-usermixin-from-flasklogin), and
working our way back up, we're going to add in the ability to use everything
we've built so far to log users in and out of our site. Before we dive
right in, let's go back to our plan...


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
            
    2. I just cut this


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
        
        
- ...from the HTML registration screen that creates new users...

    1. We need a register prompt (Done)
        * We can test for the presence of username, email, and password fields (Done)
        
    2. We need to forward registered users to a login page (Done)
        * We can test for a 302 redirect status code (Done)


- ...to the login page that logs users in.

    1. We need a login page (Done)
        * We can test for the appropreitely labeled fields for... (Done)
            - Username (Done)
            - Password  (Done)
        * We can test for a 200 status code for the GET method on the page (Done)
    
    2. Use flask-login User mixin to check login id and status (Where we are now, again)
        *  I'll write a few tests (not sure how many, at least 2) 
            - one to check a user id is present after user creation (Done)
            - another to check a login status (in or out) is present 
            

I believe I commented out a couple tests earlier on for this, but
they were incomplete because at the time, we really hadn't isolated what
makes the whole login process work. Now, we can kinda see it all as
a successful login works it's way through the stack...

To understand what's going on a little better, I went past the class and
straight to the [Flask-Login Docs](https://flask-login.readthedocs.org/en/latest/), which gives us a rundown of what it
does and doesn't do...


> It will:
>
> Store the active user’s ID in the session, and let you log them in and out easily.
> Let you restrict views to logged-in (or logged-out) users.
> Handle the normally-tricky “remember me” functionality.
> Help protect your users’ sessions from being stolen by cookie thieves.
> Possibly integrate with Flask-Principal or other authorization extensions later on.
>
> However, it does not:
>
> Impose a particular database or other storage method on you. You are entirely in charge of how the user is loaded.
> Restrict you to using usernames and passwords, OpenIDs, or any other method of authenticating.
> Handle permissions beyond “logged in or not.”
> Handle user registration or account recovery.


Flask Login doesn't store a login status directly into the database, we just
have to add the UserMixin class to our model so Flask-Login has 
dedicated hooks to identify database objects with. Flask-Login doesn't 
even require a database, that just how we're choosing to use it.

A really close look at the source of Flask-Login's [login_user()](https://flask-login.readthedocs.org/en/latest/_modules/flask_login.html#login_user)
shows that Flask-Login is retrieving uniquely identifiable information
from whatever object we assign to a user and storing that in a 
session object imported from flask. This session variable inside flask
is keeping track of logins and logouts I believe (unless a cookie is
storing user login information on the client side). This is mostly
being juggled by LoginManager manipulating the session and cookie variables.

So, two of those tests we wrote for the model...


```python

    # def test_login_property_exists(self):
    #     """Tests that a User entry is created with a login property"""
    #     user = models.User.get(email='testEmail@testEmail.com')
    #     assert 'loggedin' in dir(user)

    # def test_login_property_truthy(self):
    #     """Tests that the login property is either True or False"""
    #     user = models.User.get(email='testEmail@testEmail.com')
    #     assert user.loggedin in [True, False]
    
```

are in the wrong place. The database, without modification, doesn't
store any login, logout information. That's done in the session variable
in flask by flask-login. The other two tests, as we can see, are duplicates
of tests we already have. We just need to modify the tests we have to 
accomodate the slight changes flask-login's UserMixin makes to their
returned values, since our new ```get_id``` method will return a string and
not an integer...


```python

    def test_get_id_exists(self):
        """Tests that a User entry is created with a get_id method"""
        assert 'get_id' in dir(self.user)

    def test_get_id_result(self):
        """Tests that a User entry's get_id method returns the user id"""
        assert self.user.id == self.user.get_id()

    # def test_get_id_result(self):
    #     """Tests that a User entry's get_id method returns
    #        the user id in string format for flask-login to use"""
    #     assert str(self.user.id) == self.user.get_id()

    

    # def test_user_id_property_exists(self):
    #     """Tests that a User entry is created with a user_id property"""
    #     user = models.User.get(email='testEmail@testEmail.com')
    #     assert 'user_id' in dir(user)

```

Once we add the UserMixin class to our model, these tests pass, and we can
move on to the [server.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/8a5d958afb09522a911058e13d75ad4f494f43c7/server.py) level. We need to add assertions to our [_server_tests.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/8a5d958afb09522a911058e13d75ad4f494f43c7/_server_tests.py) file
that our user is logged in. Flask-Login uses flask's session object to
record logins by users. In order to test login status, I intend to test
the session for a ```user_id``` attribute that flask_login places there
for the logged in user.

Problem: I don't have access to the session in the response.

Flask provides a solution to test this using ```session_transaction```.
It took me a minute to figure this out, however. Here's [the docs](http://flask.pocoo.org/docs/0.10/testing/#accessing-and-modifying-sessions)
I used to find this, btw. So, after updating my tests, they should look
a little like this...


```python

def test_login(self):
        """Test User login through our POST route"""
        with test_database(self.TEST_DB, (User,)):
            self.app.post('/register', data=self.data)
            rv = self.app.post('/login', data=self.login)
            self.assertEqual(rv.status_code, 302)
             # new assertion here
            with self.app.session_transaction() as sess:
                assert 'user_id' in sess
            
```

We can use the same idea to test logout. 

Once the code has been written to satisfy these tests, congrats! We just
finished our small sprint! Everything in our beginning plan is complete. 
We can store, register, login, and logout users. I'm going to pretty this 
up a bit and make a new project to start the actual game, but we've come
a long ways.

 












