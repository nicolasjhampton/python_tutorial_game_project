<img src="http://www.azquotes.com/picture-quotes/quote-just-keep-on-using-me-until-you-use-me-up-bill-withers-138-73-52.jpg" width="75%">

## Step 3 - Using This User Up...

So I finished the password hashing in my last small sprint,
and I hope you figured that out too. I also did some small
refactoring on a method or two so each function wasn't
responisble for doing more than it should, a pattern I'm
going to try to keep, and I figured out how writing tests 
as I go can be a good guide to keeping our code inside
bite-size functions. Now, returning to the short roadmap
I have, in order to finish adding login, logout, and password 
hash information to that database, the next step is


### 2. Use flask-login User mixin to check login id and status

So I'll...

    *  ...write a few tests (not sure how many, at least 2).
    
We need...

        - ...one to check a user id is present after user creation...
        
and...

        - ...another to check a login status (in or out) is present.

I swear this gameplan almost writes itself! So, without 
knowing anything about what it takes to login and logout, I
can reasonably assume that something like "logged in" would
be a property of the ```User``` model that we create, most 
likely a boolean ```True``` for when our user is logged in 
and ```False``` for for when they're not. I think we can also 
safely assume that the user ID will be a similar property
on the user object. For the time being, I just need to check
that those two properties are present on the object.

Now, I know about the properties and methods on
every object by calling ```dir(object)```, or in this case,
```dir(models.User)``` in our test. When I open up a python
shell and try to use the ```in``` keyword for a value I know
is on the object and a value I know isn't, I get this...

```           
Python 3.5.0 (###################, Sep 12 2015, 11:00:19) 
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import models
>>> 'password' in dir(models.User)
True
>>> 'loggedin' in dir(models.User)
False
```

So it's completely possible to make the entire structure of
a test, even though I really don't know what I'm looking for
yet...

```python

    def test_login_property_exists(self):
        """Tests that a User entry is created with a login property"""
        user = models.User.get(email='testEmail@testEmail.com')
        assert 'loggedin' in dir(user)
        
```

Of course, there's a particular assertion for ```in``` truthy
values in the unittest library, but I actually see no actual
technical need to use it here, and for all intensive purposes,
I find it more valuable to narrow down the concept of what 
I'm testing so well that I, myself, can derive a true/false
result for it. 

If we know this mythical 'logged in' property exists, and we
know it's going to be either true or false, well, I can go
ahead and write another test then...

```python

    def test_login_property_truthy(self):
        """Tests that the login property is either True or False"""
        user = models.User.get(email='testEmail@testEmail.com')
        assert user.loggedin in [True, False]
        
```

Again, I'm sure I can test whether a value is truthy or not
with some special method (maybe even a 'magic method' built into
almost every value in python...), but hey, I'm not going to 
waste two hours looking on the internet for a one word method
that does the same thing as three words. At least not to start
with. We aren't born experts, exploit what you know, pick up 
the rest on the way.

I don't, however, have much of an idea what type of variable
to expect for the user ID. I do, however, know that once again,
it's likely to be a property on the ```User``` model. However,
looking at ```dir(models.User)```, I can see...

```
>>> dir(models.User)
['DoesNotExist', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_create_indexes', '_data', '_fields_to_index', '_get_pk_value', '_meta', '_pk_expr', '_populate_unsaved_relations', '_prepare_instance', '_prune_fields', '_set_pk_value', 'alias', 'as_entity', 'check_new_password_length', 'check_new_username_length', 'check_password', 'create', 'create_or_get', 'create_table', 'create_user', 'delete', 'delete_instance', 'dependencies', 'dirty_fields', 'drop_table', 'email', 'filter', 'get', 'get_id', 'get_or_create', 'hash_password', 'id', 'insert', 'insert_from', 'insert_many', 'invalidValueError', 'is_dirty', 'joined_at', 'password', 'prepared', 'raw', 'save', 'select', 'set_id', 'sqlall', 'table_exists', 'update', 'username']
```

...there's already an ```models.User.id``` property and a 
```models.User.get_id()``` method on the object, and they're
not what I'm looking for. This is the entry id automatically
assigned to every entry in the database table. So we'll fudge
a test...

```python

    def test_user_id_property_exists(self):
        """Tests that a User entry is created with a user_id property"""
        user = models.User.get(email='testEmail@testEmail.com')
        assert 'user_id' in dir(user)

```

Close enough, right? There, all tests written. Let's start 
coding...

### 3. May I remind you, we have no idea how login works...

But we wrote already wrote three tests for its expected
behavior, and put a lot of thought into how that behavior
will be represented. We also kept our expectations small
and well separated. That's why I'm writing the tests first.

So, all this login stuff is covered with a python module 
called Flask-Login, specifically the [UserMixin](http://flask-login.readthedocs.org/en/latest/#your-user-class) class. For
Treehouse students out there, Kenneth goes over all of this 
in [a video](https://teamtreehouse.com/library/build-a-social-network-with-flask/making-strong-users/the-usermixin-from-flasklogin) from the first section of "Build A Social Network
With Flask" class. Remember that most of the modules we're
using have to be installed with pip before we can import
them, I'm just not going over it. 