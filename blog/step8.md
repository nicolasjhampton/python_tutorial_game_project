## Step 8 - Cleaning up and putting it together

(1/21/16) From here, we've assembled all the parts that go into what 
the user can't see: The database, the server, and the form
validation. Before we break out and introduce ourselves to
the world wide bweb, however, I'd like to take a quick look
back and line a few things up to really make everything as
crystal clear as possible. Taking this little time for
detail work will, I think, bring us to a depth of understanding
that can easily translate to Django, Node, or any other
similar stack we run across. 

1. [models.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/a9e898265bf842cca5df7b75a3ba5e4756a582d4/models.py) and [_model_tests.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/4e601ceb45802f2f44a08ca44289c5dc6fe1bf2b/_model_tests.py)

In [Step 3, part 4, The UserMixin](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/master/blog/step3.md#4-the-usermixin), we made our User class inherit 
from the UserMixin class in order to gain login / logout 
functionality. As of now, we still haven't implemented logging
in and out, however. Removing the UserMixin class entirely 
results in only one test failing,  

```
(vpython)Nicolass-MacBook-Pro:GameProject nicolasjhampton$ python _model_tests.py
.......F.........
======================================================================
FAIL: test_get_id_result (__main__.UserTableTests)
Tests that a User entry's get_id method returns the user id for flask-login to use
----------------------------------------------------------------------
Traceback (most recent call last):
  File "_model_tests.py", line 90, in test_get_id_result
    assert str(self.user.id) == self.user.get_id()
AssertionError

----------------------------------------------------------------------
Ran 17 tests in 8.886s
```

...and the only reason this test fails without UserMixin is
the value get_id() returns is converted to a string in the
```get_id()``` method UserMixin uses to override the one we
already have. Changing our result to assert the equality between
```get_id()``` and just the plain non-string form of ```user.id```
returns a passing test result. Nothing else is affected

This is proof that UserMixin, at this current point, is completely
unneeded, so I'm taking it out for now. We'll put it back in
when it's more appropriate.

I also noticed that, although our form limits usernames to ascii
characters only using a regex expression, the error check in the
database makes no such check. I went back and made a test for this,
then added a truthy expression using ```re.match``` in our username
check method on the database.




2. [forms.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/a9e898265bf842cca5df7b75a3ba5e4756a582d4/forms.py) and [_form_tests.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/a9e898265bf842cca5df7b75a3ba5e4756a582d4/_form_tests.py)


I JUST FINISHED THIS FORM! So, if there's a lot of problems, I'm 
just too close to it right now to see them, because on the whole,
this looks really good to me. I added a lot of commenting, organized 
some labels and spacing, and moved on...


3. [server.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/a9e898265bf842cca5df7b75a3ba5e4756a582d4/server.py) and [_server_tests.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/a9e898265bf842cca5df7b75a3ba5e4756a582d4/_server_tests.py)

Same thing as forms, however I'm about to make major changes to these
files, so I just added some comments and docstrings here, deleted
a few there, and called it a day.

Our current [models.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/9ac83329a0976ae2b725f42dfc4259b7b1d1d267/models.py) and [_model_tests.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/9ac83329a0976ae2b725f42dfc4259b7b1d1d267/_model_tests.py) files. 

Our current [forms.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/9ac83329a0976ae2b725f42dfc4259b7b1d1d267/forms.py) and [_form_tests.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/9ac83329a0976ae2b725f42dfc4259b7b1d1d267/_form_tests.py) files. 

Our current [server.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/9e3dea80b2217c03dba362ca32cd0aea70a025cf/server.py) and [_server_tests.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/9e3dea80b2217c03dba362ca32cd0aea70a025cf/_server_tests.py) files.


4. PEP8

Going back to Kenneth's "Write Better Python" [PEP8 class](https://teamtreehouse.com/library/write-better-python/cleaner-code/pep-8), I 
decided to run ```flake8 models.py```, and see what happened...

```
(vpython)Nicolass-MacBook-Pro:GameProject nicolasjhampton$ flake8 models.py
models.py:4:1: F403 'from peewee import *' used; unable to detect undefined names
models.py:4:21: W291 trailing whitespace
models.py:6:1: W293 blank line contains whitespace
models.py:10:19: E261 at least two spaces before inline comment
models.py:11:80: E501 line too long (94 > 79 characters)
models.py:17:1: W293 blank line contains whitespace
models.py:20:1: W293 blank line contains whitespace
models.py:23:21: E711 comparison to None should be 'if cond is not None:'
models.py:24:19: E114 indentation is not a multiple of four (comment)
models.py:25:19: E114 indentation is not a multiple of four (comment)
models.py:27:1: W293 blank line contains whitespace
models.py:29:55: W291 trailing whitespace
models.py:31:1: W293 blank line contains whitespace
models.py:35:80: E501 line too long (80 > 79 characters)
models.py:40:1: W293 blank line contains whitespace
models.py:50:5: E303 too many blank lines (2)
models.py:54:51: W291 trailing whitespace
models.py:56:1: W293 blank line contains whitespace
models.py:58:1: W293 blank line contains whitespace
models.py:60:1: W293 blank line contains whitespace
models.py:65:26: E251 unexpected spaces around keyword / parameter equals
models.py:69:80: E501 line too long (86 > 79 characters)
models.py:71:1: W293 blank line contains whitespace
models.py:72:1: W293 blank line contains whitespace
models.py:77:21: W292 no newline at end of file
```

Ok, so at this point I ran flake8 against all 6 of my scripts
to really get this code clean before moving on. Some of the things
it catches, like the blanket peewee import, are things I'll 
keep in spite of PEP8, because it's common convention or just
works better the way it is. Ya know, don't go PEP8 crazy, but
try to keep things clean. After I cleaned up, this is what 
flake8 caught...

```
(vpython)Nicolass-MacBook-Pro:GameProject nicolasjhampton$ flake8 models.py
models.py:4:1: F403 'from peewee import *' used; unable to detect undefined names
models.py:36:80: E501 line too long (80 > 79 characters)
(vpython)Nicolass-MacBook-Pro:GameProject nicolasjhampton$ flake8 forms.py
(vpython)Nicolass-MacBook-Pro:GameProject nicolasjhampton$ flake8 server.py
(vpython)Nicolass-MacBook-Pro:GameProject nicolasjhampton$ flake8 _model_tests.py
(vpython)Nicolass-MacBook-Pro:GameProject nicolasjhampton$ flake8 _form_tests.py
_form_tests.py:2:1: F403 'from peewee import *' used; unable to detect undefined names
(vpython)Nicolass-MacBook-Pro:GameProject nicolasjhampton$ flake8 _server_tests.py
_server_tests.py:1:1: F403 'from peewee import *' used; unable to detect undefined names
```

P.S. - Once you're done using ```flake8```, make sure you do one 
more test run on everything, just to make sure you didn't break
something to make it look pretty...

```
(vpython)Nicolass-MacBook-Pro:GameProject nicolasjhampton$ coverage run _model_tests.py
..................
----------------------------------------------------------------------
Ran 18 tests in 10.129s

OK
(vpython)Nicolass-MacBook-Pro:GameProject nicolasjhampton$ coverage run _form_tests.py
..........
----------------------------------------------------------------------
Ran 10 tests in 4.111s

OK
(vpython)Nicolass-MacBook-Pro:GameProject nicolasjhampton$ coverage run _server_tests.py
..
----------------------------------------------------------------------
Ran 2 tests in 0.519s

OK
```

And after all that...

Our current [models.py]() and [_model_tests.py]() files. 

Our current [forms.py]() and [_form_tests.py]() files. 

Our current [server.py]() and [_server_tests.py]() files.

And with these files, moving forward, coverage reports...(These are 
composite results from three different reports) 

```

Name                                                       Stmts   Miss  Cover
------------------------------------------------------------------------------
models.py                                                     42      2    95%
server.py                                                     20      1    95%
forms.py                                                      15      0   100%
 
```


