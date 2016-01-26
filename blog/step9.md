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


[layout.html]()
[login.html]()
[register.html]()
[macros.html]()
[application.css]()


files. I also made some new tests in 


[_server_tests.py]()
[_form_tests.py]()


With that out of the way, lets take a look at this new ```login```
route in [server.py]()









