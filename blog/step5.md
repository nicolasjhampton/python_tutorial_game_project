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

<div id="source">
    <table>
        <tr>
            <td class="linenos">
<p id="n1" class="pln"><a href="#n1">1</a></p>
<p id="n2" class="pln"><a href="#n2">2</a></p>
<p id="n3" class="stm run hide_run"><a href="#n3">3</a></p>
<p id="n4" class="pln"><a href="#n4">4</a></p>
<p id="n5" class="pln"><a href="#n5">5</a></p>
<p id="n6" class="stm run hide_run"><a href="#n6">6</a></p>
<p id="n7" class="stm run hide_run"><a href="#n7">7</a></p>
<p id="n8" class="stm run hide_run"><a href="#n8">8</a></p>
<p id="n9" class="pln"><a href="#n9">9</a></p>
<p id="n10" class="stm run hide_run"><a href="#n10">10</a></p>
<p id="n11" class="pln"><a href="#n11">11</a></p>
<p id="n12" class="stm run hide_run"><a href="#n12">12</a></p>
<p id="n13" class="pln"><a href="#n13">13</a></p>
<p id="n14" class="stm run hide_run"><a href="#n14">14</a></p>
<p id="n15" class="pln"><a href="#n15">15</a></p>
<p id="n16" class="stm run hide_run"><a href="#n16">16</a></p>
<p id="n17" class="stm mis"><a href="#n17">17</a></p>
                
            </td>
            <td class="text">
<p id="t1" class="pln"><span class="str">&quot;&quot;&quot;Flask server boilerplate code&quot;&quot;&quot;</span><span class="strut">&nbsp;</span></p>
<p id="t2" class="pln"><span class="strut">&nbsp;</span></p>
<p id="t3" class="stm run hide_run"><span class="key">from</span> <span class="nam">flask</span> <span class="key">import</span> <span class="nam">Flask</span><span class="strut">&nbsp;</span></p>
<p id="t4" class="pln"><span class="strut">&nbsp;</span></p>
<p id="t5" class="pln"><span class="com"># server settings</span><span class="strut">&nbsp;</span></p>
<p id="t6" class="stm run hide_run"><span class="nam">DEBUG</span> <span class="op">=</span> <span class="key">True</span><span class="strut">&nbsp;</span></p>
<p id="t7" class="stm run hide_run"><span class="nam">PORT</span> <span class="op">=</span> <span class="num">8000</span><span class="strut">&nbsp;</span></p>
<p id="t8" class="stm run hide_run"><span class="nam">HOST</span> <span class="op">=</span> <span class="str">&#39;127.0.0.1&#39;</span><span class="strut">&nbsp;</span></p>
<p id="t9" class="pln"><span class="strut">&nbsp;</span></p>
<p id="t10" class="stm run hide_run"><span class="nam">app</span> <span class="op">=</span> <span class="nam">Flask</span><span class="op">(</span><span class="nam">__name__</span><span class="op">)</span><span class="strut">&nbsp;</span></p>
<p id="t11" class="pln"><span class="strut">&nbsp;</span></p>
<p id="t12" class="stm run hide_run"><span class="op">@</span><span class="nam">app</span><span class="op">.</span><span class="nam">route</span><span class="op">(</span><span class="str">&#39;/register&#39;</span><span class="op">)</span><span class="strut">&nbsp;</span></p>
<p id="t13" class="pln"><span class="key">def</span> <span class="nam">register</span><span class="op">(</span><span class="op">)</span><span class="op">:</span><span class="strut">&nbsp;</span></p>
<p id="t14" class="stm run hide_run">&nbsp; &nbsp; <span class="key">return</span> <span class="str">&quot;Registration Page&quot;</span><span class="strut">&nbsp;</span></p>
<p id="t15" class="pln"><span class="strut">&nbsp;</span></p>
<p id="t16" class="stm run hide_run"><span class="key">if</span> <span class="nam">__name__</span> <span class="op">==</span> <span class="str">&#39;__main__&#39;</span><span class="op">:</span><span class="strut">&nbsp;</span></p>
<p id="t17" class="stm mis">&nbsp; &nbsp; <span class="nam">app</span><span class="op">.</span><span class="nam">run</span><span class="op">(</span><span class="nam">debug</span><span class="op">=</span><span class="nam">DEBUG</span><span class="op">,</span> <span class="nam">host</span><span class="op">=</span><span class="nam">HOST</span><span class="op">,</span> <span class="nam">port</span><span class="op">=</span><span class="nam">PORT</span><span class="op">)</span><span class="strut">&nbsp;</span></p>
                
            </td>
        </tr>
    </table>
</div>