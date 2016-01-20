## Step 5 - Writing Simple Boilerplate For Simple Tests

So, if you're a treehouse student who finished the "Build
A Social Network With Flask" course, like I am, you most
likely forgot the "Flask Basics" course altogether, and
are ready to make this project really freaking complex. I
felt the same way, and was importing all kinds of 
LoginManagers, making before and after request methods,
and generally ignoring the test I spent all that time writing.

So...what am I testing for?

### 1. Getting a 200 status code from a server

Oh, that's right. Well, how do you do that? Basically
you receive a request at a url, and then send anything at 
all back. This ain't rocket science. This is about as 
simple as it gets. I'm going to 

- Import the Flask class from the flask module, 

- store our server settings in global variables for convenence,

- and create a flask object named app from the flask class.

- I use that object to attach a route for our register page

- that returns some kind of text, any kind of text

- then run the flask instance.

This is about as simple as a server gets, and I want
to bring it down to this level before we build it up, 
so I understand EVERYTHING, and test EVERYTHING. So
all this looks like...

```python

"""Flask server boilerplate code"""

from flask import Flask

# server settings
DEBUG = True
PORT = 8000
HOST = '127.0.0.1'

app = Flask(__name__)
    
@app.route('/register')
def register():
    return "Registration Page"
    
if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
    
```

...and I actually managed to avoid giving away any
direct code challenge answers, though if you haven't finished
the code challenges that go with this, but you followed 
me all the way here, you're doing something wrong, go back and
take ["Flask Basics"](https://teamtreehouse.com/library/flask-basics/welcome-to-flask/first-steps). Most of what I'm doing here
I learned from there.

And that is all it takes to get a 200 status code. We're
not connected to a database or making posts or checking for
template phrasing or any of that. We wrote a status test, so
we made a server that could return a couple words and a 200
status code. Let's take a look at our test coverage using
```coverage run _server_tests.py``` and ```coverage report```

```

(vpython)Nicolass-MacBook-Pro:GameProject nicolasjhampton$ coverage run _server_tests.py
.
----------------------------------------------------------------------
Ran 1 test in 0.094s

OK
(vpython)Nicolass-MacBook-Pro:GameProject nicolasjhampton$ coverage report
Name                                                                                           Stmts   Miss  Cover
------------------------------------------------------------------------------------------------------------------
_server_tests.py                                                                                  19      0   100%
models.py                                                                                         41     22    46%
server.py                                                                                          9      1    89%
(... packages omitted for clarity ...)
------------------------------------------------------------------------------------------------------------------
TOTAL                                                                                          16938  10881    36%

```

See that server.py value of 89%? That's the only one I care
about. I'm not testing the tests, and I'm not running tests
for the models here, so of course coverage on models.py is 
going to be low. There's like 50 packages listed after server
that I omitted that are things we imported that are already
tested by other people, and those packages we don't have to 
test are throwing off our total at the bottom. Still, we
only reached 89%. Somehow we missed 1 line out of ten. If
we run ```coverage html```, we'll get an entire website report
created, and we can see exactly which line I missed...

<img src="coverage_step_5.png">