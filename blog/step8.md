## Step 8 - Cleaning up and putting it together

From here, we've assembled all the parts that go into what 
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