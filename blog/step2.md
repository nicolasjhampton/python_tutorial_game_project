<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Arch_voussoirs.svg/2000px-Arch_voussoirs.svg.png" width="50%">

## Step 2 - From the springers to the keystone

### 1. Dude, that was a headache...where are we?

So, (1/15/16) we have the beginning of the User model. It 
seems we as beginners went so far out of our way that we 
forgot where it is we are going. Part of that isn't all bad.
Now we have an idea of the size of our first piece, the 
generic user. From here, we can build up to a user login/
sign out screen without really introducing too much more 
complexity at the bottom level of operation, our database. 

Sometimes you kind of have to start blindly coding for a 
minute, expecially if you're generally unfamiliar with the
capabilities of the tools you're working with. Just jump
in and break something is usually the best foundation for
a project you're afraid to start, but very quickly you're 
to want a plan, even if that plan isn't complete. In fact,
I'm not even going to try to complete this plan. Instead,
I'm going to focus on building up to the horizon of things
I know, and shoot for completing that. From there, we'll
lookout and make a new plan, until we meet our imaginary
user at the keystone of what we're building.

So, I'm thinking...

- I'll design the database table that stores the user data (done)

- Then I can add login,logout, and password hash information to that database (where we are now)

- By then, I can build the flask server that will serve our first route...

- The HTML register user screen that creates new users.


That seems like a reasonable plan to start out with. Leaves
plenty of space inbetween to figure out the details. If it
seems like we're a good ways away from any actual coding of 
the 'game', I'd say you're half right. Some of my biggest 
unknowns were in working with the ORM and testing, AKA 
things I haven't tried on my own before. Some parts, like 
routing and server setup, will go by really fast. I just
try not to be in a rush. A lot of this is teaching me things
I started this project to learn in the first place. Try to 
be kind to yourself.

### 2. Mapping my next step

Now that we know the first step is done and the basic 
skeleton of the User model is complete, let's try and fill
in some of the details in our second step:

- Then I can add login,logout, and password hash information to that database (where we are now)

    1. Use B-crypt to hash the password stored in our User model
        * I'll start this by writing 2 tests
            - one to check the password is hashed
            - another to check we can check a hashed password entry against it
            
    2. Use flask-login User mixin to check login id and status
        *  I'll write a few tests (not sure how many, at least 2)
            - one to check a user id is present after user creation
            - another to check a login status (in or out) is present 
            
> "So Nic" you say. 
> "Yes, gentle reader?" I respond.
> "Why are you doing these steps in the exact opposite order as the ["Build A Social Network"](https://teamtreehouse.com/library/build-a-social-network-with-flask) course?"
> "Good question, you studious frog you!", I say.

Well, it seems, having started this project with learning 
test-driven development in mind, that I may have learned 
something already. The simplest start to this is the User.
Once I've written a test for the most basic kind of user,
then I can add a test for a simple improvement. The simplest
improvement I see is a simple change of password format,
so I'll write the test to pass that first, then code a 
passing solution. Once that's all written and tested, I'll
make sure I didn't miss any obvious outlier cases, then
add the next most complicated piece, user login/logout id,
since it adds three or four different levels of functionality.

By going in this order, I can be fairly sure that most of 
the things I'll break when I add something will have to 
do with the particular piece I'm adding, whether that be
compatablity issues with something I already built or
me not understanding the new addition, or just that what
I'm adding won't ever work in this implemetation. Lot 
less potential for problems in TDD, huh? 

### 3. Testing the password...

