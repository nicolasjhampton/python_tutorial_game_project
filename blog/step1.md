## Step 1 - Making the User model   

### 1. ./tests.py, the first file 

Now that we have an area for our tests in [tests.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/766b977a2dfab5522dc5cae58d46f1c73a3849e4/tests.py), we need 
to figure out what these user objects are going to look 
like.

We'll want to write a test to show a user can be made.
I'm assuming we're going make a function called
```create_user``` to do that, and that it takes a 
username, email, and verified password to do so.
For the test, I think (incorrectly, but I'll find that
out later) that's all we need to know.
    
```python

    class UserTests(unittest.TestCase):
        def test_user_created(self):
            assert create_user(
                'testUsername',
                'testEmail@email.com',
                'passwordTest',
                'passwordTest') != IntegrityError
                
```
    
To be honest, I'm not sure that the nor condition against
the ```IntegrityError``` will work, but the general structure
of a test in python's unittest module is creating a class for
a series of tests, then writing a function for each unit test 
we want to run, each test coming to an assert statement that 
will somehow evaluate to "True" for passing or "False" for
not passing. Since I'm new to tests, I'm going to go with what I 
always do when I'm new to something, my best guess.

> Things our fearless leader doesn't know yet...
>
> - The class must inherit from the ```unittest.TestCase``` class
>
> - Each test has access to the class' ```self``` variable (useful later)
>
> - All unit tests must begin with "test" in the name for python's unittest module
            
Now that we have a test for the model creation, let's make 
the model in [models.py](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/766b977a2dfab5522dc5cae58d46f1c73a3849e4/models.py) ... 


### 2. ./models.py, our second file
    
 ```python
 
    class User(Model):
        username = CharField(unique=True)
        email = CharField(unique=True)
        password = CharField(max_length=100)
        joined_at = DateTimeField(default=datetime.datetime.now)
        # putting this here for future ref
        # IntegerField(default=0) 
        
        
        class Meta:
            database = DATABASE
            
```

