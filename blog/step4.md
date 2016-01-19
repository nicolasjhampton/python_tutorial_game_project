<img alt="North Korea - Samjiyon waitress (5024319154) by Roman Harak - North Korea - Samjiyon waitress. Licensed under CC BY-SA 2.0 via Commons - https://commons.wikimedia.org/wiki/File:North_Korea_-_Samjiyon_waitress_(5024319154).jpg#/media/File:North_Korea_-_Samjiyon_waitress_(5024319154).jpg" src="server.jpg" width="30%">

## Step 4 - Servers, tips, and tests: Giving 120%

20 TOP DOWN! BEHIND YOU! I NEED A RUNNER! CORNER! TABLE 20 STILL NEEDS WATER!!!!

Oh s%#&, wrong server, had a flashback. Tip your waiter, people. Anyways...

(1/18/16) Let's quick take a glance at that roadmap in step 2...

- I'll design the database table that stores the user data (done)

    * Winged it mostly (done)

- Then I can add login,logout, and password hash information to that database (mostly done)

    1. Use B-crypt to hash the password stored in our User model (done)
        * I'll start this by writing 2 tests (done)
            - one to check the password is hashed (done)
            - another to check we can check a hashed password entry against it (done)
            
    2. Use flask-login User mixin to check login id and status (kinda done)
        *  I'll write a few tests (not sure how many, at least 2) (done)
            - one to check a user id is present after user creation (done)
            - another to check a login status (in or out) is present (haven't quite figured that out yet...)

- By then, I can build the flask server that will serve our first route... (Uh, yeah, sure, let's do this)

- The HTML register user screen that creates new users.


### 1. Sometimes you can't find it because it's not there...

...not where you're looking now, at least. You see, login status
isn't stored in the database. At least not the way I were taught
anyway. Does seem useful to store it there though, so I'm going 
make a note to my future self to take another look at this after
a good once through.

Anyways, login status is stored in cookies, and those cookies
are handled by the login manager in flask-login. And I don't
really work with login manager until I start the server instance
in app.py. I guess we're starting our app.py file now. According
to the plan, by now...

- ...I can build the flask server that will serve our first route...

Alright, time to fill out this pie in the sky goal. Since I'm
writing tests for everything first, I've decided to rename the 
tests.py file _model_tests.py, then start a new file called 
_server_tests.py for our, you guessed it, server tests. I also
made a blank file called app.py to hold this mythical server
we intend to test. Uh, test for what, exactly? Well, I've 
been making this User model so I can log in and out of this
game we're going to get around to making, so...

- ...I can build the flask server that will serve our first route...

    1. There will be a url to get to a register page
        * We can test for basic connectivity
            - We need a 200 response from our /register route
        * We need a register prompt
            - We can test for the presence of username, email, and password fields
        * We can test...
        
 ...woah, getting ahead of ourselves here, aren't we? I really 
 want to jump ahead and start building all sorts of things that 
I'm not ready for in my plan. The step after this one is...

- The HTML register user screen that creates new users.

...so that seems like the best place to test our fields. Really,
all we need from this run is a basic 200 http response and a
running database/ORM. So let's try this again...

- ...I can build the flask server that will serve our first route...

    1. There will be a url to get to a register page
        * We can test for basic connectivity
            - We need a 200 response from our /register route
        * The database is running in the background
            - We can connect to the database
            - We can close the database connection
            
There, done! Simple and sweet, no frills, just a few small, 
incremental steps. I'm stressing this because this planning 
not only decides what  do next, but also how many untested
holes I leave behind in what I've done. Slow and rocksteady, 
like first wave ska. So...

### 2. Does anyone know how to test a flask server???!!!

[The flask documentation](http://flask.pocoo.org/docs/0.10/testing/) does! This is a amazing
habit to get into. Just check the docs. Don't know where they
are? Type "(program) (Subject) docs" into google. Also, although
testing isn't really covered DURING the "Make A Social Network
With Flask" course, they do present us with a series of tests we 
have to pass at the end of the course. 

> Let me be clear about what I'm going to do, and thus demonstrate:
>
> I wasn't taught how to write tests for views. I'm going to read 
> someone's source, look at a couple docs, and wing it. Job skill
> number 1, right here...

Looking at Kenneth's initial setup for these tacocat tests (you
Treehouse students, see ["The Challenge"](https://teamtreehouse.com/library/build-a-social-network-with-flask/tacocat-challenge/the-challenge) video in "Build a Social
Network with Flask" course) we can problably improve our previous 
tests by doing some things differently too...

```python

"""Source from Kenneth Love's Treehouse Course"""

import unittest

from playhouse.test_utils import test_database
from peewee import *

import tacocat
from models import User, Taco

TEST_DB = SqliteDatabase(':memory:')
TEST_DB.connect()
TEST_DB.create_tables([User, Taco], safe=True)

USER_DATA = {
    'email': 'test_0@example.com',
    'password': 'password'
}

```

So, the first thing I notice is that a special module is
imported called ```test_database```. Bet you $10 that
makes testing the models easier. Well, lo and behold...

```python

    def test_create_user(self):
            #he's not actually using the development database to test!
            with test_database(TEST_DB, (User,)):
                self.create_users()
                self.assertEqual(User.select().count(), 2)
                self.assertNotEqual(
                    User.select().get().password,
                    'password'
                )
            
```

Aha! All this time I've been creating and deleting the 
development database every test! I'll have to go back and let
our fearless leader know later. Appearently, test_database()
allows us to use a database in memory (see the ```TEST_DB = SqliteDatabase(':memory:')```
line in the setup) so we don't even have to bother with a
file system store for testing. Moving on, because this isn't 
really what we were looking for, I see our first view test.

```python

class ViewTestCase(unittest.TestCase):
    def setUp(self):
        tacocat.app.config['TESTING'] = True
        tacocat.app.config['WTF_CSRF_ENABLED'] = False
        self.app = tacocat.app.test_client()
        
```

Wait, that's not a test, is it? All that's in this test class
is a setup method. Well, looking forward, two other test
classes inherit from this test class, which inherits from
our generic ```unittest.TestCase``` class, but adds some common
functionality that both descentant classes need. I'm paying
attention here: these are the design details that separate
the developers from the script-kiddies. This is object-oriented
design in its native habitat.

Looking at ```UserViewsTestCase```, the first test class to inherit 
from ```ViewTestCase```, I think I find something close to what I'm looking for.

```python

class UserViewsTestCase(ViewTestCase):
    def test_registration(self):
        data = {
            'email': 'test@example.com',
            'password': 'password',
            'password2': 'password'
        }
        with test_database(TEST_DB, (User,)):
            rv = self.app.post(
                '/register',
                data=data)
            self.assertEqual(rv.status_code, 302)
            self.assertEqual(rv.location, 'http://localhost/')
            
```

Alright, so it looking like once we've configured our app
to use the test client in ```ViewTestCase```, we can call the 
post method against the app, using ```test_database``` to direct
our request to the test database in memory, then store the post 
request in a variable. Once that variable gets its response from
the database, we can test the response attributes (like status 
code and location) for the results we're looking for.

This is probably the answer to our second test question,

    * The database is running in the background
            - We can connect to the database
            - We can close the database connection
            
but our first question,

    * We can test for basic connectivity
            - We need a 200 response from our /register route
            
might be in the ```TacoViewsTestCase```...

```python

class TacoViewsTestCase(ViewTestCase):
    def test_empty_db(self):
        with test_database(TEST_DB, (Taco,)):
            rv = self.app.get('/')
            self.assertIn("no tacos yet", rv.get_data(as_text=True).lower())
            
```

...basically the same idea as the "post" method, and I think
we can just replace the assertIn with a test for
a 200 status code, simply to check that the page is there.

> <img alt="http://s.quickmeme.com/img/de/de946157581984180c7402c7b4bf85b92589c505ee10270edf31c22af57a4a0f.jpg" src="but_why.jpg" width="30%">
> <br>
> *<b>So why didn't Kenneth write a test to simply check that the
'/register' page is there at all?</b>* 
> *<b>...and what the heck is all this doing anyway?</b>*

 I think he probably thought
it's overkill, and it most likely is. But I said I wasn't going to 
write a single piece of code without a test, so that's what I'm
going to do. With these field guides in mind, we can take a look
at [the official flask documentation on testing](http://flask.pocoo.org/docs/0.10/testing/),
and see that they have a couple other solutions for what Kenneth
has put together for tacocat...

```python

"""from the official docs for Flask"""

import os
import flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()

```

It looks like where Kenneth has opted for global variables 
in his tests, the official documentation is suggesting we 
keep most of those common setup procedures in our ```setUp```
method on the TestCase class, using (app name).app.config to
store the testing database in a tempfile, instead of the 
```TEST_DB = SqliteDatabase(':memory:')``` Kenneth has opted
for. Personally, I like what Kenneth did, putting an temporary 
database into temporary memory instead of on a random temp
file on the hard drive, so I'm going to use that. But,
looking at the differences helps to clear up what every moving
part is doing, and increases my understanding of what's going
on.


### 3. Less talk, more explosions Mr. Wizard!

Alright, let's frankenstein us a test in [_server_tests.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/4e601ceb45802f2f44a08ca44289c5dc6fe1bf2b/_server_tests.py)!

```python


import unittest

from playhouse.test_utils import test_database
from peewee import *

import app 
from models import User

```

I've deleted the imports for tempfile and os since they were 
for creating a tempfile for a database, and I'm going to make 
one in memory instead. I'm also pretty sure test_database is 
redirecting the database file from our model's database file 
declaration to a test location, so we're keeping that.

Instead of running models.initialize here, which would use the 
model's DATABASE variable directed at the 'models.db' file (like
we have before), we're going to direct everything to our TEST_DB 
in memory. I also decided to put all of this in the setUp method. 
I have no idea if it works there, but if it does, it will get 
these variables out of the global scope, which a principal of 
functional programming.

```python


class AppTestCase(unittest.TestCase):

    def setUp(self):
        TEST_DB = SqliteDatabase(':memory:')
        TEST_DB.connect()
        TEST_DB.create_tables([User], safe=True)
        tacocat.app.config['TESTING'] = True
        tacocat.app.config['WTF_CSRF_ENABLED'] = False
        self.app = tacocat.app.test_client()

```

The flask documentation lays out instructions for using 
app.config to redirect the tests to our test database. 
Kenneth uses test_database to do the same thing in memory,
but as a global variable I find a little ugly. I'm going to 
use test_database instead, move Kenneth's global variables 
into our setUp function, and cross my fingers. (also, 
Kenneth didn't tear anything down. Is this an advantage
to using memory? Meh, don't know yet...)

```python
    
    def test_register_url(self):
        with test_database(TEST_DB, (User,)):
            rv = self.app.get('/register')
            self.assertEqual(rv.status_code, 200)
            
if __name__ == '__main__':
    unittest.main()
            
```

All that to test a little 200 status code. It's a start...
I think. I also pulled a test for registration almost 
verbatim from Kenneth's tacocat tests, as it's pretty
clear that's one of the next test we'll need, and commented
it out.

Welp, derp, derp, let's run it!











 



