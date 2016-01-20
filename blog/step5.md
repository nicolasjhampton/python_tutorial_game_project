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

<div id="header">
    <div class="content">
        <h1>Coverage for <b>_server_tests.py</b> :
            <span class="pc_cov">100%</span>
        </h1>

        <img id="keyboard_icon" src="keybd_closed.png" alt="Show keyboard shortcuts" />

        <h2 class="stats">
            19 statements &nbsp;
            <span class="run hide_run shortkey_r button_toggle_run">19 run</span>
            <span class="mis shortkey_m button_toggle_mis">0 missing</span>
            <span class="exc shortkey_x button_toggle_exc">0 excluded</span>

            
        </h2>
    </div>
</div>

<div class="help_panel">
    <img id="panel_icon" src="keybd_open.png" alt="Hide keyboard shortcuts" />
<p class="legend">Hot-keys on this page</p>
    <div>
<p class="keyhelp">
        <span class="key">r</span>
        <span class="key">m</span>
        <span class="key">x</span>
        <span class="key">p</span> &nbsp; toggle line displays
    </p>
<p class="keyhelp">
        <span class="key">j</span>
        <span class="key">k</span> &nbsp; next/prev highlighted chunk
    </p>
<p class="keyhelp">
        <span class="key">0</span> &nbsp; (zero) top of page
    </p>
<p class="keyhelp">
        <span class="key">1</span> &nbsp; (one) first highlighted chunk
    </p>
    </div>
</div>

<div id="source">
    <table>
        <tr>
            <td class="linenos">
<p id="n1" class="pln"><a href="#n1">1</a></p>
<p id="n2" class="pln"><a href="#n2">2</a></p>
<p id="n3" class="pln"><a href="#n3">3</a></p>
<p id="n4" class="stm run hide_run"><a href="#n4">4</a></p>
<p id="n5" class="pln"><a href="#n5">5</a></p>
<p id="n6" class="pln"><a href="#n6">6</a></p>
<p id="n7" class="pln"><a href="#n7">7</a></p>
<p id="n8" class="stm run hide_run"><a href="#n8">8</a></p>
<p id="n9" class="stm run hide_run"><a href="#n9">9</a></p>
<p id="n10" class="pln"><a href="#n10">10</a></p>
<p id="n11" class="stm run hide_run"><a href="#n11">11</a></p>
<p id="n12" class="stm run hide_run"><a href="#n12">12</a></p>
<p id="n13" class="pln"><a href="#n13">13</a></p>
<p id="n14" class="pln"><a href="#n14">14</a></p>
<p id="n15" class="pln"><a href="#n15">15</a></p>
<p id="n16" class="pln"><a href="#n16">16</a></p>
<p id="n17" class="pln"><a href="#n17">17</a></p>
<p id="n18" class="pln"><a href="#n18">18</a></p>
<p id="n19" class="pln"><a href="#n19">19</a></p>
<p id="n20" class="pln"><a href="#n20">20</a></p>
<p id="n21" class="pln"><a href="#n21">21</a></p>
<p id="n22" class="pln"><a href="#n22">22</a></p>
<p id="n23" class="pln"><a href="#n23">23</a></p>
<p id="n24" class="pln"><a href="#n24">24</a></p>
<p id="n25" class="pln"><a href="#n25">25</a></p>
<p id="n26" class="pln"><a href="#n26">26</a></p>
<p id="n27" class="stm run hide_run"><a href="#n27">27</a></p>
<p id="n28" class="pln"><a href="#n28">28</a></p>
<p id="n29" class="stm run hide_run"><a href="#n29">29</a></p>
<p id="n30" class="stm run hide_run"><a href="#n30">30</a></p>
<p id="n31" class="stm run hide_run"><a href="#n31">31</a></p>
<p id="n32" class="stm run hide_run"><a href="#n32">32</a></p>
<p id="n33" class="stm run hide_run"><a href="#n33">33</a></p>
<p id="n34" class="stm run hide_run"><a href="#n34">34</a></p>
<p id="n35" class="stm run hide_run"><a href="#n35">35</a></p>
<p id="n36" class="pln"><a href="#n36">36</a></p>
<p id="n37" class="pln"><a href="#n37">37</a></p>
<p id="n38" class="pln"><a href="#n38">38</a></p>
<p id="n39" class="pln"><a href="#n39">39</a></p>
<p id="n40" class="pln"><a href="#n40">40</a></p>
<p id="n41" class="pln"><a href="#n41">41</a></p>
<p id="n42" class="pln"><a href="#n42">42</a></p>
<p id="n43" class="pln"><a href="#n43">43</a></p>
<p id="n44" class="pln"><a href="#n44">44</a></p>
<p id="n45" class="pln"><a href="#n45">45</a></p>
<p id="n46" class="pln"><a href="#n46">46</a></p>
<p id="n47" class="pln"><a href="#n47">47</a></p>
<p id="n48" class="stm run hide_run"><a href="#n48">48</a></p>
<p id="n49" class="stm run hide_run"><a href="#n49">49</a></p>
<p id="n50" class="stm run hide_run"><a href="#n50">50</a></p>
<p id="n51" class="stm run hide_run"><a href="#n51">51</a></p>
<p id="n52" class="pln"><a href="#n52">52</a></p>
<p id="n53" class="pln"><a href="#n53">53</a></p>
<p id="n54" class="pln"><a href="#n54">54</a></p>
<p id="n55" class="pln"><a href="#n55">55</a></p>
<p id="n56" class="pln"><a href="#n56">56</a></p>
<p id="n57" class="pln"><a href="#n57">57</a></p>
<p id="n58" class="pln"><a href="#n58">58</a></p>
<p id="n59" class="pln"><a href="#n59">59</a></p>
<p id="n60" class="pln"><a href="#n60">60</a></p>
<p id="n61" class="pln"><a href="#n61">61</a></p>
<p id="n62" class="pln"><a href="#n62">62</a></p>
<p id="n63" class="pln"><a href="#n63">63</a></p>
<p id="n64" class="pln"><a href="#n64">64</a></p>
<p id="n65" class="pln"><a href="#n65">65</a></p>
<p id="n66" class="pln"><a href="#n66">66</a></p>
<p id="n67" class="pln"><a href="#n67">67</a></p>
<p id="n68" class="pln"><a href="#n68">68</a></p>
<p id="n69" class="stm run hide_run"><a href="#n69">69</a></p>
<p id="n70" class="stm run hide_run"><a href="#n70">70</a></p>
<p id="n71" class="pln"><a href="#n71">71</a></p>
                
            </td>
            <td class="text">