To make this first model, I went to the "Build A Social
Network W/ Flask" course, ["The User Model"](https://teamtreehouse.com/library/build-a-social-network-with-flask/making-strong-users/the-user-model) video in the
first section. For more explination on each piece of 
the model, refer to section 1 of ["Using Databases In Python"](https://teamtreehouse.com/library/using-databases-in-python).

> Things our fearless leader doesn't know yet...
>
> For our ORM (PeeWee), each class attribute is a field in 
> our database, in this case our Sqlite3 database that the
> PeeWee ORM sits on top of. Which class we assign to the
> attribute defines what type of field is created in the 
> database, e.g. ```CharField``` in the ORM becomes
> ```VARCHAR``` in the SQL database, ```DateTimeField```
> becomes ```DATETIME``` in SQL, and so forth. Remember 
> that the ORM is A SEPERATE ABSTRACT LAYER we use to 
> safely access the database of our choice.

The ```datetime``` in the user model is of note, as we leave 
off the paranthesis. This way, the date is taken from 
the time the user is created, not the time the model
is defined.

This ```Meta``` class is required for each model, it defines 
certain sorting and location properties of the ORM model.
The database attribute here, for instance, defines the 
database this model is to be stored in by the ORM.

### 3. Correcting the test we didn't know how to make

By now, I can see that I actually didn't know enough
about creating the database to correctly write the 
test. That's ok, I still built the model around the
general test case, and can go back and correct the 
test to my new understanding. Can you look back and
see my mistake?
    
```python
    
    class UserTests(unittest.TestCase):
        def test_user_created(self):
            assert models.User.create_user(
                'testUsername',
                'testEmail@email.com',
                'passwordTest',
                'passwordTest') != IntegrityError
                
```

Again, I'm still not sure if all of this works (later, I'll
be sure that this still doesn't work). I haven't run anything yet. 
But from here I can already see the syntax for creating a User
was incorrect because the ```create_user``` method will be a property
of the User model.

Skipping hashed passwords and login properties for the
moment, as they add excess complexity before we've tested
what we have, we're going to define this create_user method.
This is referenced in the first section of the "Build A 
Social Network W/ Flask" class, in the ["Class Method"](https://teamtreehouse.com/library/build-a-social-network-with-flask/making-strong-users/class-method) video.
    
 ```python
 
    @classmethod    
    def create_user(cls, username, email, password):
        try:
            cls.create(
                username=username,
                email=email,
                password=password)
        except IntegrityError:
            raise ValueError("User already exists")
            
```

As explained in the aftformentioned lesson, we're going 
to create another method for creating a user besides the
generic ```User.create``` function, so that we can handle
and verify the data that is used to create a legitimate 
user.
    
```cls``` is the equivalent of ```self``` (this) here, and refers to
its own class. With the ```@classmethod``` decorator, this allows
this method to create its own instance of the class. Its a 
little recursive, I know. Yet another reason to return to 
all of this stuff after the [Functional Python](https://teamtreehouse.com/library/functional-python) class.

The ```IntegrityError``` is thrown if the username or email are not
unique. Note that I've defined this in the SQL field declarations
(ORM class attribute assignments).

So, from here, we know that the ```models.py``` file is imported
into the tests.py script. When we run the ```tests.py``` file,
```__name__ == '__main__'``` evaluates to true, and we run all 
our tests. I can sort of see a problem here, as we haven't
set our tests to connect to or create the database we're 
testing. We might want to write a test for that, so that
the database is connected to before we test if we can 
create a user, or we could add that to our test setup,
but then we'd miss testing the database connection.

After some digging through assertions (section 2 of the
["Python Testing"](https://teamtreehouse.com/library/python-testing) course) and continuing the database setup
(section 2 of "Build A Social...", the ["Before And After Requests"](https://teamtreehouse.com/library/build-a-social-network-with-flask/takin-names/before-and-after-requests) 
video) I think I finally have figured out how to test our 
database creation. 

In practice, every flask request will open and close the 
database connection. So from here, we want to be able to
open the database connection, create a user, recall 
that user, delete that user, and then close the database.
    
```python

    def initialize():
        """Called when the program starts if not called as an imported module."""
        DATABASE.connect()
        DATABASE.create_tables([User], safe=True)
        DATABASE.close()
        
```

    - Of note: looking back at this from later in the project, I didn't quite understand 
      connecting and closing the connection yet. Derp, derp, whatev's, let's wire it up...
    
I also discovered the initialize function for the 
database, and used it to replace the ```'__name__'``` setup
in ```models.py```. This exposes a method we can run a test 
on for initialization of the database. 

### 4. One or two frustrating days later...

In learning, this will always happen. I've come to expect
that when doing something in programming I'm unfamiliar 
with, I'll hit something that I can't solve/infuriates
me for at least a few days, if not a week. Don't be afraid
of this time. Almost everything I'm strong in is because
I learned it while I broke something that took me a week
to fix while not knowing what I'm doing. 

In this case, we had a lot of pieces that we we're 90%
sure worked alone, but when we combined them, didn't work
anymore. Here's what I learned:

The PeeWee ORM is placed on top of the database, in this
case SQLite3, as indicated by the line of code in our 
models.py file ```DATABASE = SqliteDatabase('users.db')```.

SQLite3, therefore, is what is throwing errors for our
field retrictions, such as max_lengths for field entries
and unique field requirements.

SQLite3 DOESN'T THROW ERRORS FOR VARCHAR max_lengths!
Thanks goes to Chris Freeman for pointing this [doc](https://www.sqlite.org/faq.html#q9) out to me 
in [the treehouse forums](https://teamtreehouse.com/community/writing-tests-for-the-orm).

So, in order for our tests to work, we have to enforce 
those length limits ourselves. We'll use the ```create_user```
method on the ```User``` model to do just that, and the
```@classmethod``` declaration on the method will allow
it to create its own instance, bypassing the built-in
create method for this new one with our safety-checks
built in:
    
```python
    
    @classmethod
    def create_user(cls, username, email, password):
        
        # Username length check
        if(len(username) > 3 and len(username) < 51):
            usernameChecked = username
        else:
            error = "username"
         
        # Password length check    
        if(len(password) > 6 and len(password) < 20):
            passwordChecked = password
        else:
            error = "password"
            
        try:
            cls.create(
                username=usernameChecked,
                email=email,
                password=passwordChecked)
        except IntegrityError:
            raise ValueError("User already exists")
        except UnboundLocalError:
            # UnboundLocalError is thrown if any args are missing
            # from the create method. By forcing invalid Username/
            # Password values to be missing, we'll control this throw
            raise ValueError("Invalid {}".format(error))
            
```

So, with a total of twelve tests, all now passing, I run
```coverage run tests.py``` and then ```coverage report``` 
and get 100% test coverage on my models.py file. Not bad.
I think we can move on to the next step from here...

### 5. One last short note

For anyone wondering "why not doctests?", as though doctests
were even going to come close to 100% test coverage on this,
I asked the same question myself. However, I couldn't ever 
get the doctests to work with PeeWee, and couldn't find anyone
online who had anything to say about it, so if you know something
let me know. I like those little inline tests that could! 

[On to step 2...](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/master/blog/step2.md)
    
    
    
    
    
    
    
    
    
    