So, starting with an understanding of what a hashed 
password is and how we access it after it is hashed (which
can be found in [this video](https://teamtreehouse.com/library/build-a-social-network-with-flask/making-strong-users/cryptographic-hashing-with-flaskbcrypt) for you treehouse students)
we'll take a shot at writing our first test. I actually
started to write a password check and commented it out
in my last few commits:

```python

    # def test_password(self):
    #     """Tests that a User entry can be recalled by password"""
    #     user = models.User.get(username="testUsername")
    #     self.assertEqual(user.password, 'testPassword')
    
```

Originally, I was being an idiot. Of course we don't 
want to be able to search for our use by their password
(unless we were doing research on password usage and security).
So, we're going to completely rewrite this test to make
sure that the password passed into our ```create_user```
method is NOT equal to the password that ends up in the
database. Well heck, we might be able to write a test 
for that without understanding anything about how to make it
pass (unbelievably for the novice, that's the point).

```python

    def test_password_hashed(self):
        """Tests that any recalled password is not equal to the original password text (assumed hashed)"""
        user = models.User.get(username="testUsername")
        self.assertNotEqual(user.password, 'testPassword')
        
```

Super simple! Later, after understanding hashing a bit
more, if we want to add checks to make sure that the 
password entry is for sure a hashed password, not just
something not equal to the original text, we can, but 
that's a level of detail we don't have to start with.

Once we have a test making sure the password is hashed,
we want a test checking that we can compare a hashed
password with a hashed entry and get a "password equal
to hash" result. That takes some understanding worth going
back to ...

WAIT, STOP!

### 4. WAIT, STOP, DON'T TELL ME... Your card is the second test?

See how we assumed that we had to know something about
HOW to do something before we write a test to see if it
has been done. That's a lie. We ain't gotta know crap.
We're just going to name a function we haven't created
yet as the action that we are testing. It's going to take
the password and a user, then return a truthy statement
as to whether they match. If they do, we passed. If not,
not:

```python

    def test_password_equality(self):
        """Tests that any recalled password is not equal to the original password text (assumed hashed)"""
        user = models.User.get(username="testUsername")
        assert check_password(user.password, 'testPassword')
        
```

So, we're going to make a function called ```check_password```
to do this. If you know anything about how bcrypt works,
this might seem redundant. However, creating another function
for this insures each unit test is only testing one function, 
and that function is only doing one unit of work, a big 
requirement of functional programming!

Now, go ahead and design the full-sized function to pass 
these 2 tests. Instructions can be found in the 
["Cryptographic Hashing with Flask-Bcrypt"](https://teamtreehouse.com/library/build-a-social-network-with-flask/making-strong-users/cryptographic-hashing-with-flaskbcrypt)lesson.
That's not my problem guys, I'm here for the tests
and the functions. Good luck with that...

### 5. Breaking down into units of code and tests


That said, I can show you an example
of what I mean with something we previously coded in
a less-than-functional fashion. Let's have a quick look 
at the password and username length checks in our
```create_user``` function:

```python 

@classmethod
    def create_user(cls, username, email, password):
        """Method to safely create a new User entry.
           Sqlite3 does not enforce character length
           limits on VARCHAR fields, so we have to 
           manually block and throw errors."""
           
        error = "email"
        
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
            raise ValueError("Invalid {}".format(error))
            
            
```

Doesn't it seem like this function is responsible for too
much? It checks the username length, the password length,
and creates the database entry, as well as storing the 
base error variable. TOO MUCH. If I can say multiple things
it's doing, it's doing to much. Let's make the username
and password checks their own functions...


```python
     """Inside our User class..."""

    invalidValueError = "email"

    def check_new_username_length(cls, username):
        """Username length check"""
        if len(username) > 3 and len(username) < 51:
            return username
        else:
            cls.invalidValueError = "username"
            return None
            
    def check_new_password_length(cls, password):
        """Password length check"""
        if len(password) > 6 and len(password) < 20:
            return password
        else:
            cls.invalidValueError = "password"
            return None


    @classmethod
    def create_user(cls, username, email, password):
        """Method to safely create a new User entry.
           Sqlite3 does not enforce character length
           limits on VARCHAR fields, so we have to 
           manually block and throw errors."""
        
        usernameChecked = cls.check_new_username_length(cls, username)
         
        passwordChecked = cls.check_new_password_length(cls, password)
        
        try:
            cls.create(
                username=usernameChecked,
                email=email,
                password= cls.hash_password(passwordChecked))
        except IntegrityError:
            raise ValueError("User already exists")
        except UnboundLocalError:
            raise ValueError("Invalid {}".format(cls.invalidValueError))

```

Ha, now we've split up our units into small, testable 
chunks. Notice how we attached the methods to the cls object,
then passed the cls object when we needed to access variables
or methods that belong to that object (cls is a reference to 
the class of itself, very much like ```self``` and ```this```, 
although I'm only using instinct to engineer this solution, 
I don't know if it's convention. But I like it.) 

What's more, now that we've completely changed the 
implementation of the ```create_user``` method, I can run my
tests and know that everything still works! As long as I 
keep every level of complexity seperate, one level shouldn't
be changed by how the lower level changes, as long as we
take the same arguments and return the same variables. 

The invalidValueError variable is quite questionable from
a functional programming standpoint, as we shouldn't
have side affects from functions affecting variables
outside of the function's scope. But, the variable is 
contained inside of the object, it's only used for one
purpose, and in general, I'm ok with it. Functional
programming isn't the end all be all, just a guideline.
In this case, I like the solution for the moment being.

Now I can move on to [finishing this User class...](https://github.com/nicolasjhampton/python_tutorial_game_project/blob/master/blog/step3.md)
