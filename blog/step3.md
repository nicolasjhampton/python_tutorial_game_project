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

I swear this gameplan almost writes itself! Wait, something's
wrong. Let me just back up and correct something really quick...


### 2. Writing tests for code you know nothing about

So, without 
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

> <img alt="By New York : Underwood & Underwood, publishers (US-LOC) [Public domain], via Wikimedia Commons, https://commons.wikimedia.org/wiki/File%3ADunce_cap_from_LOC_3c04163u.png" src="our_fearless_leader.png" width="10%">
> *<b>Things our fearless leader doesn't know yet...</b>*
>
> HA-HA-HA-HA-HA! I know d%$# well there's no such property!
> But will wear this hat proudly, cadet, for tommorow,
> we will be all the wiser for the code we'll screw up today!

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

> <img width="20%" alt="Licensed under Public Domain via Wikimedia Commons - https://commons.wikimedia.org/wiki/File:Brown,r_time_macine60.jpg#/media/File:Brown,r_time_macine60.jpg" src="the_time_machine.jpg"/>
> *<b>But in the future...</b>*
>
> I'm not going to say I could have saved myself hours by just
> reading the docs and blindly following the instructions. Mostly
> because, as you're about to see, I followed this rabbit hole into 
> learning a ton of stuff I didn't know before. I've learned more 
> wearing this hat than most others have trying to avoid it.

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
not what I'm looking for.

> <img alt="By New York : Underwood & Underwood, publishers (US-LOC) [Public domain], via Wikimedia Commons, https://commons.wikimedia.org/wiki/File%3ADunce_cap_from_LOC_3c04163u.png" src="our_fearless_leader.png" width="10%">
> *<b>Things our fearless leader doesn't know yet...</b>*
>
> ...these actually ARE those droids we are looking for.
> UserMixin is making the reasonable guess that we're 
> using a database to store our users, and that 'id' will
> be the unique identifier. More often than not, that guess
> would be correct, and the stock code takes that into
> account.

This is the entry id automatically assigned to every entry in the 
database table. So we'll fudge a test...

```python

    def test_user_id_property_exists(self):
        """Tests that a User entry is created with a user_id property"""
        user = models.User.get(email='testEmail@testEmail.com')
        assert 'user_id' in dir(user)

```

Close enough, right? There, all tests written. Let's start 
coding...

### 3. May I remind you, we have no idea how login works...

...but we wrote already wrote three tests for its expected
behavior, and put a lot of thought into how that behavior
will be represented. We also kept our expectations small
and well separated. That's why I'm writing the tests first.