<p id="t1" class="pln"><span class="com"># I&#39;ve deleted the imports for tempfile and os</span><span class="strut">&nbsp;</span></p>
<p id="t2" class="pln"><span class="com"># since they were for creating a tempfile for a database</span><span class="strut">&nbsp;</span></p>
<p id="t3" class="pln"><span class="com"># and I&#39;m going to make one in memory instead</span><span class="strut">&nbsp;</span></p>
<p id="t4" class="stm run hide_run"><span class="key">import</span> <span class="nam">unittest</span><span class="strut">&nbsp;</span></p>
<p id="t5" class="pln"><span class="strut">&nbsp;</span></p>
<p id="t6" class="pln"><span class="com"># Redirects the database file from our model&#39;s&nbsp; </span><span class="strut">&nbsp;</span></p>
<p id="t7" class="pln"><span class="com"># database file declaration to a test location</span><span class="strut">&nbsp;</span></p>
<p id="t8" class="stm run hide_run"><span class="key">from</span> <span class="nam">playhouse</span><span class="op">.</span><span class="nam">test_utils</span> <span class="key">import</span> <span class="nam">test_database</span><span class="strut">&nbsp;</span></p>
<p id="t9" class="stm run hide_run"><span class="key">from</span> <span class="nam">peewee</span> <span class="key">import</span> <span class="op">*</span><span class="strut">&nbsp;</span></p>
<p id="t10" class="pln"><span class="strut">&nbsp;</span></p>
<p id="t11" class="stm run hide_run"><span class="key">import</span> <span class="nam">server</span><span class="strut">&nbsp;</span></p>
<p id="t12" class="stm run hide_run"><span class="key">from</span> <span class="nam">models</span> <span class="key">import</span> <span class="nam">User</span><span class="strut">&nbsp;</span></p>
<p id="t13" class="pln"><span class="strut">&nbsp;</span></p>
<p id="t14" class="pln"><span class="com"># Instead of running models.initialize, which would </span><span class="strut">&nbsp;</span></p>
<p id="t15" class="pln"><span class="com"># use the model&#39;s DATABASE variable directed at the</span><span class="strut">&nbsp;</span></p>
<p id="t16" class="pln"><span class="com"># &#39;models.db&#39; file, we&#39;re going to direct everything</span><span class="strut">&nbsp;</span></p>
<p id="t17" class="pln"><span class="com"># to our TEST_DB in memory. I also decided to put all</span><span class="strut">&nbsp;</span></p>
<p id="t18" class="pln"><span class="com"># of this in the setUp method. I have no idea if it</span><span class="strut">&nbsp;</span></p>
<p id="t19" class="pln"><span class="com"># works there, but if it does, it will get these </span><span class="strut">&nbsp;</span></p>
<p id="t20" class="pln"><span class="com"># variables out of the global scope, which a </span><span class="strut">&nbsp;</span></p>
<p id="t21" class="pln"><span class="com"># principal of functional programming</span><span class="strut">&nbsp;</span></p>
<p id="t22" class="pln"><span class="com"># TEST_DB = SqliteDatabase(&#39;:memory:&#39;)</span><span class="strut">&nbsp;</span></p>
<p id="t23" class="pln"><span class="com"># TEST_DB.connect()</span><span class="strut">&nbsp;</span></p>
<p id="t24" class="pln"><span class="com"># TEST_DB.create_tables([User], safe=True)</span><span class="strut">&nbsp;</span></p>
<p id="t25" class="pln"><span class="strut">&nbsp;</span></p>
<p id="t26" class="pln"><span class="strut">&nbsp;</span></p>
<p id="t27" class="stm run hide_run"><span class="key">class</span> <span class="nam">AppTestCase</span><span class="op">(</span><span class="nam">unittest</span><span class="op">.</span><span class="nam">TestCase</span><span class="op">)</span><span class="op">:</span><span class="strut">&nbsp;</span></p>
<p id="t28" class="pln"><span class="strut">&nbsp;</span></p>
<p id="t29" class="stm run hide_run">&nbsp; &nbsp; <span class="key">def</span> <span class="nam">setUp</span><span class="op">(</span><span class="nam">self</span><span class="op">)</span><span class="op">:</span><span class="strut">&nbsp;</span></p>
<p id="t30" class="stm run hide_run">&nbsp; &nbsp; &nbsp; &nbsp; <span class="nam">self</span><span class="op">.</span><span class="nam">TEST_DB</span> <span class="op">=</span> <span class="nam">SqliteDatabase</span><span class="op">(</span><span class="str">&#39;:memory:&#39;</span><span class="op">)</span><span class="strut">&nbsp;</span></p>
<p id="t31" class="stm run hide_run">&nbsp; &nbsp; &nbsp; &nbsp; <span class="nam">self</span><span class="op">.</span><span class="nam">TEST_DB</span><span class="op">.</span><span class="nam">connect</span><span class="op">(</span><span class="op">)</span><span class="strut">&nbsp;</span></p>
<p id="t32" class="stm run hide_run">&nbsp; &nbsp; &nbsp; &nbsp; <span class="nam">self</span><span class="op">.</span><span class="nam">TEST_DB</span><span class="op">.</span><span class="nam">create_tables</span><span class="op">(</span><span class="op">[</span><span class="nam">User</span><span class="op">]</span><span class="op">,</span> <span class="nam">safe</span><span class="op">=</span><span class="key">True</span><span class="op">)</span><span class="strut">&nbsp;</span></p>
<p id="t33" class="stm run hide_run">&nbsp; &nbsp; &nbsp; &nbsp; <span class="nam">server</span><span class="op">.</span><span class="nam">app</span><span class="op">.</span><span class="nam">config</span><span class="op">[</span><span class="str">&#39;TESTING&#39;</span><span class="op">]</span> <span class="op">=</span> <span class="key">True</span><span class="strut">&nbsp;</span></p>
<p id="t34" class="stm run hide_run">&nbsp; &nbsp; &nbsp; &nbsp; <span class="nam">server</span><span class="op">.</span><span class="nam">app</span><span class="op">.</span><span class="nam">config</span><span class="op">[</span><span class="str">&#39;WTF_CSRF_ENABLED&#39;</span><span class="op">]</span> <span class="op">=</span> <span class="key">False</span><span class="strut">&nbsp;</span></p>
<p id="t35" class="stm run hide_run">&nbsp; &nbsp; &nbsp; &nbsp; <span class="nam">self</span><span class="op">.</span><span class="nam">app</span> <span class="op">=</span> <span class="nam">server</span><span class="op">.</span><span class="nam">app</span><span class="op">.</span><span class="nam">test_client</span><span class="op">(</span><span class="op">)</span><span class="strut">&nbsp;</span></p>
<p id="t36" class="pln">&nbsp; &nbsp; &nbsp; &nbsp; <span class="com"># flask lays out these instructions for using app.config</span><span class="strut">&nbsp;</span></p>
<p id="t37" class="pln">&nbsp; &nbsp; &nbsp; &nbsp; <span class="com"># to redirect the tests to our test database.</span><span class="strut">&nbsp;</span></p>
<p id="t38" class="pln">&nbsp; &nbsp; &nbsp; &nbsp; <span class="com"># I&#39;ve opted to use test_database instead...</span><span class="strut">&nbsp;</span></p>
<p id="t39" class="pln">&nbsp; &nbsp; &nbsp; &nbsp; <span class="com"># self.db_fd, app.app.config[&#39;DATABASE&#39;] = tempfile.mkstemp()</span><span class="strut">&nbsp;</span></p>
<p id="t40" class="pln">&nbsp; &nbsp; &nbsp; &nbsp; <span class="com"># app.app.config[&#39;TESTING&#39;] = True</span><span class="strut">&nbsp;</span></p>
<p id="t41" class="pln">&nbsp; &nbsp; &nbsp; &nbsp; <span class="com"># self.app = app.app.test_client()</span><span class="strut">&nbsp;</span></p>
<p id="t42" class="pln">&nbsp; &nbsp; &nbsp; &nbsp; <span class="com"># flaskr.init_db()</span><span class="strut">&nbsp;</span></p>
<p id="t43" class="pln"><span class="strut">&nbsp;</span></p>
<p id="t44" class="pln">&nbsp; &nbsp; <span class="com"># def tearDown(self):</span><span class="strut">&nbsp;</span></p>
<p id="t45" class="pln">&nbsp; &nbsp; <span class="com">#&nbsp; &nbsp;&nbsp; os.close(self.db_fd)</span><span class="strut">&nbsp;</span></p>
<p id="t46" class="pln">&nbsp; &nbsp; <span class="com">#&nbsp; &nbsp;&nbsp; os.unlink(app.app.config[&#39;DATABASE&#39;])</span><span class="strut">&nbsp;</span></p>
<p id="t47" class="pln"><span class="strut">&nbsp;</span></p>
<p id="t48" class="stm run hide_run">&nbsp; &nbsp; <span class="key">def</span> <span class="nam">test_register_url</span><span class="op">(</span><span class="nam">self</span><span class="op">)</span><span class="op">:</span><span class="strut">&nbsp;</span></p>
<p id="t49" class="stm run hide_run">&nbsp; &nbsp; &nbsp; &nbsp; <span class="key">with</span> <span class="nam">test_database</span><span class="op">(</span><span class="nam">self</span><span class="op">.</span><span class="nam">TEST_DB</span><span class="op">,</span> <span class="op">(</span><span class="nam">User</span><span class="op">,</span><span class="op">)</span><span class="op">)</span><span class="op">:</span><span class="strut">&nbsp;</span></p>
<p id="t50" class="stm run hide_run">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <span class="nam">rv</span> <span class="op">=</span> <span class="nam">self</span><span class="op">.</span><span class="nam">app</span><span class="op">.</span><span class="nam">get</span><span class="op">(</span><span class="str">&#39;/register&#39;</span><span class="op">)</span><span class="strut">&nbsp;</span></p>
<p id="t51" class="stm run hide_run">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <span class="nam">self</span><span class="op">.</span><span class="nam">assertEqual</span><span class="op">(</span><span class="nam">rv</span><span class="op">.</span><span class="nam">status_code</span><span class="op">,</span> <span class="num">200</span><span class="op">)</span><span class="strut">&nbsp;</span></p>
<p id="t52" class="pln"><span class="strut">&nbsp;</span></p>
<p id="t53" class="pln"><span class="strut">&nbsp;</span></p>
<p id="t54" class="pln">&nbsp; &nbsp; <span class="com"># Saving this for later...</span><span class="strut">&nbsp;</span></p>
<p id="t55" class="pln">&nbsp; &nbsp; <span class="com"># def test_registration(self):</span><span class="strut">&nbsp;</span></p>
<p id="t56" class="pln">&nbsp; &nbsp; <span class="com">#&nbsp; &nbsp;&nbsp; data = {</span><span class="strut">&nbsp;</span></p>
<p id="t57" class="pln">&nbsp; &nbsp; <span class="com">#&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &#39;username&#39;: &#39;testUsername&#39;,</span><span class="strut">&nbsp;</span></p>
<p id="t58" class="pln">&nbsp; &nbsp; <span class="com">#&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &#39;email&#39;: &#39;test@example.com&#39;,</span><span class="strut">&nbsp;</span></p>
<p id="t59" class="pln">&nbsp; &nbsp; <span class="com">#&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &#39;password&#39;: &#39;password&#39;,</span><span class="strut">&nbsp;</span></p>
<p id="t60" class="pln">&nbsp; &nbsp; <span class="com">#&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &#39;password2&#39;: &#39;password&#39;</span><span class="strut">&nbsp;</span></p>
<p id="t61" class="pln">&nbsp; &nbsp; <span class="com">#&nbsp; &nbsp;&nbsp; }</span><span class="strut">&nbsp;</span></p>
<p id="t62" class="pln">&nbsp; &nbsp; <span class="com">#&nbsp; &nbsp;&nbsp; with test_database(TEST_DB, (User,)):</span><span class="strut">&nbsp;</span></p>
<p id="t63" class="pln">&nbsp; &nbsp; <span class="com">#&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; rv = self.app.post(</span><span class="strut">&nbsp;</span></p>
<p id="t64" class="pln">&nbsp; &nbsp; <span class="com">#&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &#39;/register&#39;,</span><span class="strut">&nbsp;</span></p>
<p id="t65" class="pln">&nbsp; &nbsp; <span class="com">#&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; data=data)</span><span class="strut">&nbsp;</span></p>
<p id="t66" class="pln">&nbsp; &nbsp; <span class="com">#&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; self.assertEqual(rv.status_code, 302)</span><span class="strut">&nbsp;</span></p>
<p id="t67" class="pln">&nbsp; &nbsp; <span class="com">#&nbsp; &nbsp; &nbsp; &nbsp;&nbsp; self.assertEqual(rv.location, &#39;http://localhost/&#39;)</span><span class="strut">&nbsp;</span></p>
<p id="t68" class="pln"><span class="strut">&nbsp;</span></p>
<p id="t69" class="stm run hide_run"><span class="key">if</span> <span class="nam">__name__</span> <span class="op">==</span> <span class="str">&#39;__main__&#39;</span><span class="op">:</span><span class="strut">&nbsp;</span></p>
<p id="t70" class="stm run hide_run">&nbsp; &nbsp; <span class="nam">unittest</span><span class="op">.</span><span class="nam">main</span><span class="op">(</span><span class="op">)</span><span class="strut">&nbsp;</span></p>
<p id="t71" class="pln"><span class="strut">&nbsp;</span></p>
                
            </td>
        </tr>
    </table>
</div>

<div id="footer">
    <div class="content">
        <p>
            <a class="nav" href="index.html">&#xab; index</a> &nbsp; &nbsp; <a class="nav" href="https://coverage.readthedocs.org">coverage.py v4.0.3</a>,
            created at 2016-01-19 18:55
        </p>
    </div>
</div>