So, all this login stuff is covered with a python module 
called Flask-Login, and that module requires all users 
implement certain methods that come pre-packaged in the [UserMixin](http://flask-login.readthedocs.org/en/latest/#your-user-class) class. For
Treehouse students out there, Kenneth goes over all of this 
in [a video](https://teamtreehouse.com/library/build-a-social-network-with-flask/making-strong-users/the-usermixin-from-flasklogin) from the first section of "Build A Social Network
With Flask" class. Remember that most of the modules we're
using have to be installed with pip before we can import
them, I'm just not going over it. 

So, let's just take a snapshot of the top of the [models.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/21c137f30e863010ce082d6be1b4463ea992f42b/models.py)
file as it should be before we do anything fancy...you know, for posterity...

```python

import datetime

from flask.ext.bcrypt import check_password_hash, generate_password_hash
from peewee import * # Peewee convention is to make this very broad import

# This will define the database to be connected to / created 
DATABASE = SqliteDatabase('users.db')

# User is based on the 'Model' class, as all our database 
# objects will be.
class User(Model):
    """Database schema for the User table. All database objects descend from 'Model' class."""
    username = CharField(max_length=50, unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=20)
    joined_at = DateTimeField(default=datetime.datetime.now)
    invalidValueError = "email"
    
    class Meta:
        database = DATABASE
        
```
The first thing I'm going to do is import the ```UserMixin```
from the flask-login module, then add the ```UserMixin``` 
class as the first class of our User model.

### 4. The UserMixin

Kenneth goes over the UserMixin documentation in the video and 
explains that what it's doing is pretty simple, but there's a 
link to the [source code](http://flask-login.readthedocs.org/en/latest/_modules/flask_login.html#UserMixin), so we might as well 
take a look at HOW simple...

```python

    class UserMixin(object):
            '''
            This provides default implementations for the methods that Flask-Login
            expects user objects to have.
            '''
            @property
            def is_active(self):
                return True

            @property
            def is_authenticated(self):
                return True

            @property
            def is_anonymous(self):
                return False

            def get_id(self):
                try:
                    return unicode(self.id)
                except AttributeError:
                    raise NotImplementedError('No `id` attribute - override `get_id`')

            def __eq__(self, other):
                '''
                Checks the equality of two `UserMixin` objects using `get_id`.
                '''
                if isinstance(other, UserMixin):
                    return self.get_id() == other.get_id()
                return NotImplemented

            def __ne__(self, other):
                '''
                Checks the inequality of two `UserMixin` objects using `get_id`.
                '''
                equal = self.__eq__(other)
                if equal is NotImplemented:
                    return NotImplemented
                return not equal

            if sys.version_info[0] != 2:  # pragma: no cover
                # Python 3 implicitly set __hash__ to None if we override __eq__
                # We set it back to its default implementation
                __hash__ = object.__hash__

```

So, on the surface, pretty simple. We know a class can inherit
more than one class, so all we're doing when we add this one 
is adding the methods and properties that belong to the UserMixin 
class to our model class. They're all pretty simple, once you 
take a closer look at them. Let's go backwards:

```python

        if sys.version_info[0] != 2:  # pragma: no cover
            # Python 3 implicitly set __hash__ to None if we override __eq__
            # We set it back to its default implementation
            __hash__ = object.__hash__

```

python 2 and python 3 handle equality between objects differently,
thus this test. Nothing important really...

```python

        def __eq__(self, other):
            '''
            Checks the equality of two `UserMixin` objects using `get_id`.
            '''
            if isinstance(other, UserMixin):
                return self.get_id() == other.get_id()
            return NotImplemented

        def __ne__(self, other):
            '''
            Checks the inequality of two `UserMixin` objects using `get_id`.
            '''
            equal = self.__eq__(other)
            if equal is NotImplemented:
                return NotImplemented
            return not equal

```

These two definitions override the magic methods for equality and
non-equality on the object. For more info, check out this tutorial 
on [magic methods](http://www.rafekettler.com/magicmethods.html), pretty useful information. Basically, 
we're just making sure that when we compare ```User``` objects, 
we compare them by the ```user_id```. What ```user_id```, you might 
ask...

```python

        def get_id(self):
            try:
                return unicode(self.id)
            except AttributeError:
                raise NotImplementedError('No `id` attribute - override `get_id`')

```
So, from what I can tell, this id, in our case, is actually 
present before any of this ```UserMixin``` implementation. 
It's the automatically added id field of the database entry, 
which at this level the class can be fairly certain will be 
present. If the ```user_id``` is not present, we'll get an error 
asking us to modify the method to retrieve whatever we are 
using to uniquely identify the User objects. Again, nothing 
special, just a dependable way for the flask-login  module 
to access each unique ```User``` object.

```python

        @property
        def is_active(self):
            return True

        @property
        def is_authenticated(self):
            return True

        @property
        def is_anonymous(self):
            return False

```

> <img alt="http://s.quickmeme.com/img/de/de946157581984180c7402c7b4bf85b92589c505ee10270edf31c22af57a4a0f.jpg" src="but_why.jpg" width="10%">

Do you ever get that urge to make something very simple
exceedingly complex? Let's feed that urge now. Each one of these 
"properties" (more in a second) are referring to special
states we actually aren't going to use in this class. That's
what Kenneth really goes over in this video. We wont be making
anonymous users, but we could override this method to create 
them if we wanted, and flask-login would know where to look 
for info needed to implement them. All are users will be 
authenticated (meaning we aren't going to send a text to 
someone's phone for registration verification or anything 
like that), and all users will be active at all times (meaning
we wont be suspending accounts or requiring additional hoops 
besides registration to get an account started). These could be 
useful in other situations in which we cared, but we really 
don't. Not today, at least.

What's more fascinating to me here are the ```@property``` 
decorators wrapping each of these functions. Check out the 
[decorators workshop](https://teamtreehouse.com/library/python-decorators) for more information on these, 
but the ```@property``` decorator is a builtin python 
decorator. Really, it's just a function that takes a function 
as an argument. Lots of languages can take functions as 
arguments and return functions as computed values, but
python has a special built-in syntax (or syntaxical sugar, 
get used to that needless nickname) for decorators, as
they can be pretty useful.

In this case, the ```@property``` decorator (or function, 
just think of it as a function) takes these functions as 
arguments and turns them into namespaced properties on the 
User object. We could write this a couple different ways 
to show just how simple this really is...

```python

         #e.g. 1 - python decorator special syntax

         @property
         def is_anonymous(self):
             return False

         #############################################################

         #e.g. 2 - the actual simple concept of a decorator function
         #         is just a function that wraps another function
         #         to add functionality

         def is_anonymous(self): #we're going to wrap this function in the decorator
            return False

         is_anonymous = property(is_anonymous) # the decorator is just another function
                                               # which takes a function and returns 
                                               # a function that does more
         
         is_anonymous(self) #then we can run the enhanced function

```

See, nothing special really. Now, what does the ```@property```
do, in particular? Well, from what I can tell, it defines 
getters, setters, and deleters for the value of the original 
function, and attaches it as a property of the object. 
Basically, it makes a property. If you want more of a look, 
[check it out](https://docs.python.org/2/howto/descriptor.html#properties). It looks like a lot of 
recursive-curried-magic-knot-tying, but it's actually pretty 
straight forward if you take the time to read the simple yet 
confusing low level code.  

### 4. Testing things we know, and refactoring a bit

So, do we need to understand all that to use UserMixin? No,
not at all. In fact, except as a learning tool, all that info
overload was pretty useless, really. Basically, UserMixin is
just a quick way to make sure our users have properties and
methods flask-login needs to use. BUT, now we do know what 
properties and methods the tests have to look for. And we 
missed most of them! So let's quick write those tests...

```python
    
     def test_user_id_exists(self):
        """Tests that a User entry is created with a login property"""
        user = models.User.get(email='testEmail@testEmail.com')
        assert 'id' in dir(user)
        
     def test_get_id_exists(self):
        """Tests that a User entry is created with a login property"""
        user = models.User.get(email='testEmail@testEmail.com')
        assert 'get_id' in dir(user)
        
     def test_get_id_result(self):
        """Tests that a User entry is created with a login property"""
        user = models.User.get(email='testEmail@testEmail.com')
        assert str(user.id) == user.get_id()
        
 ```
 
> <img width="20%" alt="Licensed under Public Domain via Wikimedia Commons - https://commons.wikimedia.org/wiki/File:Brown,r_time_macine60.jpg#/media/File:Brown,r_time_macine60.jpg" src="the_time_machine.jpg"/>
> *<b>But in the future...</b>*
>
> ...Professor Jones has been shot repeatedly by a strange 
> unicode function Python doesn't seem to recognize, so
> Indy has to retrieve the holy grail of version inconsistances... 
> 
> Spoiler alert:
> In Python 2, unicode and strings are handled differently
> In Python 3, they aren't, thus the unicode function is depreceated
> In Hebrew, Jehovah is spelled with an 'I'
 
 So, we keep seeing this line in a lot of our newer tests...
 
 ```python
 
    user = models.User.get(email='testEmail@testEmail.com')
    
```

So I've decided to factor this out into our setUp method, 
so we don't have to write it into every test. Keep in mind
that in order for all the tests to have access to this 
variable, you have to attach it to the self reference of the
class, like...

```python

    self.user = models.User.get(email='testEmail@testEmail.com')
    
```
and then refer to it the same way, such as...

```python

    def test_get_id_result(self):
        """Tests that a User entry's get_id method returns the user id for flask-login to use"""
        assert str(self.user.id) == self.user.get_id()
        
```

After a couple of test runs, I was able to modify all
the tests and check for any possible false positives from
the change. All good.

We know, now that everything has a test (mostly, I'm at 93% coverage)
that we have a secure User model that can be handled by 
flask-login.
 
At this point, I think our last goal here...

    - ...[writing] another [test] to check a login status (in or out) is present.
    
deserves to be pushed [into the next step...](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/master/step4.md)

(I mean, this was getting crowded, wasn't it?)




